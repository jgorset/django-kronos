import sys
import os

from subprocess import Popen as run
from subprocess import PIPE

from django.conf import settings

import kronos

def read_crontab():
    """
    Read the crontab.
    """
    command = run(
        args = 'crontab -l',
        shell = True,
        stdout = PIPE,
        stderr = PIPE
    )

    stdout, stderr = command.stdout.read(), command.stderr.read()

    if stderr and 'no crontab for' not in stderr:
        raise ValueError('Could not read from crontab: \'%s\'' % stderr)

    return stdout

def write_crontab(string):
    """
    Write the given string to the crontab.
    """
    command = run(
        args = 'printf \'%s\' | crontab' % string.replace("'", "'\\''"),
        shell = True,
        stdout = PIPE,
        stderr = PIPE
    )

    stdout, stderr = command.stdout.read(), command.stderr.read()

    if stderr:
        raise ValueError('Could not write to crontab: \'%s\'' % stderr)

def delete_crontab():
    """
    Delete the crontab.
    """
    command = run(
        args = 'crontab -r',
        shell = True,
        stdout = PIPE,
        stderr = PIPE
    )

    stdout, stderr = command.stdout.read(), command.stderr.read()

    if stderr and 'no crontab' not in stderr:
        raise ValueError('Could not delete crontab: \'%s\'' % stderr)
