from django.core.management.base import BaseCommand
from django.conf import settings
from decouple import config

class Command(BaseCommand):
    help = 'Test LDAP configuration từ .env'
    
    def handle(self, *args, **options):
        self.stdout.write('=== LDAP Configuration Test ===')
        
        # Kiểm tra LDAP có enabled không
        ldap_enabled = config('LDAP_ENABLED', default=False, cast=bool)
        self.stdout.write(f'LDAP Enabled: {ldap_enabled}')
        
        if not ldap_enabled:
            self.stdout.write(self.style.WARNING('LDAP is disabled in .env'))
            return
        
        # Kiểm tra các config LDAP
        ldap_configs = [
            ('LDAP_SERVER_URI', config('LDAP_SERVER_URI', default='')),
            ('LDAP_BIND_DN', config('LDAP_BIND_DN', default='')),
            ('LDAP_BIND_PASSWORD', '***' if config('LDAP_BIND_PASSWORD', default='') else 'EMPTY'),
            ('LDAP_USER_SEARCH_BASE', config('LDAP_USER_SEARCH_BASE', default='')),
            ('LDAP_GROUP_SEARCH_BASE', config('LDAP_GROUP_SEARCH_BASE', default='')),
        ]
        
        for key, value in ldap_configs:
            status = '✓' if value and value != 'EMPTY' else '✗'
            self.stdout.write(f'{status} {key}: {value}')
        
        # Test LDAP connection
        try:
            import ldap
            server_uri = config('LDAP_SERVER_URI', default='')
            if server_uri:
                self.stdout.write('\n--- Testing LDAP Connection ---')
                conn = ldap.initialize(server_uri)
                conn.set_option(ldap.OPT_REFERRALS, 0)
                conn.set_option(ldap.OPT_NETWORK_TIMEOUT, 5)
                
                bind_dn = config('LDAP_BIND_DN', default='')
                bind_password = config('LDAP_BIND_PASSWORD', default='')
                
                conn.simple_bind_s(bind_dn, bind_password)
                self.stdout.write(self.style.SUCCESS('✓ LDAP connection successful'))
                conn.unbind_s()
            else:
                self.stdout.write(self.style.WARNING('No LDAP_SERVER_URI configured'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ LDAP connection failed: {str(e)}'))
        
        # Kiểm tra authentication backends
        self.stdout.write('\n--- Authentication Backends ---')
        for backend in settings.AUTHENTICATION_BACKENDS:
            self.stdout.write(f'• {backend}')
