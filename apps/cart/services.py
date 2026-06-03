from apps.cart.models import Cart


class CartService:

    @staticmethod
    def get_or_create_cart(request) -> Cart:
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(
                customer=request.user,
                is_active=True,
                defaults={'session_key': ''},
            )
            # Gộp session cart (nếu có) vào customer cart
            session_key = request.session.get('cart_session_key')
            if session_key:
                try:
                    session_cart = Cart.objects.get(
                        session_key=session_key,
                        is_active=True,
                        customer=None,
                    )
                    cart.merge_with(session_cart)
                    # Xóa session key sau khi merge
                    del request.session['cart_session_key']
                except Cart.DoesNotExist:
                    pass
            return cart

        # Guest — dùng session_key
        session_key = CartService._ensure_session_key(request)
        cart, _ = Cart.objects.get_or_create(
            session_key=session_key,
            is_active=True,
            customer=None,
            defaults={},
        )
        return cart

    @staticmethod
    def _ensure_session_key(request) -> str:
        """
        Đảm bảo session đã có key, tạo mới nếu cần.
        Lưu key vào session để dùng lại giữa các request.
        """
        if not request.session.session_key:
            request.session.create()
        key = request.session.get('cart_session_key')
        if not key:
            key = request.session.session_key
            request.session['cart_session_key'] = key
        return key

    @staticmethod
    def clear_cart(request) -> None:
        """Vô hiệu hóa giỏ hàng hiện tại (sau khi đặt hàng thành công)."""
        cart = CartService.get_or_create_cart(request)
        cart.is_active = False
        cart.save(update_fields=['is_active'])
