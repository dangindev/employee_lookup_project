# Employee Lookup System

![Django](https://img.shields.io/badge/Django-4.2.7-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue)
![Python](https://img.shields.io/badge/Python-3.12-yellow)
![LDAP](https://img.shields.io/badge/LDAP-Enabled-orange)

Hệ thống tra cứu thông tin nhân viên tích hợp với LDAP của TTGroup, cho phép quản lý và tra cứu thông tin nhân viên một cách hiệu quả.

## 🌟 Tính năng chính

- 🔐 Xác thực đa dạng:
  - Tích hợp LDAP với TTGroup
  - Hệ thống tài khoản nội bộ
  - Phân quyền chi tiết theo vai trò

- 👥 Quản lý nhân viên:
  - Thông tin cá nhân
  - Lịch sử công tác
  - Quản lý theo công ty

- 🔍 Tra cứu thông tin:
  - Tìm kiếm nâng cao
  - Lọc theo nhiều tiêu chí
  - Xuất báo cáo

## 🛠 Công nghệ sử dụng

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL
- **Authentication**: 
  - django-auth-ldap
  - Custom authentication system
- **Frontend**: 
  - Bootstrap 5
  - Crispy Forms
- **Development Tools**:
  - django-extensions
  - python-decouple

## 📋 Yêu cầu hệ thống

- Python 3.12+
- PostgreSQL 13+
- LDAP Server (TTGroup)
- Virtual Environment

## 🚀 Cài đặt

1. Clone repository:
```bash
git clone [repository-url]
cd employee_lookup_project
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv employee_lookup_env
source employee_lookup_env/bin/activate  # Linux/Mac
# hoặc
employee_lookup_env\Scripts\activate  # Windows
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

4. Tạo file .env từ mẫu:
```bash
cp .env.example .env
```

5. Cấu hình các biến môi trường trong file .env:
```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Database
DATABASE_NAME=employee_lookup
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# LDAP Configuration
LDAP_ENABLED=True
LDAP_SERVER_URI=ldap://your-ldap-server
LDAP_BIND_DN=your-bind-dn
LDAP_BIND_PASSWORD=your-bind-password
LDAP_USER_SEARCH_BASE=your-search-base
```

6. Tạo database:
```bash
createdb employee_lookup
```

7. Chạy migrations:
```bash
python manage.py migrate
```

8. Tạo superuser:
```bash
python manage.py createsuperuser
```

9. Chạy development server:
```bash
python manage.py runserver
```

## 🔧 Cấu hình LDAP

Hệ thống hỗ trợ xác thực qua LDAP của TTGroup. Để cấu hình:

1. Đảm bảo `LDAP_ENABLED=True` trong file .env
2. Cấu hình các thông số LDAP:
   - LDAP_SERVER_URI
   - LDAP_BIND_DN
   - LDAP_BIND_PASSWORD
   - LDAP_USER_SEARCH_BASE

3. Kiểm tra cấu hình LDAP:
```bash
python manage.py test_ldap_config
```

## 👥 Quản lý người dùng

### Loại tài khoản

1. **System Account**:
   - Tài khoản nội bộ
   - Quản lý bởi admin
   - Không phụ thuộc LDAP

2. **LDAP Account**:
   - Tài khoản TTGroup
   - Xác thực qua LDAP
   - Cần được cấp quyền trong hệ thống

### Phân quyền

- **Admin**: Quản lý toàn bộ hệ thống
- **Manager**: Quản lý nhân viên và thông tin công ty
- **User**: Xem và tra cứu thông tin

## 📝 Sử dụng

1. Đăng nhập:
   - System Account: username/password
   - LDAP Account: TTGroup credentials

2. Tra cứu thông tin:
   - Sử dụng thanh tìm kiếm
   - Lọc theo tiêu chí
   - Xuất báo cáo

3. Quản lý:
   - Thêm/sửa/xóa nhân viên
   - Quản lý công ty
   - Cấp quyền LDAP

## 🔍 Kiểm tra

1. Test LDAP connection:
```bash
python test_ldap.py
```

2. Test system account:
```bash
python manage.py test
```

## 📚 Tài liệu tham khảo

- [Django Documentation](https://docs.djangoproject.com/)
- [django-auth-ldap Documentation](https://django-auth-ldap.readthedocs.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:

1. Fork repository
2. Tạo branch mới
3. Commit changes
4. Push lên branch
5. Tạo Pull Request

## 📄 License

Project này được phát hành dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## 👥 Tác giả

- TTGroup IT Team

## 📞 Hỗ trợ

Nếu bạn gặp vấn đề hoặc cần hỗ trợ, vui lòng:

1. Kiểm tra [Issues](https://github.com/dangindev/employee_lookup_project/issues)
2. Tạo issue mới nếu cần
3. Liên hệ IT Support Team 