from django.core.management.base import NoArgsCommand
from kronos import reinstall


class Command(NoArgsCommand):
    help = 'Register tasks with cron'

    def handle_noargs(self, **options):
        removed, installed = reinstall()
        if not removed:
            print("{} tasks installed.".format(installed))
        elif not installed:
            print("{} tasks removed.".format(removed))
        else:
            print("{} tasks removed, {} installed.".format(removed, installed))
