# companies/admin.py
from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'phone', 'email', 'is_active', 'get_active_employees_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'email']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('code', 'name')
        }),
        ('Thông tin liên hệ', {
            'fields': ('address', 'phone', 'email')
        }),
        ('Trạng thái', {
            'fields': ('is_active',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'admin_company':
            return qs.filter(id=request.user.company.id)
        return qs
    
    def has_add_permission(self, request):
        return hasattr(request.user, 'role') and request.user.role == 'admin_corporation'
    
    def has_change_permission(self, request, obj=None):
        if hasattr(request.user, 'role'):
            if request.user.role == 'admin_corporation':
                return True
            elif request.user.role == 'admin_company':
                return obj and obj == request.user.company
        return False
    
    def has_delete_permission(self, request, obj=None):
        return hasattr(request.user, 'role') and request.user.role == 'admin_corporation'