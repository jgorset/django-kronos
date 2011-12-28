#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'django-kronos',
    version = '0.2.2',
    description = 'Kronos is a Django application that makes it easy to define and schedule tasks with cron.',
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG').read(),
    author = 'Johannes Gorset',
    author_email = 'jgorset@gmail.com',
    url = 'http://github.com/jgorset/kronos',
    packages = ['kronos', 'kronos.management', 'kronos.management.commands']
)
