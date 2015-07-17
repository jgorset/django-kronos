from django.core.management.base import NoArgsCommand

import kronos


@kronos.register('0 0 * * *', args={"--arg1": None, "-b": "some-arg2", "--some-list": ["site1", "site2", "site3"]})
class Command(NoArgsCommand):
    help = 'Register tasks with cron'

    def handle_noargs(self, **options):
        print('command task')
