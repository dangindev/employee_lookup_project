from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from companies.models import Company
from employees.models import Employee, PurchaseHistory
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho hệ thống TTGroup'
    
    def handle(self, *args, **options):
        self.stdout.write('Đang tạo dữ liệu mẫu cho TTGroup...')
        
        # Tạo công ty
        companies_data = [
            {'code': 'TTG-HO', 'name': 'Tập đoàn TT Group - Hội sở', 'address': 'Tầng 10, Tòa nhà Lotte Center, 54 Liễu Giai, Ba Đình, Hà Nội', 'phone': '024.3333.4444'},
            {'code': 'TTC-HCM', 'name': 'Công ty TNHH TT Construction - Chi nhánh TP.HCM', 'address': 'Tầng 5, Tòa nhà Bitexco, TP.HCM', 'phone': '028.3333.5555'},
            {'code': 'TTT-DN', 'name': 'Công ty CP TT Technology - Chi nhánh Đà Nẵng', 'address': 'Tầng 3, Tòa nhà Indochina, Đà Nẵng', 'phone': '0236.3333.6666'},
            {'code': 'TTF-HN', 'name': 'Công ty CP TT Finance - Hà Nội', 'address': 'Tầng 8, Tòa nhà Diamond Flower, Hà Nội', 'phone': '024.3333.7777'},
        ]
        
        companies = []
        for comp_data in companies_data:
            company, created = Company.objects.get_or_create(
                code=comp_data['code'],
                defaults=comp_data
            )
            companies.append(company)
            if created:
                self.stdout.write(f'Tạo công ty: {company.name}')
        
        # Tạo admin accounts
        # Admin tập đoàn
        admin_corp, created = User.objects.get_or_create(
            username='admin.ttgroup',
            defaults={
                'email': 'admin@ttgroup.com.vn',
                'first_name': 'Admin',
                'last_name': 'TTGroup',
                'account_type': 'system',
                'role': 'admin_corporation',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_corp.set_password('TTGroup@2024')
            admin_corp.save()
            self.stdout.write('Tạo Admin Tập đoàn: admin.ttgroup / TTGroup@2024')
        
        # Admin từng công ty
        admin_accounts = [
            {'username': 'admin.ho', 'company': companies[0], 'name': 'Admin Hội sở'},
            {'username': 'admin.hcm', 'company': companies[1], 'name': 'Admin TP.HCM'},
            {'username': 'admin.danang', 'company': companies[2], 'name': 'Admin Đà Nẵng'},
            {'username': 'admin.finance', 'company': companies[3], 'name': 'Admin Finance'},
        ]
        
        for admin_data in admin_accounts:
            admin_user, created = User.objects.get_or_create(
                username=admin_data['username'],
                defaults={
                    'email': f"{admin_data['username']}@ttgroup.com.vn",
                    'first_name': 'Admin',
                    'last_name': admin_data['name'],
                    'account_type': 'system',
                    'role': 'admin_company',
                    'company': admin_data['company'],
                    'is_staff': True
                }
            )
            if created:
                admin_user.set_password('TTGroup@2024')
                admin_user.save()
                self.stdout.write(f'Tạo {admin_data["name"]}: {admin_data["username"]} / TTGroup@2024')
        
        # Tạo nhân viên quản lý
        manager_accounts = [
            {'username': 'manager.ho', 'company': companies[0], 'name': 'Manager Hội sở'},
            {'username': 'manager.hcm', 'company': companies[1], 'name': 'Manager TP.HCM'},
        ]
        
        for manager_data in manager_accounts:
            manager_user, created = User.objects.get_or_create(
                username=manager_data['username'],
                defaults={
                    'email': f"{manager_data['username']}@ttgroup.com.vn",
                    'first_name': 'Manager',
                    'last_name': manager_data['name'],
                    'account_type': 'system',
                    'role': 'manager',
                    'company': manager_data['company'],
                    'is_staff': False
                }
            )
            if created:
                manager_user.set_password('TTGroup@2024')
                manager_user.save()
                self.stdout.write(f'Tạo {manager_data["name"]}: {manager_data["username"]} / TTGroup@2024')
        
        # Tạo nhân viên mẫu
        sample_employees = [
            {'cccd': '001234567890', 'name': 'Nguyễn Văn An', 'birth': '1990-01-15', 'gender': 'M', 'company': 0, 'position': 'Trưởng phòng IT', 'dept': 'Công nghệ thông tin'},
            {'cccd': '001234567891', 'name': 'Trần Thị Bình', 'birth': '1992-03-20', 'gender': 'F', 'company': 0, 'position': 'Nhân viên Kế toán', 'dept': 'Kế toán'},
            {'cccd': '001234567892', 'name': 'Lê Văn Cường', 'birth': '1988-07-10', 'gender': 'M', 'company': 1, 'position': 'Giám đốc dự án', 'dept': 'Xây dựng'},
            {'cccd': '001234567893', 'name': 'Phạm Thị Dung', 'birth': '1995-11-25', 'gender': 'F', 'company': 1, 'position': 'Kỹ sư xây dựng', 'dept': 'Kỹ thuật'},
            {'cccd': '001234567894', 'name': 'Hoàng Văn Em', 'birth': '1987-05-30', 'gender': 'M', 'company': 2, 'position': 'Tech Lead', 'dept': 'Phát triển phần mềm'},
            {'cccd': '001234567895', 'name': 'Ngô Thị Phượng', 'birth': '1993-09-18', 'gender': 'F', 'company': 2, 'position': 'Business Analyst', 'dept': 'Phân tích hệ thống'},
            {'cccd': '001234567896', 'name': 'Vũ Văn Giang', 'birth': '1985-12-08', 'gender': 'M', 'company': 3, 'position': 'Giám đốc tài chính', 'dept': 'Tài chính'},
            {'cccd': '001234567897', 'name': 'Đặng Thị Hoa', 'birth': '1991-06-14', 'gender': 'F', 'company': 3, 'position': 'Chuyên viên đầu tư', 'dept': 'Đầu tư'},
        ]
        
        for i, emp_data in enumerate(sample_employees):
            employee, created = Employee.objects.get_or_create(
                cccd=emp_data['cccd'],
                defaults={
                    'full_name': emp_data['name'],
                    'birth_date': emp_data['birth'],
                    'gender': emp_data['gender'],
                    'company': companies[emp_data['company']],
                    'employee_id': f'EMP{1000 + i}',
                    'position': emp_data['position'],
                    'department': emp_data['dept'],
                    'phone': f'09{random.randint(10000000, 99999999)}',
                    'email': f"{emp_data['name'].lower().replace(' ', '.').replace('ê', 'e').replace('â', 'a').replace('ư', 'u').replace('ơ', 'o').replace('ă', 'a').replace('ế', 'e').replace('ổ', 'o').replace('ó', 'o').replace('ờ', 'o').replace('ứ', 'u')}@ttgroup.com.vn",
                    'hire_date': date.today() - timedelta(days=random.randint(30, 1000)),
                    'address': f'Địa chỉ mẫu {i+1}, Quận {random.randint(1,12)}, Hà Nội'
                }
            )
            
            if created:
                self.stdout.write(f'Tạo nhân viên: {employee.full_name} - {employee.cccd}')
                
                # Tạo lịch sử mua hàng cho mỗi nhân viên
                products = [
                    'Laptop Dell Inspiron 15', 'Máy tính để bàn HP', 'Màn hình Samsung 24"',
                    'Bàn làm việc gỗ', 'Ghế văn phòng ergonomic', 'Điện thoại iPhone 14',
                    'Túi xách công sở', 'Áo sơ mi công sở', 'Giày da nam/nữ',
                    'Cà phê văn phòng', 'Nước uống', 'Văn phòng phẩm', 'Máy in Canon',
                    'USB Kingston 32GB', 'Tai nghe Sony', 'Bàn phím cơ', 'Chuột không dây'
                ]
                
                for j in range(random.randint(3, 10)):
                    product = random.choice(products)
                    quantity = random.randint(1, 5)
                    unit_price = random.randint(50000, 20000000)
                    
                    PurchaseHistory.objects.create(
                        employee=employee,
                        product_name=product,
                        product_code=f'SP{random.randint(1000, 9999)}',
                        purchase_date=date.today() - timedelta(days=random.randint(1, 365)),
                        quantity=quantity,
                        unit_price=unit_price,
                        total_amount=quantity * unit_price,
                        description=f'Mua {product} cho nhân viên {employee.full_name}',
                        order_number=f'ORD{random.randint(100000, 999999)}'
                    )
        
        self.stdout.write(self.style.SUCCESS('Đã tạo dữ liệu mẫu thành công!'))
        self.stdout.write('=== THÔNG TIN ĐĂNG NHẬP ===')
        self.stdout.write('Admin Tập đoàn: admin.ttgroup / TTGroup@2024')
        self.stdout.write('Admin Hội sở: admin.ho / TTGroup@2024')
        self.stdout.write('Admin TP.HCM: admin.hcm / TTGroup@2024')
        self.stdout.write('Admin Đà Nẵng: admin.danang / TTGroup@2024')
        self.stdout.write('Admin Finance: admin.finance / TTGroup@2024')
        self.stdout.write('Manager Hội sở: manager.ho / TTGroup@2024')
        self.stdout.write('Manager TP.HCM: manager.hcm / TTGroup@2024')
        self.stdout.write('=== CCCD TEST ===')
        for emp in sample_employees:
            self.stdout.write(f"{emp['cccd']} - {emp['name']}")
