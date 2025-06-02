

| Username | Password | Role | Company | Account Type |
|----------|----------|------|---------|--------------|
| `admin.ttgroup` | `TTGroup@2024` | Admin Tập đoàn | - | System Account |
| `admin.ho` | `TTGroup@2024` | Admin Công ty | TTG-HO | System Account |
| `admin.hcm` | `TTGroup@2024` | Admin Công ty | TTC-HCM | System Account |
| `admin.danang` | `TTGroup@2024` | Admin Công ty | TTT-DN | System Account |
| `admin.finance` | `TTGroup@2024` | Admin Công ty | TTF-HN | System Account |
| `admin.company.test` | `TTGroup@2024` | Admin Công ty | TTG-HO | System Account |
| `manager.ho` | `TTGroup@2024` | Nhân viên quản lý | TTG-HO | System Account |
| `manager.hcm` | `TTGroup@2024` | Nhân viên quản lý | TTC-HCM | System Account |
| `manager.test` | `TTGroup@2024` | Nhân viên quản lý | TTG-HO | System Account |

## Test với admin.danang:

1. **URL**: `http://127.0.0.1:8000/auth/login/`
2. **Thông tin đăng nhập**:
   - Account Type: **System Account**
   - Username: `admin.danang`
   - Password: `TTGroup@2024`
3. **Quyền hạn**: 
   - Quản lý nhân viên của công ty TTT-DN (Đà Nẵng)
   - Tạo LDAP users cho công ty TTT-DN
   - Tra cứu cross-company tất cả nhân viên

Nếu user này chưa được tạo, bạn có thể chạy lại:

```bash
python manage.py create_sample_data
```

Hoặc tạo manual nhanh:

```bash
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_lookup.settings')
django.setup()

from django.contrib.auth import get_user_model
from companies.models import Company

User = get_user_model()
company = Company.objects.filter(code='TTT-DN').first()

if company:
    admin_dn, created = User.objects.get_or_create(
        username='admin.danang',
        defaults={
            'email': 'admin.danang@ttgroup.com.vn',
            'first_name': 'Admin',
            'last_name': 'Đà Nẵng',
            'account_type': 'system',
            'role': 'admin_company',
            'company': company,
            'is_active': True,
        }
    )
    
    admin_dn.set_password('TTGroup@2024')
    admin_dn.save()
    print(f'✓ Admin Đà Nẵng: admin.danang / TTGroup@2024')
    print(f'Company: {admin_dn.company.name}')
else:
    print('Công ty TTT-DN chưa có, chạy create_sample_data trước')
"
```

Mật khẩu thống nhất: **TTGroup@2024** cho tất cả system accounts! 🚀