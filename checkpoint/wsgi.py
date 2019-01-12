"""
WSGI config for checkpoint project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from camera.Camera import Camera

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkpoint.settings')

camera = Camera()
application = get_wsgi_application()
