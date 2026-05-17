"""Production settings override - minimal, focused on HTTPS and security."""
from .settings import *


# Production Security Settings (overrides settings.py defaults)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


STATIC_URL = '/api/static/'
STATIC_ROOT = Path('/home1/bajanepa/public_html/api/static')
MEDIA_URL = '/api/media/'
MEDIA_ROOT = Path('/home1/bajanepa/public_html/api/media')
MEDIA_SYMLINK_PATH = '/home1/bajanepa/public_html/api/media'
MEDIA_TARGET_PATH = '/home1/bajanepa/bajanepal/backend/media'
