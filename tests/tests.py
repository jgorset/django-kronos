from nose.tools import with_setup

from django.test.client import Client
from django.core.management import call_command

from subprocess import PIPE
from StringIO import StringIO

from nose.tools import *

from kronos import tasks, load
from kronos.utils import read_crontab, write_crontab, delete_crontab

from mock import Mock, patch

import project.cron
import project.app

load()

@patch('subprocess.Popen')
def test_read_crontab(mock):
    """Test reading from the crontab."""
    mock.return_value = Mock(
        stdout = StringIO('crontab: installing new crontab'),
        stderr = StringIO('')
    )

    read_crontab()

    mock.assert_called_with(
        args = 'crontab -l',
        shell = True,
        stdout = PIPE,
        stderr = PIPE
    )

@patch('subprocess.Popen')
def test_read_empty_crontab(mock):
    """Test reading from an empty crontab."""
    mock.return_value = Mock(
        stdout = StringIO(''),
        stderr = StringIO('crontab: no crontab for <user>')
    )

    read_crontab()

@patch('subprocess.Popen')
def test_read_crontab_with_errors(mock):
    """Test reading from the crontab."""
    mock.return_value = Mock(
        stdout = StringIO(''),
        stderr = StringIO('bash: crontal: command not found')
    )

    assert_raises(ValueError, read_crontab)

@patch('subprocess.Popen')
def test_write_crontab(mock):
    """Test writing to the crontab."""
    mock.return_value = Mock(
        stdout = StringIO('crontab: installing new crontab'),
        stderr = StringIO('')
    )

    write_crontab("* * * * * echo\n")

    mock.assert_called_with(
        args = 'printf \'* * * * * echo\n\' | crontab',
        shell = True,
        stdout = PIPE,
        stderr = PIPE
    )

def test_task_collection():
    """Test task collection."""
    assert project.app.cron.complain.__name__ in [task.__name__ for task in tasks]
    assert project.cron.praise.__name__ in [task.__name__ for task in tasks]

def test_runtask():
    """Test running tasks via the ``runtask`` command."""
    call_command('runtask', 'complain')
    call_command('runtask', 'praise')

@patch('subprocess.Popen')
def test_installtasks(mock):
    """Test installing tasks with the ``installtasks`` command."""
    mock.return_value = Mock(
        stdout = StringIO('crontab: installing new crontab'),
        stderr = StringIO('')
    )

    call_command('installtasks')

    assert mock.called

@patch('subprocess.Popen')
def test_unintalltasks(mock):
    """Test uninstalling tasks with the ``uninstalltasks`` command."""
    mock.return_value = Mock(
        stdout = StringIO('crontab: installing new crontab'),
        stderr = StringIO('')
    )

    call_command('uninstalltasks')

    assert mock.called
