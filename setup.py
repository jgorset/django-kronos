#!/usr/bin/env python
import os
from setuptools import setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
exec(compile(open('kronos/version.py').read(), 'kronos/version.py', 'exec'))

readme = open('README.rst').read()
history = open('HISTORY.rst').read()

setup(
    name='django-kronos',
    version=__version__,
    description='Kronos is a Django application that makes it easy to define and schedule tasks with cron.',
    long_description=readme + '\n\n' + history,
    author='Johannes Gorset',
    author_email='jgorset@gmail.com ',
    url='http://github.com/jgorset/kronos',
    packages=['kronos'],
    include_package_data=True,
    zip_safe=False,
)
