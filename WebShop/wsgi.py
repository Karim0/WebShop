"""
WSGI config for WebShop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

# import os, sys
#
# # add the hellodjango project path into the sys.path
# sys.path.append('<PATH_TO_MY_DJANGO_PROJECT>/WebShop')
#
# # add the virtualenv site-packages path to the sys.path
# sys.path.append('<PATH_TO_VIRTUALENV>/Lib/site-packages')
#
# # poiting to the project settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebShop.settings")
#
#
# from django.core.wsgi import get_wsgi_application
#
#
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebShop.settings')
#
# application = get_wsgi_application()

import os
import django

from django.core.handlers.wsgi import WSGIHandler


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eisentask.settings.production")
django.setup(set_prefix=False)

application = WSGIHandler()