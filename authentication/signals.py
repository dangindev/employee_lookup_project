from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser

@receiver(pre_save, sender=CustomUser)
def clear_user_groups_on_role_change(sender, instance, **kwargs):
    """Clear groups khi role thay đổi"""
    if instance.pk:  # Chỉ khi update, không phải create
        try:
            old_instance = CustomUser.objects.get(pk=instance.pk)
            if old_instance.role != instance.role:
                # Role thay đổi, clear all groups
                instance._clear_groups = True
        except CustomUser.DoesNotExist:
            pass

@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    """Tự động gán user vào group tương ứng với role"""
    
    # Clear groups nếu role thay đổi
    if hasattr(instance, '_clear_groups'):
        instance.groups.clear()
        delattr(instance, '_clear_groups')
    
    # Mapping role -> group name
    role_group_mapping = {
        'admin_corporation': 'Admin Tập đoàn',
        'admin_company': 'Admin Công ty', 
        'manager': 'Nhân viên quản lý',
    }
    
    group_name = role_group_mapping.get(instance.role)
    if group_name:
        try:
            group = Group.objects.get(name=group_name)
            instance.groups.add(group)
            
            # Set is_staff cho admin roles
            if instance.role in ['admin_corporation', 'admin_company']:
                if not instance.is_staff:
                    CustomUser.objects.filter(pk=instance.pk).update(is_staff=True)
            else:
                # Manager không có quyền staff (trừ superuser)
                if instance.is_staff and not instance.is_superuser:
                    CustomUser.objects.filter(pk=instance.pk).update(is_staff=False)
                    
        except Group.DoesNotExist:
            print(f"Group '{group_name}' không tồn tại. Chạy command setup_permissions trước.")
