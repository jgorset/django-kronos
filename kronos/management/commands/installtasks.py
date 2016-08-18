from django.core.management.base import BaseCommand
from kronos import reinstall


class Command(BaseCommand):
    help = 'Register tasks with cron'

    def handle(self, *args, **options):
        removed, installed = reinstall()
        if not removed:
            print("{} tasks installed.".format(installed))
        elif not installed:
            print("{} tasks removed.".format(removed))
        else:
            print("{} tasks removed, {} installed.".format(removed, installed))
