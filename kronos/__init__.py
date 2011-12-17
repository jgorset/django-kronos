import os
import sys

from functools import wraps

from django.conf import settings
from django.utils.importlib import import_module

tasks = []

def load():
    """
    Load ``cron`` modules for applications listed in ``INSTALLED_APPS``.
    """
    for application in settings.INSTALLED_APPS:
        module = import_module(application)

        try:
            import_module('%s.cron' % application)
        except ImportError:
            pass

def register(schedule):
    def decorator(function):
        global tasks

        tasks.append(function)

        function.cron_expression = '%(schedule)s %(python)s %(project_path)s/manage.py runtask %(task)s\n' % {
            'schedule': schedule,
            'python': sys.executable,
            'project_path': os.path.dirname(sys.modules[settings.SETTINGS_MODULE].__file__),
            'task': function.__name__
        }

        @wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper

    return decorator
