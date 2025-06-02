from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ACCOUNT_TYPE_CHOICES = [
        ('ttgroup', 'TTGroup Account'),
        ('system', 'System Account'),
    ]
    
    ROLE_CHOICES = [
        ('admin_corporation', 'Admin Tập đoàn'),
        ('admin_company', 'Admin Công ty'),
        ('manager', 'Nhân viên quản lý'),
    ]
    
    account_type = models.CharField(
        max_length=20, 
        choices=ACCOUNT_TYPE_CHOICES,
        verbose_name="Loại tài khoản"
    )
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES,
        verbose_name="Vai trò"
    )
    company = models.ForeignKey(
        'companies.Company', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Công ty"
    )
    ldap_dn = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name="LDAP DN"
    )
    phone = models.CharField(
        max_length=15, 
        blank=True,
        verbose_name="Số điện thoại"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def has_corporation_permission(self):
        return self.role == 'admin_corporation'
    
    def has_company_permission(self):
        return self.role in ['admin_corporation', 'admin_company']
    
    def can_lookup_employee(self, employee=None):
        """Kiểm tra quyền tra cứu thông tin nhân viên - cho phép cross-company"""
        # Tất cả user đã đăng nhập đều có thể tra cứu thông tin nhân viên
        return self.is_authenticated
    
    def can_manage_employee(self, employee):
        """Kiểm tra quyền quản lý (CRUD) nhân viên - chỉ trong công ty"""
        if self.role == 'admin_corporation':
            return True
        elif self.role == 'admin_company':
            return employee.company == self.company
        return False  # Manager không có quyền manage
    
    def save(self, *args, **kwargs):
        # Auto set is_staff based on role
        if self.role in ['admin_corporation', 'admin_company']:
            self.is_staff = True
        else:
            # Giữ nguyên is_staff nếu không phải admin (để không ảnh hưởng superuser)
            if not self.is_superuser:
                self.is_staff = False
        super().save(*args, **kwargs)

class LDAPUserPermission(models.Model):
    """Model để quản lý quyền truy cập cho LDAP users"""
    username = models.CharField(max_length=150, unique=True, verbose_name="Username LDAP")
    role = models.CharField(
        max_length=20, 
        choices=CustomUser.ROLE_CHOICES,
        verbose_name="Vai trò"
    )
    company = models.ForeignKey(
        'companies.Company', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Công ty"
    )
    is_allowed = models.BooleanField(default=True, verbose_name="Được phép truy cập")
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Được tạo bởi"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Quyền LDAP User"
        verbose_name_plural = "Quyền LDAP Users"
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
