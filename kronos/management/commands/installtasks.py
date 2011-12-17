import sys
import os

from subprocess import Popen as run
from subprocess import PIPE

from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings

from kronos import tasks, reinstall

class Command(NoArgsCommand):
    help = 'Register tasks with cron'

    def handle_noargs(self, **options):
        reinstall()

        print "Installed %s tasks." % len(tasks)
