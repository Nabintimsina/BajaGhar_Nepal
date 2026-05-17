import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'nepali_platform.settings_production'))
django.setup()

from django.contrib.auth.models import User

admin_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', os.environ.get('BRANDING_CONTACT_EMAIL', 'admin@bajanepal.com'))
admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123').strip()

if not admin_password:
    raise SystemExit('DJANGO_SUPERUSER_PASSWORD must be set before creating the admin user.')

if not User.objects.filter(username=admin_username).exists():
    User.objects.create_superuser(
        username=admin_username,
        email=admin_email,
        password=admin_password,
    )
    print(f'Superuser created: {admin_username}')
else:
    print(f"Superuser '{admin_username}' already exists")
