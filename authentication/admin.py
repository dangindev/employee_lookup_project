from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LDAPUserPermission

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'account_type', 'role', 'company', 'is_active', 'is_staff']
    list_filter = ['account_type', 'role', 'company', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin TTGroup', {
            'fields': ('account_type', 'role', 'company', 'phone', 'ldap_dn'),
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Thông tin TTGroup', {
            'fields': ('account_type', 'role', 'company', 'phone'),
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role'):
            if request.user.role == 'admin_company':
                # Admin công ty chỉ thấy users của công ty mình
                return qs.filter(company=request.user.company)
            elif request.user.role == 'admin_corporation':
                # Admin tập đoàn thấy tất cả
                return qs
        return qs
    
    def save_model(self, request, obj, form, change):
        if not change:  # Tạo mới
            if obj.account_type == 'system' and not obj.password:
                obj.set_password('temp123')  # Password tạm thời
        super().save_model(request, obj, form, change)

@admin.register(LDAPUserPermission)
class LDAPUserPermissionAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'company', 'is_allowed', 'created_by', 'created_at']
    list_filter = ['role', 'company', 'is_allowed', 'created_at']
    search_fields = ['username']
    
    fieldsets = (
        ('Thông tin LDAP User', {
            'fields': ('username', 'is_allowed')
        }),
        ('Phân quyền', {
            'fields': ('role', 'company')
        }),
        ('Thông tin tạo', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_by']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Tạo mới
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'admin_company':
            # Admin công ty chỉ thấy LDAP users của công ty mình
            return qs.filter(company=request.user.company)
        return qs
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company":
            if hasattr(request.user, 'role') and request.user.role == 'admin_company':
                # Admin công ty chỉ chọn được công ty của mình
                kwargs["queryset"] = request.user.company.__class__.objects.filter(id=request.user.company.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
