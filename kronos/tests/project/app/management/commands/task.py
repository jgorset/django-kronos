from django.core.management.base import NoArgsCommand

import kronos


@kronos.register('0 0 * * *')
class Command(NoArgsCommand):
    help = 'Register tasks with cron'

    def handle_noargs(self, **options):
        print('command task')
