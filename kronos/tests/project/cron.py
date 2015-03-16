import kronos

@kronos.register('0 0 * * *')
def praise():
    print("Kronos makes it really easy to define and schedule "
        "tasks with cron!")

@kronos.register('0 0 * * *', args={"--arg1": None, "-b": "some-arg2", "--some-list": ["site1", "site2", "site3"]})
def praise_with_args():
    print("Kronos makes it really easy to define and schedule "
        "tasks with cron, even with arguments!")

@kronos.register('0 0 * * *', args={})
def praise_with_empty_args():
    print("Kronos makes it really easy to define and schedule "
        "tasks with cron, even with arguments, that you can forget and it still work!")