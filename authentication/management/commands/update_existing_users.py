from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = 'Cập nhật permissions cho users hiện tại'
    
    def handle(self, *args, **options):
        # Mapping role -> group name
        role_group_mapping = {
            'admin_corporation': 'Admin Tập đoàn',
            'admin_company': 'Admin Công ty', 
            'manager': 'Nhân viên quản lý',
        }
        
        updated_count = 0
        
        for user in User.objects.all():
            if user.role in role_group_mapping:
                group_name = role_group_mapping[user.role]
                
                try:
                    group = Group.objects.get(name=group_name)
                    
                    # Clear existing groups
                    user.groups.clear()
                    
                    # Add to correct group
                    user.groups.add(group)
                    
                    # Update is_staff
                    if user.role in ['admin_corporation', 'admin_company']:
                        user.is_staff = True
                    else:
                        if not user.is_superuser:
                            user.is_staff = False
                    
                    user.save()
                    updated_count += 1
                    
                    self.stdout.write(f'✓ Cập nhật user: {user.username} -> {group_name}')
                    
                except Group.DoesNotExist:
                    self.stdout.write(f'✗ Group "{group_name}" không tồn tại')
        
        self.stdout.write(self.style.SUCCESS(f'Đã cập nhật {updated_count} users'))
