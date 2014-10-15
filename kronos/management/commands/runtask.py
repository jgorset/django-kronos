from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

import kronos


class Command(BaseCommand):
    help = 'Run the given task'

    option_list = BaseCommand.option_list + (
        make_option('--list',
            action='store_true',
            dest='list',
            default=False,
            help='List all available tasks'),
        )

    def handle(self, *args, **options):
        kronos.load()

        if options['list']:
            print('* List of tasks registered in Kronos *')
            for task in kronos.tasks:
                print('>> {0}'.format(task.__name__))
        else:
            if len(args) == 0:
                raise CommandError('You need to add a task')
            task_name = args[0]
            for task in kronos.tasks:
                if task.__name__ == task_name:
                    return task()
            raise CommandError('Task \'%s\' not found' % task_name)
