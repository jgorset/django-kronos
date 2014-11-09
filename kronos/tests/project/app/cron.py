import random
import kronos


@kronos.register('0 0 * * *')
def complain():
    complaints = [
        "I forgot to migrate our applications's cron jobs to our new server! Darn!",
        "I'm out of complaints! Damnit!"
    ]

    print(random.choice(complaints))
