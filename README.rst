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
