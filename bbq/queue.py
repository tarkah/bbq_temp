import time
from threading import Thread
from queue import Queue
from bbq import temps
from bbq.constants import TEMP_TIMEOUT

queue = Queue()

def temp_timeout(queue):
    last_update = time.time()
    while True:
        try:
            last_update = queue.get(timeout=11)
        except:
            pass
        delta = time.time() - last_update
        print('Seconds since last temp update: {}'.format(delta))
        if delta > TEMP_TIMEOUT:
            temps.clear()

temp_thread = Thread(target=temp_timeout, args=(queue,))
