from functools import wraps

from django.core.management import get_commands, load_command_class
from django.utils.importlib import import_module
from kronos.settings import PROJECT_MODULE, KRONOS_PYTHON, KRONOS_MANAGE, \
    KRONOS_PYTHONPATH, KRONOS_POSTFIX
from django.conf import settings
from kronos.utils import read_crontab, write_crontab, delete_crontab
from kronos.version import __version__


tasks = []


def load():
    """
    Load ``cron`` modules for applications listed in ``INSTALLED_APPS``.
    """
    paths = ['%s.cron' % PROJECT_MODULE.__name__]

    if '.' in PROJECT_MODULE.__name__:
        paths.append('%s.cron' % '.'.join(
            PROJECT_MODULE.__name__.split('.')[0:-1]))

    for application in settings.INSTALLED_APPS:
        paths.append('%s.cron' % application)

    # load kronostasks
    for p in paths:
        try:
            import_module(p)
        except ImportError:
            pass

    # load django tasks
    for cmd, app in get_commands().items():
        load_command_class(app, cmd)


def register(schedule):
    def decorator(function):
        global tasks

        if hasattr(function, 'handle'):
            # django command
            function.cron_expression = '%(schedule)s %(python)s %(manage)s ' \
                '%(task)s --settings=%(settings_module)s %(postfix)s' \
                '$KRONOS_BREAD_CRUMB' % {
                    'schedule': schedule,
                    'python': KRONOS_PYTHON,
                    'manage': KRONOS_MANAGE,
                    'task': function.__module__.split('.')[-1],
                    'settings_module': settings.SETTINGS_MODULE,
                    'postfix': KRONOS_POSTFIX
                }
            task = dict(name=function.__module__.split('.')[-1],
                django_command=True,
                fn=function)
        else:
            function.cron_expression = '%(schedule)s %(python)s %(manage)s ' \
                'runtask %(task)s --settings=%(settings_module)s ' \
                '%(postfix)s $KRONOS_BREAD_CRUMB' % {
                    'schedule': schedule,
                    'python': KRONOS_PYTHON,
                    'manage': KRONOS_MANAGE,
                    'task': function.__name__,
                    'settings_module': settings.SETTINGS_MODULE,
                    'postfix': KRONOS_POSTFIX
                }
            task = dict(name=function.__name__,
                django_command=False,
                fn=function)

        if KRONOS_PYTHONPATH is not None:
            function.cron_expression += ' --pythonpath=%s' % KRONOS_PYTHONPATH

        tasks.append(task)

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
        new_crontab += '%s\n' % task['fn'].cron_expression

    write_crontab(current_crontab + new_crontab)


def printtasks():
    """
    Print the tasks that would be installed in the
    crontab, for debugging purposes.
    """
    load()

    for task in tasks:
        print(task['fn'].cron_expression)


def uninstall():
    """
    Uninstall tasks from cron.
    """
    current_crontab = read_crontab()

    new_crontab = ''
    for line in current_crontab.split('\n')[:-1]:
        exp = '%(python)s %(manage)s runtask' % {
            'python': KRONOS_PYTHON,
            'manage': KRONOS_MANAGE,
            }
        if '$KRONOS_BREAD_CRUMB' not in line and exp not in line:
            new_crontab += '%s\n' % line

    if new_crontab:
        write_crontab(new_crontab)
    else:
        delete_crontab()


def reinstall():
    uninstall()
    install()
