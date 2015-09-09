from django.core.management.base import BaseCommand
import kronos


class Command(BaseCommand):
    help = 'List all available tasks'

    def handle(self, *args, **options):
        kronos.load()

        print('* List of tasks registered in Kronos *')

        print('>> Kronos tasks')
        for task in kronos.registry:
            if task.function:
                print('    >> {0}'.format(task.name))

        print('>> Django tasks')
        for task in kronos.registry:
            if not task.function:
                print('    >> {0}'.format(task.name))
