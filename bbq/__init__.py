from flask import Flask

app = Flask(__name__)


temps = []


from threading import Thread
from bbq.queue import queue, temp_timeout

temp_thread = Thread(target=temp_timeout, args=(queue,))


from bbq.views import *
