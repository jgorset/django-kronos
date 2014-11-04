import kronos

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'List all available tasks'

    def handle(self, *args, **options):
        kronos.load()

        print('* List of tasks registered in Kronos *')
        for task in kronos.tasks:
            print('>> {0}'.format(task.__name__))
