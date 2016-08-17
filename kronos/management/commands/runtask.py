import kronos

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Run the given task'

    def add_arguments(self, parser):
        parser.add_argument('task', nargs='?', type=str)

    def handle(self, *args, **options):
        kronos.load()

        task_name = options.get('task')

        for task in kronos.registry:
            if task.name == task_name:
                if task.function:
                    return task.function()
                else:
                    raise CommandError('This is a django command. You have '
                        'to run it via python manage.py {0}'
                        .format(task_name))
        raise CommandError('Task \'%s\' not found' % task_name)
