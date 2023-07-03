"""
WSGI config for personal_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from jobs import updater

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personal_site.settings")

updater.start()

application = get_wsgi_application()
