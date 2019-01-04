.. image::  https://raw.githubusercontent.com/jgorset/django-kronos/master/docs/banner.png

.. image:: https://coveralls.io/repos/github/jgorset/django-kronos/badge.svg?branch=master
    :target: https://coveralls.io/github/jgorset/django-kronos?branch=master
.. image:: https://travis-ci.org/jgorset/django-kronos.svg?branch=master
    :target: https://travis-ci.org/jgorset/django-kronos
.. image:: https://img.shields.io/github/license/jgorset/django-kronos.svg
    :target: https://raw.githubusercontent.com/jgorset/django-kronos/master/LICENSE
.. image:: https://img.shields.io/pypi/v/django-kronos.svg
    :target: https://pypi.python.org/pypi/django-kronos/

Usage
-----

Define tasks
^^^^^^^^^^^^

Kronos collects tasks from ``cron`` modules in your project root and each of your applications::

    # app/cron.py

    import kronos
    import random

    @kronos.register('0 0 * * *')
    def complain():
        complaints = [
            "I forgot to migrate our applications's cron jobs to our new server! Darn!",
            "I'm out of complaints! Damnit!"
        ]

        print random.choice(complaints)

Kronos works with Django management commands, too::

    # app/management/commands/task.py

    from django.core.management.base import BaseCommand

    import kronos

    @kronos.register('0 0 * * *')
    class Command(BaseCommand):
        def handle(self, *args, **options):
            print('Hello, world!')

If your management command accepts arguments, just pass them in the decorator::

    # app/management/commands/task.py

    from django.core.management.base import BaseCommand

    import kronos

    @kronos.register('0 0 * * *', args={'-l': 'nb'})
    class Command(BaseCommand):

        def add_arguments(self, parser):
            parser.add_argument(
                '-l', '--language',
                dest='language',
                type=str,
                default='en',
            )

        def handle(self, *args, **options):
            if options['language'] == 'en':
              print('Hello, world!')

            if options['language'] == 'nb':
              print('Hei, verden!')


Run tasks manually
^^^^^^^^^^^^^^^^^^

::

    $ python manage.py runtask complain
    I forgot to migrate our applications's cron jobs to our new server! Darn!

Keep in mind that if the registered task is a django command you have to run it
in the normal way::

    $ python manage.py task


List all registered tasks
^^^^^^^^^^^^^^^^^^

::

    $ python manage.py showtasks
    * List of tasks registered in Kronos *
    >> Kronos tasks
        >> my_task_one
        >> my_task_two
    >> Django tasks
        >> my_django_task


Register tasks with cron
^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ python manage.py installtasks
    Installed 1 task.

You can review the crontab with a ``crontab -l`` command::

    $ crontab -l
    0 0 * * * /usr/bin/python /path/to/manage.py runtask complain --settings=myprpoject.settings $KRONOS_BREAD_CRUMB
    0 0 * * * /usr/bin/python /path/to/manage.py task --settings=myprpoject.settings $KRONOS_BREAD_CRUMB

Usually this line will work pretty well for you, but there can be some rare
cases when it requires modification. You can achieve it with a number of
settings variables used by kronos:

KRONOS_PYTHON
    Python interpreter to build a crontab line (defaults to the interpreter you used to
    invoke the management command).

KRONOS_MANAGE
    Management command to build a crontab line (defaults to ``manage.py`` in the current
    working directory).

KRONOS_PYTHONPATH
    Extra path which will be added as a ``--pythonpath`` option to the management command.

KRONOS_POSTFIX
    Extra string added at the end of the command. For dirty things like ``> /dev/null 2>&1``

KRONOS_PREFIX
    Extra string added at the beginning of the command. For dirty things like ``source /path/to/env &&``.
    If you use the ``virtualenv``, you can add the environment path by ``echo "KRONOS_PREFIX = 'source `echo $VIRTUAL_ENV`/bin/activate && '" >> myprpoject/settings.py``

Define these variables in your ``settings.py`` file if you wish to alter crontab lines.

The env variable ``$KRONOS_BREAD_CRUMB`` is defined to detect which tasks have to be deleted after
being installed.

Installation
------------

::

    $ pip install django-kronos

... and add ``kronos`` to ``INSTALLED_APPS``.


Contribute
----------

* Fork the repository.
* Do your thing.
* Open a pull request.
* Receive cake.

I love you
----------

Johannes Gorset made this. You should `tweet me <http://twitter.com/jgorset>`_ if you can't get it
to work. In fact, you should tweet me anyway.
