# Kronos

## About

Kronos is a Django application that makes it easy to define and schedule tasks with cron.

## Usage

### Define tasks

Kronos collects tasks from `cron` modules in each of your applications:

    # cookies/cron.py

    import kronos

    @kronos.register('0 0 * * *')
    def praise():
        complaints = [
            "I forgot to migrate our applications's cron jobs to our new server! Darn!",
            "I'm out of complaints! Damnit!"
        ]

        print random.choice(complaints)

### Register tasks with cron

    $ python manage.py installtasks

## Installation

    $ pip install kronos
