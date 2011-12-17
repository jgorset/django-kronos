import os
import sys

from functools import wraps

from django.conf import settings
from django.utils.importlib import import_module

from kronos.utils import read_crontab, write_crontab, delete_crontab

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

        function.cron_expression = '%(schedule)s %(python)s %(project_path)s/manage.py runtask %(task)s' % {
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

def uninstall():
    """
    Uninstall tasks from cron.
    """
    current_crontab = read_crontab()

    new_crontab = ''
    for line in current_crontab.split('\n')[:-1]:
        if '%(python)s %(project_path)s/manage.py runtask' % {
            'python': sys.executable,
            'project_path': os.path.dirname(sys.modules[settings.SETTINGS_MODULE].__file__)
        } not in line:
            new_crontab += '%s\n' % line

    if new_crontab:
        write_crontab(new_crontab)
    else:
        delete_crontab()

def reinstall():
    uninstall()
    install()
