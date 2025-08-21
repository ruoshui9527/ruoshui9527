import random
import time

def is_valid_time():
    current_time = time.localtime()
    current_hour = current_time.tm_hour

    if 8 <= current_hour < 26:
        return True
    else:
        return False


def wait_time():
    get_time = random.uniform(600, 1800)
    time.sleep(get_time)