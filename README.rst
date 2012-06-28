Kronos
======

Kronos makes it really easy to schedule tasks with cron.

Usage
-----

Define tasks
^^^^^^^^^^^^

Kronos collects tasks from ``cron`` modules in your project root and each of your applications::

    # app/cron.py

    import kronos

    @kronos.register('0 0 * * *')
    def complain():
        complaints = [
            "I forgot to migrate our applications's cron jobs to our new server! Darn!",
            "I'm out of complaints! Damnit!"
        ]

        print random.choice(complaints)

Run tasks manually
^^^^^^^^^^^^^^^^^^

::

    $ python manage.py runtask complain
    I forgot to migrate our applications's cron jobs to our new server! Darn!

Register tasks with cron
^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ python manage.py installtasks
    Installed 1 task.

You can review the crontab with a ``crontab -l`` command::

    $ crontab -l
    0 0 * * * /usr/bin/python /path/to/manage.py runtask complain --settings=myprpoject.settings

Usually this line will work pretty well for you, but there can be some rare
cases when it requires modification. You can achieve it with a number of
settings variables used by kronos:

KRONOS_PYTHON
    Python interpreter to build a crontab line. By default the
    same interpreter as one you invoked to install tasks is used.

KRONOS_MANAGE
    Management command to build a crontab line. By default ``getcwd() + manage.py``
    is used.

KRONOS_PYTHONPATH
    Extra path which will be added as a ``--pythonpath`` option to the management command.
    By default extra pythonpath is not used.

Define these variables in your :file:`settings.py` if you wish to alter crontab
lines.

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
