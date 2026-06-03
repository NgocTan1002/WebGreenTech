from django.contrib import admin
from django.utils.html import format_html
from .models import ContactInquiry, DemoRequest


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'company', 'email',
        'inquiry_type_badge', 'status_badge',
        'subject', 'created_at',
    ]
    list_filter   = ['status', 'inquiry_type', 'created_at']
    search_fields = ['name', 'email', 'company', 'subject']
    readonly_fields = [
        'ip_address', 'user_agent', 'source_url',
        'created_at', 'updated_at',
    ]
    date_hierarchy = 'created_at'
    list_per_page  = 50

    fieldsets = [
        ('Người gửi', {
            'fields': [('name', 'email'), ('phone', 'company'), 'country'],
        }),
        ('Nội dung', {
            'fields': ['inquiry_type', 'subject', 'message'],
        }),
        ('Xử lý', {
            'fields': ['status', 'internal_notes'],
        }),
        ('Metadata', {
            'fields': ['ip_address', 'user_agent', 'source_url',
                       'created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]

    actions = ['action_mark_read', 'action_mark_replied', 'action_close']

    def has_add_permission(self, request):
        return False  # chỉ tạo qua form public

    # ── Badges ────────────────────────────────────────────────────────────────

    def inquiry_type_badge(self, obj):
        colors = {
            ContactInquiry.INQUIRY_GENERAL:     ('#4A5568', '#EDF2F7'),
            ContactInquiry.INQUIRY_TECHNICAL:   ('#1A365D', '#BEE3F8'),
            ContactInquiry.INQUIRY_SALES:       ('#276749', '#C6F6D5'),
            ContactInquiry.INQUIRY_SUPPORT:     ('#744210', '#FEFCBF'),
            ContactInquiry.INQUIRY_PARTNERSHIP: ('#44337A', '#E9D8FD'),
        }
        fg, bg = colors.get(obj.inquiry_type, ('#555', '#EEE'))
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;'
            'border-radius:10px;font-size:11px;font-weight:600">{}</span>',
            bg, fg, obj.get_inquiry_type_display(),
        )
    inquiry_type_badge.short_description = 'Loại'

    def status_badge(self, obj):
        colors = {
            ContactInquiry.STATUS_NEW:     ('#744210', '#FEFCBF'),
            ContactInquiry.STATUS_READ:    ('#1A365D', '#BEE3F8'),
            ContactInquiry.STATUS_REPLIED: ('#276749', '#C6F6D5'),
            ContactInquiry.STATUS_CLOSED:  ('#4A5568', '#EDF2F7'),
        }
        fg, bg = colors.get(obj.status, ('#555', '#EEE'))
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;'
            'border-radius:10px;font-size:11px;font-weight:600">{}</span>',
            bg, fg, obj.get_status_display(),
        )
    status_badge.short_description = 'Trạng thái'
    status_badge.admin_order_field = 'status'

    # ── Actions ───────────────────────────────────────────────────────────────

    @admin.action(description='Đánh dấu Đã đọc')
    def action_mark_read(self, request, queryset):
        n = queryset.filter(status=ContactInquiry.STATUS_NEW).update(
            status=ContactInquiry.STATUS_READ
        )
        self.message_user(request, f'Đã đánh dấu đã đọc {n} liên hệ.')

    @admin.action(description='Đánh dấu Đã trả lời')
    def action_mark_replied(self, request, queryset):
        n = queryset.filter(
            status__in=[ContactInquiry.STATUS_NEW, ContactInquiry.STATUS_READ]
        ).update(status=ContactInquiry.STATUS_REPLIED)
        self.message_user(request, f'Đã đánh dấu đã trả lời {n} liên hệ.')

    @admin.action(description='Đóng liên hệ')
    def action_close(self, request, queryset):
        n = queryset.exclude(status=ContactInquiry.STATUS_CLOSED).update(
            status=ContactInquiry.STATUS_CLOSED
        )
        self.message_user(request, f'Đã đóng {n} liên hệ.')


@admin.register(DemoRequest)
class DemoRequestAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'company', 'email',
        'solution', 'preferred_date',
        'status_badge', 'created_at',
    ]
    list_filter   = ['status', 'created_at', 'solution']
    search_fields = ['name', 'email', 'company']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['solution']
    date_hierarchy = 'created_at'
    list_per_page  = 50

    fieldsets = [
        ('Người đăng ký', {
            'fields': [
                ('name', 'email'),
                ('phone', 'company'),
                ('job_title', 'country'),
            ],
        }),
        ('Yêu cầu demo', {
            'fields': ['solution', 'preferred_date', 'message'],
        }),
        ('Xử lý', {
            'fields': ['status'],
        }),
        ('Thời gian', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]

    actions = ['action_schedule', 'action_complete', 'action_cancel']

    def has_add_permission(self, request):
        return False

    def status_badge(self, obj):
        colors = {
            DemoRequest.STATUS_NEW:       ('#744210', '#FEFCBF'),
            DemoRequest.STATUS_SCHEDULED: ('#1A365D', '#BEE3F8'),
            DemoRequest.STATUS_COMPLETED: ('#276749', '#C6F6D5'),
            DemoRequest.STATUS_CANCELLED: ('#742A2A', '#FED7D7'),
        }
        fg, bg = colors.get(obj.status, ('#555', '#EEE'))
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;'
            'border-radius:10px;font-size:11px;font-weight:600">{}</span>',
            bg, fg, obj.get_status_display(),
        )
    status_badge.short_description = 'Trạng thái'
    status_badge.admin_order_field = 'status'

    @admin.action(description='Đánh dấu Đã lên lịch')
    def action_schedule(self, request, queryset):
        n = queryset.filter(status=DemoRequest.STATUS_NEW).update(
            status=DemoRequest.STATUS_SCHEDULED
        )
        self.message_user(request, f'Đã lên lịch {n} demo.')

    @admin.action(description='Đánh dấu Hoàn thành')
    def action_complete(self, request, queryset):
        n = queryset.filter(status=DemoRequest.STATUS_SCHEDULED).update(
            status=DemoRequest.STATUS_COMPLETED
        )
        self.message_user(request, f'Đã hoàn thành {n} demo.')

    @admin.action(description='Huỷ demo')
    def action_cancel(self, request, queryset):
        n = queryset.filter(
            status__in=[DemoRequest.STATUS_NEW, DemoRequest.STATUS_SCHEDULED]
        ).update(status=DemoRequest.STATUS_CANCELLED)
        self.message_user(request, f'Đã huỷ {n} demo.')