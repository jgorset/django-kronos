from django.core.management.base import BaseCommand, CommandError

import kronos

class Command(BaseCommand):
    args = '<task>'
    help = 'Run the given task'

    def handle(self, task_name, **options):
        kronos.load()

        for task in kronos.tasks:
            if task.__name__ == task_name:
                if task.seconds_interval is not None and task.seconds_interval < 60:
                    results = []
                    counter = int(60/task.seconds_interval)

                    for i in xrange(counter):
                        results.append(task())

                        if i < counter:
                            sleep(task.seconds_interval)

                    return str(results)
                else:
                    return task()

        raise CommandError('Task \'%s\' not found' % task_name)
