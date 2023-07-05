"""
WSGI config for personal_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from jobs.updater import start

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personal_site.settings")

if not os.getenv('DEBUG', '0').lower() in ['true', 't', '1']:
    start()

application = get_wsgi_application()
