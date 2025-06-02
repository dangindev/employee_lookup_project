from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Cập nhật quyền staff cho admin công ty'
    
    def handle(self, *args, **options):
        # Cập nhật tất cả admin công ty có quyền staff
        admin_companies = User.objects.filter(role='admin_company')
        
        for admin in admin_companies:
            admin.is_staff = True
            admin.save()
            self.stdout.write(f'Cập nhật quyền staff cho: {admin.username}')
        
        self.stdout.write(self.style.SUCCESS(f'Đã cập nhật {admin_companies.count()} admin công ty'))
