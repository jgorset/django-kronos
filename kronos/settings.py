import os
import sys

from django.conf import settings

KRONOS_PYTHON = getattr(settings, 'KRONOS_PYTHON', sys.executable)
KRONOS_MANAGE = getattr(settings, 'KRONOS_MANAGE', '%s/manage.py' % os.getcwd())
KRONOS_PYTHONPATH = getattr(settings, 'KRONOS_PYTHONPATH', None)
try:
    PROJECT_MODULE = sys.modules['.'.join(settings.SETTINGS_MODULE.split('.')[:-1])]
except KeyError:
    PROJECT_MODULE = None
KRONOS_POSTFIX = getattr(settings, 'KRONOS_POSTFIX', '')
KRONOS_PREFIX = getattr(settings, 'KRONOS_PREFIX', '')
