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
