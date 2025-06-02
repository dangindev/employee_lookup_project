# employees/models.py
from django.db import models
from django.core.validators import RegexValidator

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Nam'),
        ('F', 'Nữ'),
    ]
    
    cccd = models.CharField(
        max_length=12, 
        unique=True, 
        verbose_name="Số CCCD",
        validators=[RegexValidator(r'^\d{12}$', 'CCCD phải có đúng 12 chữ số')]
    )
    full_name = models.CharField(max_length=255, verbose_name="Họ tên")
    birth_date = models.DateField(verbose_name="Ngày sinh")
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        verbose_name="Giới tính"
    )
    phone = models.CharField(max_length=15, blank=True, verbose_name="Điện thoại")
    email = models.EmailField(blank=True, verbose_name="Email")
    address = models.TextField(blank=True, verbose_name="Địa chỉ")
    company = models.ForeignKey(
        'companies.Company', 
        on_delete=models.CASCADE,
        verbose_name="Công ty"
    )
    employee_id = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name="Mã nhân viên"
    )
    position = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Chức vụ"
    )
    department = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Phòng ban"
    )
    hire_date = models.DateField(null=True, blank=True, verbose_name="Ngày vào làm")
    is_active = models.BooleanField(default=True, verbose_name="Hoạt động")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"
        ordering = ['full_name']
        indexes = [
            models.Index(fields=['cccd']),
            models.Index(fields=['company', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.full_name} ({self.cccd})"
    
    def get_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    def get_full_employee_id(self):
        return f"{self.company.code}-{self.employee_id}" if self.employee_id else ""

class PurchaseHistory(models.Model):
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='purchases',
        verbose_name="Nhân viên"
    )
    product_name = models.CharField(max_length=255, verbose_name="Tên sản phẩm")
    product_code = models.CharField(max_length=50, blank=True, verbose_name="Mã sản phẩm")
    purchase_date = models.DateField(verbose_name="Ngày mua")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    unit_price = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name="Đơn giá"
    )
    total_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name="Tổng tiền"
    )
    description = models.TextField(blank=True, verbose_name="Mô tả")
    order_number = models.CharField(max_length=50, blank=True, verbose_name="Số đơn hàng")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Lịch sử mua hàng"
        verbose_name_plural = "Lịch sử mua hàng"
        ordering = ['-purchase_date']
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.product_name} ({self.purchase_date})"
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('lookup', 'Tra cứu'),
        ('create', 'Tạo mới'),
        ('update', 'Cập nhật'),
        ('delete', 'Xóa'),
    ]
    
    user = models.ForeignKey(
        'authentication.CustomUser', 
        on_delete=models.CASCADE,
        verbose_name="Người dùng"
    )
    action = models.CharField(
        max_length=20, 
        choices=ACTION_CHOICES,
        verbose_name="Hành động"
    )
    target_cccd = models.CharField(max_length=12, verbose_name="CCCD được tra cứu")
    target_employee = models.ForeignKey(
        Employee, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Nhân viên"
    )
    ip_address = models.GenericIPAddressField(verbose_name="Địa chỉ IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian")
    details = models.JSONField(blank=True, null=True, verbose_name="Chi tiết")
    
    class Meta:
        verbose_name = "Nhật ký hệ thống"
        verbose_name_plural = "Nhật ký hệ thống"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.target_cccd}"