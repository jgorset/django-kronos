from optparse import make_option

from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings

from kronos import tasks, reinstall, printtasks

class Command(NoArgsCommand):
    help = 'Register tasks with cron'

    option_list = NoArgsCommand.option_list + (
        make_option(
            '--fake',
            action='store_true',
            dest='fake',
            default=False,
            help='Do not write the crontab, instead print the lines that \
                  would be added for debugging'
        ),
    )

    def handle_noargs(self, **options):
        if options.get('fake'):
            printtasks()
        else:
            reinstall()
            print "Installed %s tasks." % len(tasks)
