from django.core.management.base import BaseCommand, CommandError

import kronos

class Command(BaseCommand):
    args = '<task>'
    help = 'Run the given task'

    def handle(self, task_name, **options):
        kronos.load()

        for task in kronos.tasks:
            if task.__name__ == task_name:
                return task()

        raise CommandError('Task \'%s\' not found' % task_name)
