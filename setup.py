#!/usr/bin/env python

from setuptools import setup

from kronos.version import __version__

setup(
    name = 'kronos',
    version = __version__,
    description = '',
    author = 'Johannes Gorset',
    author_email = 'jgorset@gmail.com',
    url = '',
    packages = ['kronos', 'kronos.management', 'kronos.management.commands']
)
