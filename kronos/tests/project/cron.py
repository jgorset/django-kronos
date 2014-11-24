import kronos

@kronos.register('0 0 * * *')
def praise():
    print("Kronos makes it really easy to define and schedule "
        "tasks with cron!")
