import sys
import os

from subprocess import Popen as run
from subprocess import PIPE

from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings

from kronos import uninstall

class Command(NoArgsCommand):
    help = 'Remove tasks from cron'

    def handle_noargs(self, **options):
        uninstall()
