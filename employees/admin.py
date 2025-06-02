from django.contrib import admin
from .models import Employee, PurchaseHistory, AuditLog

class PurchaseHistoryInline(admin.TabularInline):
    model = PurchaseHistory
    extra = 0
    readonly_fields = ['total_amount']
    fields = ['product_name', 'product_code', 'purchase_date', 'quantity', 'unit_price', 'total_amount', 'description']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['cccd', 'full_name', 'birth_date', 'company', 'position', 'is_active']
    list_filter = ['company', 'gender', 'is_active', 'created_at']
    search_fields = ['cccd', 'full_name', 'employee_id', 'phone', 'email']
    list_per_page = 50
    inlines = [PurchaseHistoryInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('cccd', 'full_name', 'birth_date', 'gender', 'phone', 'email')
        }),
        ('Thông tin công việc', {
            'fields': ('company', 'employee_id', 'position', 'department', 'hire_date')
        }),
        ('Địa chỉ', {
            'fields': ('address',)
        }),
        ('Trạng thái', {
            'fields': ('is_active',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Admin interface: chỉ quản lý nhân viên của công ty mình (trừ admin tập đoàn)
        if hasattr(request.user, 'role') and request.user.role == 'admin_company':
            return qs.filter(company=request.user.company)
        return qs
    
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        # Kiểm tra quyền manage
        return request.user.can_manage_employee(obj)
    
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return super().has_delete_permission(request, obj)
        # Kiểm tra quyền manage
        return request.user.can_manage_employee(obj)

@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ['employee', 'product_name', 'purchase_date', 'quantity', 'total_amount']
    list_filter = ['purchase_date', 'employee__company']
    search_fields = ['employee__full_name', 'employee__cccd', 'product_name', 'order_number']
    date_hierarchy = 'purchase_date'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'admin_company':
            # Admin công ty chỉ thấy lịch sử mua hàng của nhân viên công ty mình
            return qs.filter(employee__company=request.user.company)
        return qs

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'target_cccd', 'get_cross_company_info', 'ip_address', 'timestamp']
    list_filter = ['action', 'timestamp', 'user__company']
    search_fields = ['user__username', 'target_cccd', 'ip_address']
    readonly_fields = ['user', 'action', 'target_cccd', 'target_employee', 'ip_address', 'user_agent', 'timestamp', 'details']
    date_hierarchy = 'timestamp'
    
    def get_cross_company_info(self, obj):
        """Hiển thị thông tin cross-company lookup"""
        if obj.details and isinstance(obj.details, dict):
            if obj.details.get('cross_company'):
                return f"Cross-company: {obj.details.get('user_company', 'Unknown')} → {obj.details.get('target_company', 'Unknown')}"
            elif obj.details.get('status') == 'success':
                return "Same company"
        return "-"
    get_cross_company_info.short_description = "Cross-company"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'admin_company':
            # Admin công ty thấy audit log của users công ty mình + cross-company lookups
            return qs.filter(
                Q(user__company=request.user.company) |  # Users của công ty mình
                Q(target_employee__company=request.user.company)  # Nhân viên công ty mình được tra cứu
            )
        return qs
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return hasattr(request.user, 'role') and request.user.role == 'admin_corporation'
