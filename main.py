import time
from datetime import datetime
import pytz
from flask import Flask, request, render_template, jsonify
from threading import Thread
from queue import Queue

TEMP_TIMEOUT = 60*60
LOCAL_TZ = pytz.timezone('US/Pacific')

queue = Queue()

app = Flask(__name__)

placeholder_temp = {'id': -1, 'temp1': 0, 'temp2': 0, 'volts': 0, 'date': datetime.now(LOCAL_TZ)}
temps = [ placeholder_temp ]

@app.route('/')
def index():
    return render_template('index.html', temps=temps)

@app.route('/api/temp', methods=['GET', 'POST'])
def api_temp():
    if request.method == 'POST':
        if request.is_json:
            json = request.get_json(silent=True)
            if json is None:
                response = { 'status': 'failure', 'error_message': 'Json empty or not valid' }
                return jsonify(response)
            queue.put(time.time())
            if temps[0]['id'] == -1:
                temps.pop(0)
            temps.append({'id': len(temps), 'temp1': json['Temp1'],
                          'temp2': json['Temp2'], 'volts': json['Volts'],
                          'date': datetime.now(LOCAL_TZ)})
            response = { 'status': 'success' }
            return jsonify(response)
        else:
            response = { 'status': 'failure', 'error_message': 'Must be application/json' }
            return jsonify(response)
    else:
        response = { 'status': 'success', 'data': temps }
        return jsonify(response)

@app.route('/api/temp/<int:id>', methods=['GET'])
def api_temp_id(id):
    try:
        temp = [temp for temp in temps if temp['id'] == id][0]
        response = {'status': 'succcess', 'data': temp}
    except:
        response = {'status': 'failure', 'error_message': 'Invalid id' }
    return jsonify(response)

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
            temps.append(placeholder_temp)

if __name__ == '__main__':
    Thread(target=temp_timeout, args=(queue,)).start()
    app.run(host='0.0.0.0', port=8085)
