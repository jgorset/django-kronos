import os
import sys
import hashlib

from django.utils.encoding import smart_bytes
from django.conf import settings

KRONOS_PYTHON = getattr(settings, 'KRONOS_PYTHON', sys.executable)
KRONOS_MANAGE = getattr(settings, 'KRONOS_MANAGE', '%s/manage.py' % os.getcwd())
KRONOS_PYTHONPATH = getattr(settings, 'KRONOS_PYTHONPATH', None)
KRONOS_POSTFIX = getattr(settings, 'KRONOS_POSTFIX', '')
KRONOS_PREFIX = getattr(settings, 'KRONOS_PREFIX', '')

try:
    PROJECT_MODULE = \
        sys.modules['.'.join(settings.SETTINGS_MODULE.split('.')[:-1])]
except KeyError:
    PROJECT_MODULE = None

def get_default_breadcrumb():
    string = smart_bytes('kronos:{}'.format(settings.SECRET_KEY))  
    hash = hashlib.md5(string).hexdigest()
    res = 'kronos:{}'.format(hash)
    return res

KRONOS_BREADCRUMB = getattr(settings,
    'KRONOS_BREADCRUMB', get_default_breadcrumb())
