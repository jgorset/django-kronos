from django.test.client import Client
from django.core.management import call_command

from kronos import tasks, load
from kronos.utils import read_crontab, write_crontab, delete_crontab

import project.cron
import project.app

crontab_backup = ''

load()

def setup():
    global crontab_backup
    crontab_backup = read_crontab()

def teardown():
    global crontab_backup

    if crontab_backup:
        write_crontab(crontab_backup)
    else:
        delete_crontab()

def test_read_crontab():
    """Test reading from the crontab."""
    assert read_crontab() == crontab_backup

def test_write_crontab():
    """Test writing to the crontab."""
    write_crontab("* * * * * echo\n")

    assert read_crontab() == '* * * * * echo\n'

def test_task_collection():
    """Test task collection."""
    assert project.app.cron.complain.__name__ in [task.__name__ for task in tasks]
    assert project.cron.praise.__name__ in [task.__name__ for task in tasks]

def test_runtask():
    """Test running tasks via the ``runtask`` command."""
    call_command('runtask', 'complain')
    call_command('runtask', 'praise')

def test_installtasks():
    """Test installing tasks via the ``installtasks`` command."""
    call_command('installtasks')

    for task in tasks:
        assert task.cron_expression in read_crontab()

def test_unintalltasks():
    """Test uninstalling tasks via the ``uninstalltasks`` command."""
    call_command('uninstalltasks')

    for task in tasks:
        assert task.cron_expression not in read_crontab()
