from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from authentication.models import LDAPUserPermission
from companies.models import Company

User = get_user_model()

class Command(BaseCommand):
    help = 'Thêm LDAP users được phép truy cập hệ thống'
    
    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='LDAP username')
        parser.add_argument('--role', type=str, choices=['admin_corporation', 'admin_company', 'manager'], default='manager', help='User role')
        parser.add_argument('--company-code', type=str, help='Company code (required for admin_company and manager)')
        parser.add_argument('--create-sample', action='store_true', help='Create sample LDAP users')
    
    def handle(self, *args, **options):
        if options['create_sample']:
            self.create_sample_ldap_users()
        elif options['username']:
            self.add_single_user(options)
        else:
            self.stdout.write('Vui lòng cung cấp --username hoặc --create-sample')
    
    def add_single_user(self, options):
        username = options['username']
        role = options['role']
        company_code = options.get('company_code')
        
        company = None
        if company_code:
            try:
                company = Company.objects.get(code=company_code)
            except Company.DoesNotExist:
                self.stdout.write(f'Công ty với mã {company_code} không tồn tại')
                return
        
        ldap_perm, created = LDAPUserPermission.objects.get_or_create(
            username=username,
            defaults={
                'role': role,
                'company': company,
                'is_allowed': True
            }
        )
        
        if created:
            self.stdout.write(f'Đã thêm LDAP user: {username} với role {role}')
        else:
            self.stdout.write(f'LDAP user {username} đã tồn tại')
    
    def create_sample_ldap_users(self):
        """Tạo một số LDAP users mẫu"""
        companies = Company.objects.all()
        if not companies:
            self.stdout.write('Chưa có công ty nào. Vui lòng tạo dữ liệu mẫu trước.')
            return
        
        sample_users = [
            # Admin tập đoàn (có thể truy cập tất cả)
            {'username': 'admin.ldap', 'role': 'admin_corporation', 'company': None},
            
            # Admin công ty
            {'username': 'admin.ho.ldap', 'role': 'admin_company', 'company': companies.filter(code='TTG-HO').first()},
            {'username': 'admin.hcm.ldap', 'role': 'admin_company', 'company': companies.filter(code='TTC-HCM').first()},
            
            # Nhân viên quản lý
            {'username': 'manager.ho.ldap', 'role': 'manager', 'company': companies.filter(code='TTG-HO').first()},
            {'username': 'manager.hcm.ldap', 'role': 'manager', 'company': companies.filter(code='TTC-HCM').first()},
            
            # Thêm username LDAP thật của bạn (thay đổi theo username thật)
            {'username': 'adminttg', 'role': 'admin_corporation', 'company': None},
        ]
 
        for user_data in sample_users:
            ldap_perm, created = LDAPUserPermission.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'role': user_data['role'],
                    'company': user_data['company'],
                    'is_allowed': True
                }
            )
            
            if created:
                company_name = user_data['company'].name if user_data['company'] else 'Tất cả'
                self.stdout.write(f'Thêm LDAP user: {user_data["username"]} - {user_data["role"]} - {company_name}')
        
        self.stdout.write(self.style.SUCCESS('Đã tạo sample LDAP users thành công!'))
        self.stdout.write('=== LDAP USERS CÓ THỂ ĐĂNG NHẬP ===')
        for perm in LDAPUserPermission.objects.filter(is_allowed=True):
            company_name = perm.company.name if perm.company else 'Tất cả công ty'
            self.stdout.write(f'{perm.username} - {perm.get_role_display()} - {company_name}')
