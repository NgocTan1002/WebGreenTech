from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, CustomerAddress


class CustomerAddressInline(admin.TabularInline):
    model = CustomerAddress
    extra = 0
    fields = [
        "label", "address_line1", "city",
        "country", "is_default_shipping", "is_default_billing",
    ]


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    """
    Kế thừa UserAdmin để giữ nguyên chức năng
    đổi password, permission của Django.
    """
    model = Customer
    list_display = [
        "email", "display_full_name", "company_name",
        "company_type", "is_verified", "is_vip",
        "is_staff", "is_active", "created_at",
    ]
    list_filter = [
        "is_active", "is_staff", "is_verified",
        "is_vip", "company_type",
    ]
    search_fields = ["email", "first_name", "last_name", "company_name"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at", "last_login"]
    inlines = [CustomerAddressInline]

    # UserAdmin dùng username — override lại để dùng email
    fieldsets = [
        ("Tài khoản", {
            "fields": ["email", "password"],
        }),
        ("Thông tin cá nhân", {
            "fields": ["first_name", "last_name", "phone"],
        }),
        ("Thông tin công ty", {
            "fields": [
                "company_name", "company_type",
                "job_title", "industry",
            ],
        }),
        ("Trạng thái", {
            "fields": [
                "is_active", "is_staff", "is_superuser",
                "is_verified", "is_vip", "newsletter_subscribed",
            ],
        }),
        ("Phân quyền", {
            "fields": ["groups", "user_permissions"],
            "classes": ["collapse"],
        }),
        ("Thời gian", {
            "fields": ["last_login", "created_at", "updated_at"],
            "classes": ["collapse"],
        }),
    ]

    # Form tạo user mới
    add_fieldsets = [
        (None, {
            "classes": ["wide"],
            "fields": [
                "email", "first_name", "last_name",
                "password1", "password2",
                "company_name", "is_staff",
            ],
        }),
    ]

    def display_full_name(self, obj):
        return obj.get_full_name()
    display_full_name.short_description = 'Họ và tên'