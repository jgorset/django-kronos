from django.core.management.base import BaseCommand

import kronos


@kronos.register('0 0 * * *', args={})
class Command(BaseCommand):
    help = 'Register tasks with cron'

    def handle(self, *args, **options):
        print('command task')
