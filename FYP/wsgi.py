"""
WSGI config for FYP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FYP.settings')

application = get_wsgi_application()
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(application)

application = get_wsgi_application()
