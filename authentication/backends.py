from django.contrib.auth.backends import ModelBackend
from django_auth_ldap.backend import LDAPBackend
from django.contrib.auth import get_user_model
from django.db import transaction
import logging

User = get_user_model()
logger = logging.getLogger('django_auth_ldap')

class CustomLDAPBackend(LDAPBackend):
    """Custom LDAP backend for TTGroup accounts"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Chỉ xử lý TTGroup accounts
        if kwargs.get('account_type') != 'ttgroup':
            return None
        
        try:
            # Kiểm tra xem user có được phép truy cập không
            from authentication.models import LDAPUserPermission
            
            try:
                ldap_permission = LDAPUserPermission.objects.get(username=username)
                if not ldap_permission.is_allowed:
                    logger.warning(f'LDAP user {username} is not allowed to access')
                    return None
            except LDAPUserPermission.DoesNotExist:
                logger.warning(f'LDAP user {username} not found in permission list')
                return None
            
            # Gọi parent authenticate
            user = super().authenticate(request, username, password, **kwargs)
            
            if user:
                with transaction.atomic():
                    # Set account type
                    user.account_type = 'ttgroup'
                    
                    # Get LDAP DN if available
                    if hasattr(user, 'ldap_user') and user.ldap_user:
                        user.ldap_dn = user.ldap_user.dn
                    
                    # Set role và company từ LDAPUserPermission
                    user.role = ldap_permission.role
                    user.company = ldap_permission.company
                    
                    # Ensure user is active
                    user.is_active = True
                    user.save()
                    
                logger.info(f'LDAP authentication successful for user: {username} with role: {user.role}')
                
            return user
            
        except Exception as e:
            logger.error(f'LDAP authentication error for user {username}: {str(e)}')
            return None

class SystemAccountBackend(ModelBackend):
    """Custom backend for system accounts"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Chỉ xử lý System accounts
        if kwargs.get('account_type') != 'system':
            return None
            
        try:
            user = User.objects.get(username=username, account_type='system')
            if user.check_password(password) and user.is_active:
                logger.info(f'System account authentication successful for user: {username}')
                return user
        except User.DoesNotExist:
            logger.warning(f'System account not found: {username}')
            return None
        except Exception as e:
            logger.error(f'System account authentication error for user {username}: {str(e)}')
            return None
        
        return None
