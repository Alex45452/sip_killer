import datetime

def time_checker():
    def wrapper(func):
        while datetime.datetime.now() - start_time < attack_duration:
            func()
            asyncio.sleep(speed)
        return
    return wrapper