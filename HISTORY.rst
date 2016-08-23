1.0.0
+++++

* Django 1.10 support.

0.9.0
+++++

* Fixed a bug that caused Kronos to crash if the settings module resided outside
  of the project directory.
* Fixed a bug that caused Kronos to remove other crontabs upon uninstalling.

0.8.0
+++++

* Kronos is now even more compatible with Python 3.
* Kronos is no longer compatible with Python 2.6.
* Kronos is no longer compatible with Django 1.7.
* You may now prefix commands with ``KRONOS_PREFIX``.
* Fixed an issue where Kronos would not pick up on AppConfig apps.

0.7.0
+++++

* You may now pass arguments to Django management commands registered with Kronos.
* Kronos is now compatible with Python 3.
* Kronos will now log errors when it fails to load tasks.

0.6.0
+++++

* You may now register Django management commands.

0.5.0
+++++

* You may now list commands with ``python manage.py showtasks``.

0.4.0
+++++

* You may now postfix commands with ``KRONOS_POSTFIX``.

0.3.0
+++++

* You may now customize the interpreter, management path and python path for tasks with the ``KRONOS_PYTHON``,
  ``KRONOS_MANAGE`` and ``KRONOS_PYTHONPATH`` settings, respectively.

0.2.3
+++++

* Kronos now supports Django 1.4-style projects.
* Fixed a bug that caused installation to fail for users that didn't already have a crontab.

0.2.2
+++++

* Fixed a bug that caused unclosed single quotes in the crontab to raise a ValueError

0.2.1
+++++

* Fixed a bug that caused 'cron'-modules in the project root to be ignored.

0.2.0
+++++

* Kronos will now collect tasks from a 'cron' module in the project root.
