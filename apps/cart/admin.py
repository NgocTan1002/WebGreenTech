from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['product', 'quantity', 'unit_price', 'line_total_display']
    readonly_fields = ['line_total_display']

    def line_total_display(self, obj):
        if obj.pk:
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
        return f'{int(obj.subtotal):,} ₫'
    subtotal_display.short_description = 'Tạm tính'

    def has_add_permission(self, request):
        return False  # cart chỉ được tạo qua code, không tạo thủ công
