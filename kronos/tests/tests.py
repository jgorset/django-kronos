import sys
import kronos.tests.project.app
import kronos.tests.project.cron
import mock

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.core.management.base import CommandError
from crontab import CronTab
from kronos.settings import KRONOS_BREADCRUMB
from kronos import registry, load


crontab = CronTab(user=True)

def get_crontab(*args, **kwargs):
    return crontab


class TestCase(TestCase):

    def setUp(self):
        load()
        crontab.remove_all()

    # @patch('subprocess.Popen')
    # def test_unintalltasks(self, mock):
    #     """Test uninstalling tasks with the ``uninstalltasks`` command."""
    #     mock.return_value = Mock(
    #         stdout=StringIO('crontab: installing new crontab'),
    #         stderr=StringIO('')
    #     )
    #
    #     call_command('uninstalltasks')
    #     self.assertTrue(mock.called)

    def test_task_collection(self):
        """Test task collection."""
        self.assertIn(kronos.tests.project.app.cron.complain.__name__,
            [task.name for task in registry])
        self.assertIn(kronos.tests.project.cron.praise.__name__,
            [task.name for task in registry])
        self.assertIn('task',
            [task.name for task in registry])

    def test_runtask(self):
        """Test running tasks via the ``runtask`` command."""
        call_command('runtask', 'complain')
        call_command('runtask', 'praise')

    def test_runtask_django(self):
        """Test running tasks via the ``runtask`` command."""
        self.assertRaises(CommandError,
            lambda: call_command('runtask', 'task'))

    @mock.patch('crontab.CronTab', autospec=True, side_effect=get_crontab)
    def test_installtasks(self, _):
        """Test installing tasks with the ``installtasks`` command."""
        call_command('installtasks')
        self.assertTrue(any(['runtask praise' in cmd for cmd in crontab.commands]))
        self.assertTrue(any(['runtask complain' in cmd for cmd in crontab.commands]))
        self.assertTrue(any(['manage.py task' in cmd for cmd in crontab.commands]))
        self.assertIn(KRONOS_BREADCRUMB, crontab.comments)

    @mock.patch('crontab.CronTab', autospec=True, side_effect=get_crontab)
    def test_uninstalltasks(self, _):
        """Test uninstalling tasks with the ``uninstalltasks`` command."""
        call_command('installtasks')
        call_command('uninstalltasks')
        self.assertEqual(len(list(crontab.commands)), 0)

    def test_list_tasks(self):
        sys.stdout = StringIO()
        call_command('showtasks')
        sys.stdout.seek(0)
        val = sys.stdout.read()
        self.assertIn('complain', val)
        self.assertIn('praise', val)
        self.assertIn('task', val)

    @mock.patch('crontab.CronTab', autospec=True, side_effect=get_crontab)
    def test_third_party(self, _):
        """Test third party cron jobs are left as they are"""
        crontab.new(command='/bin/true')

        call_command('installtasks')
        self.assertTrue(len(list(crontab.commands)), 10)

        call_command('uninstalltasks')
        self.assertTrue(len(list(crontab.commands)), 1)
