import kronos

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'List all available tasks'

    def handle(self, *args, **options):
        kronos.load()

        print('* List of tasks registered in Kronos *')

        print('>> Kronos tasks')
        for task in kronos.tasks:
            if not task['django_command']:
                print('    >> {0}'.format(task['name']))

        print('>> Django tasks')
        for task in kronos.tasks:
            if task['django_command']:
                print('    >> {0}'.format(task['name']))
