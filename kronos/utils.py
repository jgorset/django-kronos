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
        args = 'printf \'%s\' | crontab' % string,
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

    if stderr:
        raise ValueError('Could not delete crontab: \'%s\'' % stderr)

def install():
    """
    Register tasks with cron.
    """
    kronos.load()

    current_crontab = read_crontab()

    new_crontab = ''
    for task in kronos.tasks:
        new_crontab += task.cron_expression

    write_crontab(current_crontab + new_crontab)

def uninstall():
    """
    Uninstall tasks from cron.
    """
    current_crontab = read_crontab()

    new_crontab = ''
    for line in current_crontab.split('\n')[:-1]:
        if '%(python)s %(project_path)s/manage.py runtask' % {
            'python': sys.executable,
            'project_path': os.path.dirname(sys.modules[settings.SETTINGS_MODULE].__file__)
        } not in line:
            new_crontab += '%s\n' % line

    write_crontab(new_crontab)

def reinstall():
    uninstall()
    install()
