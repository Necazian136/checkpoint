"""
WSGI config for checkpoint project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from modules.Vision import Vision

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkpoint.settings')

vision = Vision()
application = get_wsgi_application()
