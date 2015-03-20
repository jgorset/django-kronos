import subprocess


def read_crontab():
    """
    Read the crontab.
    """
    command = subprocess.Popen(
        args='crontab -l',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = command.stdout.read(), command.stderr.read()

    if stderr and 'no crontab for' not in stderr.decode():
        raise ValueError('Could not read from crontab: \'%s\'' % stderr)

    return stdout


def write_crontab(string):
    """
    Write the given string to the crontab.
    """
    command = subprocess.Popen(
        args='printf \'%s\' | crontab' % string.replace("'", "'\\''"),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = command.stdout.read(), command.stderr.read()

    if stderr:
        raise ValueError('Could not write to crontab: \'%s\'' % stderr)


def delete_crontab():
    """
    Delete the crontab.
    """
    command = subprocess.Popen(
        args='crontab -r',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = command.stdout.read(), command.stderr.read()

    if stderr and 'no crontab' not in stderr.decode():
        raise ValueError('Could not delete crontab: \'%s\'' % stderr)
