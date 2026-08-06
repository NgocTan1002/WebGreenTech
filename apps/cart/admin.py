from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['product', 'quantity', 'pricing_type', 'unit_price', 'line_total_display']
    readonly_fields = ['pricing_type', 'line_total_display']

    def line_total_display(self, obj):
        if obj.pk:
            if obj.price_pending:
                return 'Chờ báo giá'
            return f'{int(obj.line_total):,} ₫'
        return '—'
    line_total_display.short_description = 'Thành tiền'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display  = ['id', 'customer', 'session_key', 'is_active',
                     'total_items', 'subtotal_display', 'created_at']
    list_filter   = ['is_active', 'created_at']
    search_fields = ['customer__email', 'session_key']
    readonly_fields = ['id', 'total_items', 'subtotal_display', 'created_at', 'updated_at']
    raw_id_fields   = ['customer']   # tránh load dropdown toàn bộ user
    inlines         = [CartItemInline]

    # Không có actions, không có fieldsets phức tạp — chỉ để xem
    def subtotal_display(self, obj):
        subtotal = obj.subtotal
        if obj.has_pending_quote:
            if subtotal:
                return f'{int(subtotal):,} ₫ + Chờ báo giá'
            return 'Chờ báo giá'
        return f'{int(subtotal):,} ₫'
    subtotal_display.short_description = 'Tạm tính'

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related('customer')
            .prefetch_related('items')
        )

    def has_add_permission(self, request):
        return False  # cart chỉ được tạo qua code, không tạo thủ công
