# apps/orders/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Order, OrderItem, QuoteRequest, QuoteRequestItem


# ── Inlines ───────────────────────────────────────────────────────────────────

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product', 'product_sku', 'product_name', 'quantity', 'unit_price', 'line_total_display']
    readonly_fields = ['product_sku', 'product_name', 'line_total_display']

    def line_total_display(self, obj):
        if obj.pk:
            return f'{int(obj.line_total):,} ₫'
        return '—'
    line_total_display.short_description = 'Thành tiền'


class QuoteRequestItemInline(admin.TabularInline):
    model = QuoteRequestItem
    extra = 1
    fields = ['product', 'product_sku', 'product_name', 'quantity', 'notes']
    readonly_fields = ['product_sku', 'product_name']


# ── OrderAdmin ────────────────────────────────────────────────────────────────

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'order_type_badge', 'status_badge',
        'company_name', 'email',
        'total_display', 'item_count',
        'created_at',
    ]
    list_filter  = ['status', 'order_type', 'created_at']
    search_fields = ['order_number', 'email', 'company_name', 'po_number']
    readonly_fields = [
        'id', 'order_number',
        'subtotal', 'total',
        'created_at', 'updated_at',
        'from_quote_link',
    ]
    date_hierarchy = 'created_at'
    list_per_page  = 50
    save_on_top    = True
    inlines        = [OrderItemInline]

    fieldsets = [
        ('Thông tin đơn hàng', {
            'fields': ['id', 'order_number', 'order_type', 'status', 'po_number'],
        }),
        ('Khách hàng', {
            'fields': [
                'customer',
                ('first_name', 'last_name'),
                ('email', 'phone'),
                'company_name',
            ],
        }),
        ('Địa chỉ', {
            'fields': ['shipping_address', 'billing_address'],
            'classes': ['collapse'],
        }),
        ('Tài chính', {
            'fields': ['subtotal', 'total'],
        }),
        ('Vận chuyển', {
            'fields': ['tracking_number', 'shipped_at', 'delivered_at'],
            'classes': ['collapse'],
        }),
        ('Ghi chú', {
            'fields': ['customer_notes', 'internal_notes'],
            'classes': ['collapse'],
        }),
        ('Liên kết', {
            'fields': ['from_quote_link'],
            'classes': ['collapse'],
        }),
        ('Thời gian', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]

    actions = [
        'action_confirm',
        'action_mark_processing',
        'action_mark_shipped',
        'action_cancel',
    ]

    # ── Cột hiển thị ──────────────────────────────────────────────────────────

    def order_type_badge(self, obj):
        if obj.order_type == Order.ORDER_TYPE_QUOTE:
            bg, fg = '#EBF8FF', '#2B6CB0'
        else:
            bg, fg = '#F0FFF4', '#276749'
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;'
            'border-radius:10px;font-size:11px;font-weight:600">{}</span>',
            bg, fg, obj.get_order_type_display(),
        )
    order_type_badge.short_description = 'Loại đơn'

    def status_badge(self, obj):
        colors = {
            Order.STATUS_PENDING:    ('#744210', '#FEFCBF'),
            Order.STATUS_CONFIRMED:  ('#1A365D', '#BEE3F8'),
            Order.STATUS_PROCESSING: ('#322659', '#E9D8FD'),
            Order.STATUS_SHIPPED:    ('#1A365D', '#BEE3F8'),
            Order.STATUS_DELIVERED:  ('#276749', '#C6F6D5'),
            Order.STATUS_CANCELLED:  ('#742A2A', '#FED7D7'),
            Order.STATUS_REFUNDED:   ('#4A5568', '#EDF2F7'),
        }
        fg, bg = colors.get(obj.status, ('#555', '#EEE'))
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;'
            'border-radius:10px;font-size:11px;font-weight:600">{}</span>',
            bg, fg, obj.get_status_display(),
        )
    status_badge.short_description = 'Trạng thái'
    status_badge.admin_order_field = 'status'

    def total_display(self, obj):
        if obj.total:
            return f'{int(obj.total):,} ₫'
        return '—'
    total_display.short_description = 'Tổng tiền'
    total_display.admin_order_field = 'total'

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'SL dòng'

    def from_quote_link(self, obj):
        try:
            q = obj.from_quote
            url = f'/admin/orders/quoterequest/{q.pk}/change/'
            return format_html('<a href="{}">{}</a>', url, q.reference)
        except Exception:
            return '—'
    from_quote_link.short_description = 'Từ báo giá'

    # ── Actions ───────────────────────────────────────────────────────────────

    @admin.action(description='✅ Xác nhận đơn hàng')
    def action_confirm(self, request, queryset):
        n = queryset.filter(status=Order.STATUS_PENDING).update(status=Order.STATUS_CONFIRMED)
        self.message_user(request, f'Đã xác nhận {n} đơn hàng.')

    @admin.action(description='⚙️ Chuyển sang Đang xử lý')
    def action_mark_processing(self, request, queryset):
        n = queryset.filter(status=Order.STATUS_CONFIRMED).update(status=Order.STATUS_PROCESSING)
        self.message_user(request, f'Đã chuyển {n} đơn sang đang xử lý.')

    @admin.action(description='🚚 Đánh dấu Đã giao vận')
    def action_mark_shipped(self, request, queryset):
        n = queryset.filter(status=Order.STATUS_PROCESSING).update(
            status=Order.STATUS_SHIPPED,
            shipped_at=timezone.now(),
        )
        self.message_user(request, f'Đã cập nhật {n} đơn hàng sang đã giao vận.')

    @admin.action(description='✖ Huỷ đơn hàng')
    def action_cancel(self, request, queryset):
        allowed = [Order.STATUS_PENDING, Order.STATUS_CONFIRMED]
        n = queryset.filter(status__in=allowed).update(status=Order.STATUS_CANCELLED)
        self.message_user(request, f'Đã huỷ {n} đơn hàng.')


# ── QuoteRequestAdmin ─────────────────────────────────────────────────────────

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = [
        'reference', 'status_badge',
        'company', 'name', 'email',
        'solution', 'item_count',
        'assigned_to', 'created_at',
    ]
    list_filter  = ['status', 'created_at']
    search_fields = ['reference', 'email', 'company', 'name']
    readonly_fields = ['reference', 'created_at', 'updated_at', 'converted_order_link']
    autocomplete_fields = ['assigned_to', 'solution']
    date_hierarchy = 'created_at'
    list_per_page  = 50
    save_on_top    = True
    inlines        = [QuoteRequestItemInline]
    list_editable  = ['assigned_to']

    fieldsets = [
        ('Thông tin yêu cầu báo giá', {
            'fields': ['reference', 'status', 'solution', 'application'],
        }),
        ('Liên hệ', {
            'fields': [('name', 'email'), ('phone', 'company')],
        }),
        ('Nội dung yêu cầu', {
            'fields': ['message'],
        }),
        ('Xử lý nội bộ', {
            'fields': ['assigned_to', 'internal_notes', 'converted_order_link'],
        }),
        ('Thời gian', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]

    actions = [
        'action_mark_in_review',
        'action_mark_quoted',
        'action_decline',
    ]

    # ── Cột hiển thị ──────────────────────────────────────────────────────────

    def status_badge(self, obj):
        colors = {
            QuoteRequest.STATUS_NEW:       ('#744210', '#FEFCBF'),
            QuoteRequest.STATUS_IN_REVIEW: ('#322659', '#E9D8FD'),
            QuoteRequest.STATUS_QUOTED:    ('#1A365D', '#BEE3F8'),
            QuoteRequest.STATUS_ACCEPTED:  ('#276749', '#C6F6D5'),
            QuoteRequest.STATUS_DECLINED:  ('#742A2A', '#FED7D7'),
        }
        fg, bg = colors.get(obj.status, ('#555', '#EEE'))
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;'
            'border-radius:10px;font-size:11px;font-weight:600">{}</span>',
            bg, fg, obj.get_status_display(),
        )
    status_badge.short_description = 'Trạng thái'
    status_badge.admin_order_field = 'status'

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Số sản phẩm'

    def converted_order_link(self, obj):
        if obj.converted_to_order:
            o = obj.converted_to_order
            url = f'/admin/orders/order/{o.pk}/change/'
            return format_html('<a href="{}">{}</a>', url, o.order_number)
        return 'Chưa chuyển đổi'
    converted_order_link.short_description = 'Đơn hàng đã tạo'

    @admin.action(description='👁 Chuyển sang Đang xem xét')
    def action_mark_in_review(self, request, queryset):
        n = queryset.filter(status=QuoteRequest.STATUS_NEW).update(
            status=QuoteRequest.STATUS_IN_REVIEW
        )
        self.message_user(request, f'Đã chuyển {n} RFQ sang đang xem xét.')

    @admin.action(description='💬 Đánh dấu Đã báo giá')
    def action_mark_quoted(self, request, queryset):
        n = queryset.filter(status=QuoteRequest.STATUS_IN_REVIEW).update(
            status=QuoteRequest.STATUS_QUOTED
        )
        self.message_user(request, f'Đã cập nhật {n} RFQ sang đã báo giá.')

    @admin.action(description='✖ Từ chối báo giá')
    def action_decline(self, request, queryset):
        allowed = [QuoteRequest.STATUS_NEW, QuoteRequest.STATUS_IN_REVIEW]
        n = queryset.filter(status__in=allowed).update(status=QuoteRequest.STATUS_DECLINED)
        self.message_user(request, f'Đã từ chối {n} RFQ.')