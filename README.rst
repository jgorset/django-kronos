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

Register tasks with cron
^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ python manage.py installtasks

Installation
------------

    $ pip install django-kronos

Add ``kronos`` to ``INSTALLED_APPS``.
