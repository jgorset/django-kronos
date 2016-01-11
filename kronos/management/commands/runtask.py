import kronos

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<task>'
    help = 'Run the given task'

    def handle(self, task_name, **options):
        kronos.load()

        for task in kronos.registry:
            if task.name == task_name:
                if task.function:
                    return task.function()
                else:
                    raise CommandError('This is a django command. You have '
                        'to run it via python manage.py {0}'
                        .format(task_name))
        raise CommandError('Task \'%s\' not found' % task_name)
