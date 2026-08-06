from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from apps.core.db import (
    get_cart_detail, get_cart_summary,
    upsert_cart_item, get_product_detail,
)
from apps.cart.services import CartService
 
 
class CartDetailView(TemplateView):
    template_name = "cart/detail.html"
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart    = CartService.get_or_create_cart(self.request)
        items   = get_cart_detail(str(cart.id))
        summary = get_cart_summary(str(cart.id))
        has_pending_quote = any(item.get("price_pending") for item in items)
        context.update({
            "cart":       cart,
            "cart_items": items,
            "subtotal":   summary["subtotal"],
            "total_items": summary["total_items"],
            "has_pending_quote": has_pending_quote,
        })
        return context
 
 
class CartAddView(View):
 
    def post(self, request, slug=None, *args, **kwargs):
        slug       = slug or request.POST.get("product_slug")
        quantity   = int(request.POST.get("quantity", 1))
        product    = get_product_detail(slug)
 
        if not product:
            return JsonResponse({"success": False, "message": "Sản phẩm không tồn tại"}, status=404)
 
        if product["stock_status"] == "out_of_stock":
            return JsonResponse({"success": False, "message": "Sản phẩm đã hết hàng"}, status=400)

        pricing_type = product.get("pricing_type")
        requires_quote = product.get("requires_quote", False)
        if pricing_type == "contact" and not requires_quote:
            message = "Sản phẩm này cần liên hệ tư vấn trước khi báo giá."
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({
                    "success": False,
                    "message": message,
                    "contact_url": f'{reverse("contacts:contact")}?product={product["slug"]}',
                }, status=400)
            messages.info(request, message)
            return redirect(f'{reverse("contacts:contact")}?product={product["slug"]}')

        cart   = CartService.get_or_create_cart(request)
        price_pending = requires_quote or pricing_type != "fixed"
        price = None if price_pending else (
            product.get("sale_price") or product.get("price")
        )
        result = upsert_cart_item(str(cart.id), product["id"], quantity, price)
 
        summary = get_cart_summary(str(cart.id))
 
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success":         True,
                "message":         (
                    f'Đã thêm "{product["name"]}" vào yêu cầu báo giá.'
                    if price_pending
                    else f'Đã thêm "{product["name"]}" vào giỏ hàng.'
                ),
                "cart_total_items": summary["total_items"],
                "item_quantity":   result["quantity"],
                "created":         result["created"],
            })
 
        messages.success(
            request,
            (
                f'Đã thêm "{product["name"]}" vào yêu cầu báo giá.'
                if price_pending
                else f'Đã thêm "{product["name"]}" vào giỏ hàng.'
            ),
        )
        return redirect("cart:detail")
    
class CartUpdateView(View):
    def post(self, request, *args, **kwargs):
        from apps.cart.models import CartItem
        item_id = kwargs.get('item_id')
        quantity = int(request.POST.get("quantity", 1))

        cart = CartService.get_or_create_cart(request)

        try:
            item =  CartItem.objects.get(id=item_id, cart=cart)
            if quantity <= 0:
                item.delete()
            else:
                item.quantity = quantity
                item.save(update_fields=["quantity", "updated_at"])
        except CartItem.DoesNotExist:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success":False, "message":"Item không tồn tại."}, status=404)
            messages.error(request, "Item không tồn tại.")
            return redirect("cart:detail")
        
        summary = get_cart_summary(str(cart.id))

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "cart_total_items": summary["total_items"],
                "subtotal": str(summary["subtotal"]),
            })
        
        return redirect("cart:detail")
    
class CartRemoveView(View):
    def post(self, request, *args, **kwargs):
        from apps.cart.models import CartItem
        item_id = kwargs.get('item_id')

        cart = CartService.get_or_create_cart(request)

        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            product_name = item.product.name
            item.delete()
        except CartItem.DoesNotExist:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": False, "message": "Item không tồn tại."})
            return redirect("cart:detail")
        
        summary = get_cart_summary(str(cart.id))

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "message": f'Đã xóa "{product_name}" khỏi giỏ hàng.',
                "cart_total_items": summary["total_items"],
                "subtotal": str(summary["subtotal"]),
            })
        
        messages.success(request, f'Đã xóa "{product_name}" khỏi giỏ hàng.')
        return redirect("cart:detail")
    
class CartClearView(View):
    def post(self, request, *args, **kwargs):
        cart = CartService.get_or_create_cart(request)
        cart.items.all().delete()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "message": "Đã làm mới giỏ hàng."})
        messages.success(request, "Đã làm mới giỏ hàng.")
        return redirect("cart:detail")
