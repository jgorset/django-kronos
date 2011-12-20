#!/usr/bin/env python

from setuptools import setup

from kronos.version import __version__

setup(
    name = 'kronos',
    version = __version__,
    description = 'Kronos is a Django application that makes it easy to define and schedule tasks with cron.',
    author = 'Johannes Gorset',
    author_email = 'jgorset@gmail.com',
    url = 'http://github.com/jgorset/kronos',
    packages = ['kronos', 'kronos.management', 'kronos.management.commands']
)
