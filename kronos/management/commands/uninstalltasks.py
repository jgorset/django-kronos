from django.core.management.base import NoArgsCommand

from kronos import uninstall


class Command(NoArgsCommand):
    help = 'Remove tasks from cron'

    def handle_noargs(self, **options):
        count = uninstall()
        print('{} tasks removed'.format(count))
