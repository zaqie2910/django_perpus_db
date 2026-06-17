import os
import sys

# Jalur ke folder project kamu (sesuai nama dari GitHub)
path = '/home/zaqie/django_perpus_db'
if path not in sys.path:
    sys.path.append(path)

# Mengarahkan ke settings.py di dalam folder webperpus
os.environ['DJANGO_SETTINGS_MODULE'] = 'webperpus.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()