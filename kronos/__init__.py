from functools import wraps
import collections
import crontab
import django
from django.core.management import get_commands, load_command_class

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

from kronos.settings import PROJECT_MODULE, KRONOS_PYTHON, KRONOS_MANAGE, \
    KRONOS_PYTHONPATH, KRONOS_POSTFIX, KRONOS_PREFIX, KRONOS_BREADCRUMB
from django.conf import settings
from kronos.version import __version__
import six
from django.utils.module_loading import autodiscover_modules


Task = collections.namedtuple('Task', ['name', 'schedule', 'command', 'function'])

registry = set()


def load():
    """
    Load ``cron`` modules for applications listed in ``INSTALLED_APPS``.
    """
    autodiscover_modules('cron')

    if PROJECT_MODULE:
        if '.' in PROJECT_MODULE.__name__:
            try:
                import_module('%s.cron' % '.'.join(
                    PROJECT_MODULE.__name__.split('.')[0:-1]))
            except ImportError as e:
                if 'No module named' not in str(e):
                    print(e)

    # load django tasks
    for cmd, app in get_commands().items():
        try:
            load_command_class(app, cmd)
        except django.core.exceptions.ImproperlyConfigured:
            pass


KRONOS_TEMPLATE = \
    '%(prefix)s %(python)s %(manage)s ' \
    'runtask %(name)s %(passed_args)s --settings=%(settings_module)s ' \
    '%(postfix)s'

DJANGO_TEMPLATE = \
    '%(prefix)s %(python)s %(manage)s ' \
    '%(name)s %(passed_args)s --settings=%(settings_module)s ' \
    '%(postfix)s'


def process_args(args):
    res = []
    for key, value in six.iteritems(args):
        if isinstance(value, dict):
            raise TypeError('Parse for dict arguments not yet implemented.')

        if isinstance(value, list):
            temp_args = ",".join(map(str, value))
            res.append("{}={}".format(key, temp_args))
        else:
            if value is None:
                arg_text = "{}"
            elif isinstance(value, str):
                arg_text = '{}="{}"'
            else:
                arg_text = '{}={}'
            res.append(arg_text.format(key, value))
    return res


def register(schedule, args=None):
    def decorator(function):
        global registry_kronos, registry_django

        passed_args = process_args(args) if args is not None else []

        ctx = {
            'prefix': KRONOS_PREFIX,
            'python': KRONOS_PYTHON,
            'manage': KRONOS_MANAGE,
            'passed_args': ' '.join(passed_args),
            'settings_module': settings.SETTINGS_MODULE,
            'postfix': KRONOS_POSTFIX
        }

        if hasattr(function, 'handle'):
            func = None
            tmpl = DJANGO_TEMPLATE
            name = function.__module__.split('.')[-1]
        else:
            func = function
            tmpl = KRONOS_TEMPLATE
            name = function.__name__

        command = tmpl % dict(ctx, name=name)
        if KRONOS_PYTHONPATH is not None:
            command += ' --pythonpath=%s' % KRONOS_PYTHONPATH

        registry.add(Task(name, schedule, command, func))

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
    tab = crontab.CronTab(user=True)
    for task in registry:
        tab.new(task.command, KRONOS_BREADCRUMB).setall(task.schedule)
    tab.write()
    return len(registry)


def printtasks():
    """
    Print the tasks that would be installed in the
    crontab, for debugging purposes.
    """
    load()

    tab = crontab.CronTab('')
    for task in registry:
        tab.new(task.command, KRONOS_BREADCRUMB).setall(task.schedule)
    print(tab.render())


def uninstall():
    """
    Uninstall tasks from cron.
    """
    tab = crontab.CronTab(user=True)
    count = len(list(tab.find_comment(KRONOS_BREADCRUMB)))
    tab.remove_all(comment=KRONOS_BREADCRUMB)
    tab.write()
    return count


def reinstall():
    return uninstall(), install()
