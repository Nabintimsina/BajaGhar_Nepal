import os
import sys
from pathlib import Path

project_home = Path(__file__).resolve().parent
if str(project_home) not in sys.path:
    sys.path.insert(0, str(project_home))

settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
if not settings_module:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'nepali_platform.settings_production'

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
