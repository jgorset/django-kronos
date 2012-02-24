from version import __version__

import os
import sys

from functools import wraps

from kronos.utils import read_crontab, write_crontab, delete_crontab
from kronos.settings import PROJECT_PATH, PROJECT_MODULE

from django.utils.importlib import import_module
from django.conf import settings

tasks = []

def load():
    """
    Load ``cron`` modules for applications listed in ``INSTALLED_APPS``.
    """
    try:
        import_module('%s.cron' % PROJECT_MODULE.__name__)
    except ImportError:
        pass

    # Also try the parent module, in case PROJECT_MODULE is a settings package
    if '.' in PROJECT_MODULE.__name__:
        try:
            import_module('%s.cron' % '.'.join(PROJECT_MODULE.__name__.split('.')[0:-1]))
        except ImportError:
            pass

    for application in settings.INSTALLED_APPS:
        try:
            import_module('%s.cron' % application)
        except ImportError:
            pass

def register(schedule):
    def decorator(function):
        global tasks

        tasks.append(function)

        function.cron_expression = '%(schedule)s %(python)s %(project_path)s/manage.py runtask %(task)s --settings=%(settings_module)s' % {
            'schedule': schedule,
            'python': sys.executable,
            'project_path': PROJECT_PATH,
            'task': function.__name__,
            'settings_module': settings.SETTINGS_MODULE,
        }

        @wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper

    return decorator

def install():
    """
    Register tasks with cron.
    """
    load()

    current_crontab = read_crontab()

    new_crontab = ''
    for task in tasks:
        new_crontab += '%s\n' % task.cron_expression

    write_crontab(current_crontab + new_crontab)

def printtasks():
    """
    Print the tasks that would be installed in the
    crontab, for debugging purposes.
    """
    load()

    for task in tasks:
        print task.cron_expression

def uninstall():
    """
    Uninstall tasks from cron.
    """
    current_crontab = read_crontab()

    new_crontab = ''
    for line in current_crontab.split('\n')[:-1]:
        if '%(python)s %(project_path)s/manage.py runtask' % {
            'python': sys.executable,
            'project_path': PROJECT_PATH,
        } not in line:
            new_crontab += '%s\n' % line

    if new_crontab:
        write_crontab(new_crontab)
    else:
        delete_crontab()

def reinstall():
    uninstall()
    install()
