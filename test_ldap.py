import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_lookup.settings')
django.setup()

from django.contrib.auth import authenticate

# Test system account
print("Testing system account...")
user = authenticate(username='admin.ttgroup', password='TTGroup@2024', account_type='system')
print(f"System auth result: {user}")

# Test LDAP (chỉ nếu trong mạng TTGroup)
print("\nTesting LDAP...")
try:
    # Thay 'your_ldap_username' bằng username LDAP thật của bạn
    user = authenticate(username='dangnh4', password='Tony@1234', account_type='ttgroup')
    print(f"LDAP auth result: {user}")
except Exception as e:
    print(f"LDAP error: {e}")
