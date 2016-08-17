from django.core.management.base import BaseCommand

from kronos import uninstall


class Command(BaseCommand):
    help = 'Remove tasks from cron'

    def handle(self, **options):
        count = uninstall()
        print('{} tasks removed'.format(count))
