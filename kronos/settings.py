import os
import sys

from django.conf import settings

PROJECT_PATH = os.getcwd()
PROJECT_MODULE = sys.modules['.'.join(settings.SETTINGS_MODULE.split('.')[:-1])]
