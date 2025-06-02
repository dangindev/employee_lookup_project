from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from authentication.models import CustomUser
from employees.models import Employee, PurchaseHistory, AuditLog
from companies.models import Company

class Command(BaseCommand):
    help = 'Setup groups và permissions cho hệ thống'
    
    def handle(self, *args, **options):
        self.create_groups_and_permissions()
        self.stdout.write(self.style.SUCCESS('Đã setup groups và permissions thành công!'))
    
    def create_groups_and_permissions(self):
        # Tạo custom permissions
        self.create_custom_permissions()
        
        # Tạo groups và gán permissions
        self.create_admin_corporation_group()
        self.create_admin_company_group()
        self.create_manager_group()
    
    def create_custom_permissions(self):
        """Tạo custom permissions"""
        # Employee permissions
        employee_ct = ContentType.objects.get_for_model(Employee)
        purchase_ct = ContentType.objects.get_for_model(PurchaseHistory)
        audit_ct = ContentType.objects.get_for_model(AuditLog)
        user_ct = ContentType.objects.get_for_model(CustomUser)
        company_ct = ContentType.objects.get_for_model(Company)
        
        # Custom permissions cho company-specific access
        custom_permissions = [
            ('view_company_employees', 'Can view company employees', employee_ct),
            ('change_company_employees', 'Can change company employees', employee_ct),
            ('add_company_employees', 'Can add company employees', employee_ct),
            ('delete_company_employees', 'Can delete company employees', employee_ct),
            
            ('view_company_purchases', 'Can view company purchase history', purchase_ct),
            ('change_company_purchases', 'Can change company purchase history', purchase_ct),
            ('add_company_purchases', 'Can add company purchase history', purchase_ct),
            ('delete_company_purchases', 'Can delete company purchase history', purchase_ct),
            
            ('view_company_audit', 'Can view company audit logs', audit_ct),
            ('manage_ldap_users', 'Can manage LDAP users', user_ct),
        ]
        
        for codename, name, content_type in custom_permissions:
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={'name': name}
            )
            if created:
                self.stdout.write(f'✓ Tạo permission: {name}')
    
    def create_admin_corporation_group(self):
        """Tạo group Admin Tập đoàn với full permissions"""
        group, created = Group.objects.get_or_create(name='Admin Tập đoàn')
        
        if created:
            self.stdout.write('✓ Tạo group: Admin Tập đoàn')
        
        # Admin tập đoàn có tất cả permissions
        all_permissions = Permission.objects.all()
        group.permissions.set(all_permissions)
        
        self.stdout.write(f'✓ Gán {all_permissions.count()} permissions cho Admin Tập đoàn')
    
    def create_admin_company_group(self):
        """Tạo group Admin Công ty với permissions hạn chế"""
        group, created = Group.objects.get_or_create(name='Admin Công ty')
        
        if created:
            self.stdout.write('✓ Tạo group: Admin Công ty')
        
        # Permissions cho admin công ty
        permission_codenames = [
            # Employee permissions
            'view_employee', 'add_employee', 'change_employee', 'delete_employee',
            'view_company_employees', 'add_company_employees', 'change_company_employees', 'delete_company_employees',
            
            # Purchase history permissions
            'view_purchasehistory', 'add_purchasehistory', 'change_purchasehistory', 'delete_purchasehistory',
            'view_company_purchases', 'add_company_purchases', 'change_company_purchases', 'delete_company_purchases',
            
            # Audit log view only
            'view_auditlog', 'view_company_audit',
            
            # LDAP user management
            'view_ldapuserpermission', 'add_ldapuserpermission', 'change_ldapuserpermission',
            'manage_ldap_users',
            
            # Company view
            'view_company',
            
            # Basic user permissions
            'view_customuser',
        ]
        
        permissions = Permission.objects.filter(codename__in=permission_codenames)
        group.permissions.set(permissions)
        
        self.stdout.write(f'✓ Gán {permissions.count()} permissions cho Admin Công ty')
    
    def create_manager_group(self):
        """Tạo group Nhân viên quản lý chỉ với quyền xem"""
        group, created = Group.objects.get_or_create(name='Nhân viên quản lý')
        
        if created:
            self.stdout.write('✓ Tạo group: Nhân viên quản lý')
        
        # Chỉ có quyền view
        permission_codenames = [
            'view_employee',
            'view_company_employees', 
            'view_purchasehistory',
            'view_company_purchases',
            'view_auditlog',
            'view_company_audit',
        ]
        
        permissions = Permission.objects.filter(codename__in=permission_codenames)
        group.permissions.set(permissions)
        
        self.stdout.write(f'✓ Gán {permissions.count()} permissions cho Nhân viên quản lý')
