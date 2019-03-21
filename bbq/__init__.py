from flask import Flask
app = Flask(__name__)

temps = []

from bbq.queue import temp_thread
from bbq.views import *
