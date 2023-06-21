"""
WSGI config for fintly project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import newrelic.agent
newrelic.agent.initialize(r"C:\Users\jjaco\Google Drive\Coding\Django\Projects\fintly_project\newrelic.ini")
newrelic.agent.register_application()
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fintly.settings')

application = get_wsgi_application()
