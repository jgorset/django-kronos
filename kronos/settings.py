import os
import sys

from django.conf import settings

SETTINGS_MODULE = sys.modules[settings.SETTINGS_MODULE]
SETTINGS_PATH = SETTINGS_MODULE.__file__
PROJECT_PATH = os.path.dirname(SETTINGS_PATH)
PROJECT_MODULE = sys.modules['.'.join(settings.SETTINGS_MODULE.split('.')[:-1])]
