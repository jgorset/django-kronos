from django.core.management.base import BaseCommand

import kronos


@kronos.register('0 0 * * *', args={"--arg1": None, "-b": "some-arg2", "--some-list": ["site1", "site2", "site3"]})
class Command(BaseCommand):
    help = 'Register tasks with cron'

    def handle(self, *args, **options):
        print('command task')
