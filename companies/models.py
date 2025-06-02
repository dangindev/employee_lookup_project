# companies/models.py
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên công ty")
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã công ty")
    address = models.TextField(blank=True, verbose_name="Địa chỉ")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Điện thoại")
    email = models.EmailField(blank=True, verbose_name="Email")
    is_active = models.BooleanField(default=True, verbose_name="Hoạt động")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Công ty"
        verbose_name_plural = "Công ty"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_active_employees_count(self):
        return self.employee_set.filter(is_active=True).count()