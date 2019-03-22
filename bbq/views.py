import time
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from bbq import temps
from bbq.queue import queue
from bbq.database import db_session
from bbq.constants import TEMP_TIMEOUT, LOCAL_TZ

app = Flask('bbq')


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
            print(json)
            temps.append({'id': len(temps), 'temp1': json['Temp1'],
                          'temp2': json['Temp2'], 'volts': json['Volts'],
                          'date': datetime.now(LOCAL_TZ), 'mac': json['MAC'], 
                          'mode': json['Mode'], 'runtime': json['Runtime(ms)']})
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


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
