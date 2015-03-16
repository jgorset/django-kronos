import random
import kronos


@kronos.register('0 0 * * *')
def complain():
    complaints = [
        "I forgot to migrate our applications's cron jobs to our new server! Darn!",
        "I'm out of complaints! Damnit!"
    ]

    print(random.choice(complaints))

@kronos.register('0 0 * * *', args={"--arg1": None, "-b": "some-arg2", "--some-list": ["site1", "site2", "site3"]})
def complain_with_args():
    complaints = [
        "I forgot to migrate our applications's cron jobs to our new server! Darn!",
        "I'm out of complaints! Damnit!"
    ]

    print(random.choice(complaints))

@kronos.register('0 0 * * *', args={})
def complain_with_empty_args():
    complaints = [
        "I forgot to migrate our applications's cron jobs to our new server! Darn!",
        "I'm out of complaints! Damnit!"
    ]

    print(random.choice(complaints))
