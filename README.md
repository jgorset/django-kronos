# Kronos

## About

Kronos is a Django application that makes it easy to define and schedule tasks with *cron*.

## Usage

### Define tasks

Kronos collects tasks from `cron` modules in each of your applications:

    # cookies/cron.py

    import cron
    
    # Register a task and schedule it with a timedelta-compatible format
    @cron.register(minutes=15)
    def complain():
        complaints = [
            "I forgot to migrate our applications's cron jobs to our new server! Darn!",
            "I'm out of complaints! Damnit!"
        ]

        print random.choice(complaints)

    # Register a task with cron's native scheduling format
    @cron.register('0 0 * * *')
    def praise():
        print "Kronos makes it really easy to define and schedule recurring tasks!"


### Register tasks with cron

    $ django cron install
