from django.core.management.base import BaseCommand, CommandError

import kronos

class Command(BaseCommand):
    args = '<task>'
    help = 'Run the given task'

    def handle(self, *args, **options):
        kronos.load()

        task_name = args[0]

        if len(args) > 1:
            for task in kronos.tasks:
                if task.__name__ == task_name:
                    return task(args[1:])
        else:
            for task in kronos.tasks:
                if task.__name__ == task_name:
                    return task()

        raise CommandError('Task \'%s\' not found' % task_name)