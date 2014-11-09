import sys
import kronos.tests.project.app
import kronos.tests.project.cron

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from subprocess import PIPE

from django.core.management import call_command
from django.test import TestCase
from django.core.management.base import CommandError
from kronos import tasks, load
from kronos.utils import read_crontab, write_crontab
from mock import Mock, patch


class TestCase(TestCase):

    def setUp(self):
        load()

    @patch('subprocess.Popen')
    def test_unintalltasks(self, mock):
        """Test uninstalling tasks with the ``uninstalltasks`` command."""
        mock.return_value = Mock(
            stdout=StringIO('crontab: installing new crontab'),
            stderr=StringIO('')
        )

        call_command('uninstalltasks')
        self.assertTrue(mock.called)

    @patch('subprocess.Popen')
    def test_read_crontab(self, mock):
        """Test reading from the crontab."""
        mock.return_value = Mock(
            stdout=StringIO('crontab: installing new crontab'),
            stderr=StringIO('')
        )

        read_crontab()

        mock.assert_called_with(
            args='crontab -l',
            shell=True,
            stdout=PIPE,
            stderr=PIPE
        )

    @patch('subprocess.Popen')
    def test_read_empty_crontab(self, mock):
        """Test reading from an empty crontab."""
        mock.return_value = Mock(
            stdout=StringIO(''),
            stderr=StringIO('crontab: no crontab for <user>')
        )

        read_crontab()

    @patch('subprocess.Popen')
    def test_read_crontab_with_errors(self, mock):
        """Test reading from the crontab."""
        mock.return_value = Mock(
            stdout=StringIO(''),
            stderr=StringIO('bash: crontal: command not found')
        )

        self.assertRaises(ValueError, read_crontab)

    @patch('subprocess.Popen')
    def test_write_crontab(self, mock):
        """Test writing to the crontab."""
        mock.return_value = Mock(
            stdout=StringIO('crontab: installing new crontab'),
            stderr=StringIO('')
        )

        write_crontab("* * * * * echo\n")

        mock.assert_called_with(
            args='printf \'* * * * * echo\n\' | crontab',
            shell=True,
            stdout=PIPE,
            stderr=PIPE
        )

    def test_task_collection(self):
        """Test task collection."""
        self.assertIn(kronos.tests.project.app.cron.complain.__name__,
            [task['name'] for task in tasks])
        self.assertIn(kronos.tests.project.cron.praise.__name__,
            [task['name'] for task in tasks])
        self.assertIn('task',
            [task['name'] for task in tasks])

    def test_runtask(self):
        """Test running tasks via the ``runtask`` command."""
        call_command('runtask', 'complain')
        call_command('runtask', 'praise')

    def test_runtask_django(self):
        """Test running tasks via the ``runtask`` command."""
        self.assertRaises(CommandError,
            lambda: call_command('runtask', 'task'))

    @patch('subprocess.Popen')
    def test_installtasks(self, mock):
        """Test installing tasks with the ``installtasks`` command."""
        mock.return_value = Mock(
            stdout=StringIO('crontab: installing new crontab'),
            stderr=StringIO('')
        )

        call_command('installtasks')

        self.assertTrue(mock.called)

    @patch('subprocess.Popen')
    def test_installed_tasks(self, mock):
        """Test installing tasks with the ``installtasks`` command."""
        mock.return_value = Mock(
            stdout=StringIO('crontab: installing new crontab'),
            stderr=StringIO('')
        )

        call_command('installtasks')
        calls = str(mock.mock_calls[-1])
        self.assertIn('runtask praise', calls)
        self.assertIn('runtask complain', calls)
        self.assertIn('manage.py task', calls)

    def test_list_tasks(self):
        sys.stdout = StringIO()
        call_command('showtasks')
        sys.stdout.seek(0)
        val = sys.stdout.read()
        self.assertIn('complain', val)
        self.assertIn('praise', val)
        self.assertIn('task', val)
