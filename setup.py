#!/usr/bin/env python

from setuptools import setup

execfile('kronos/version.py')

setup(
    name = 'django-kronos',
    version = __version__,
    description = 'Kronos is a Django application that makes it easy to define and schedule tasks with cron.',
    long_description = open('README.rst').read(),
    author = 'Johannes Gorset',
    author_email = 'jgorset@gmail.com',
    url = 'http://github.com/jgorset/kronos',
    packages = ['kronos', 'kronos.management', 'kronos.management.commands']
)
