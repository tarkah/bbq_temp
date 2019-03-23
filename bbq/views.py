import time
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from bbq import temps
from bbq.database import db_session
from bbq.models import Device, Session, Temp
from bbq.constants import TEMP_TIMEOUT, LOCAL_TZ

app = Flask('bbq')


@app.route('/')
def index():
    query = db_session.query(Temp).order_by(Temp.id.desc())
    temps = query.all()
    return render_template('index.html', temps=temps)


@app.route('/api/temp', methods=['GET', 'POST'])
def api_temp():
    if request.method == 'POST':
        if request.is_json:
            json = request.get_json(silent=True)
            if json is None:
                response = {'status': 'failure',
                            'error_message': 'Json empty or not valid'}
                return jsonify(response)
            values = api_temp_get_values(json)
            device = validate_device(values['mac'])
            session = validate_session(device)
            temp = create_temp(session, values)
            response = {'status': 'success'}
            return jsonify(response)
        else:
            response = {'status': 'failure',
                        'error_message': 'Must be application/json'}
            return jsonify(response)
    else:
        response = {'status': 'failure', 'message': 'Not yet implemented'}
        return jsonify(response)


@app.route('/api/temp/<int:id>', methods=['GET'])
def api_temp_id(id):
    try:
        temp = [temp for temp in temps if temp['id'] == id][0]
        response = {'status': 'succcess', 'data': temp}
    except:
        response = {'status': 'failure', 'error_message': 'Invalid id'}
    return jsonify(response)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def api_temp_get_values(json):
    values = {'mac': json['MAC'], 'temp_1': json['Temp1'],
              'temp_2': json['Temp2'], 'volts': json['Volts'],
              'mode': json['Mode'], 'runtime_seconds': json['Runtime(ms)']}
    return values


def validate_device(mac):
    query = db_session.query(Device).filter(Device.mac == mac)
    device = query.first()
    if device is None:
        device = create_device(mac)
    return device


def create_device(mac):
    device = Device(mac)
    db_session.add(device)
    db_session.commit()
    return device


def validate_session(device):
    query = db_session.query(Session).filter(Session.device_id == device.id,
                                             Session.completed.is_(None))
    session = query.first()
    if session is None:
        session = create_session(device)
    return session


def create_session(device):
    session = Session(device)
    db_session.add(session)
    db_session.commit()
    return session


def create_temp(session, values):
    temp = Temp(session, values['temp_1'], values['temp_2'], values['volts'],
                mode=values['mode'], runtime_seconds=values['runtime_seconds'])
    db_session.add(temp)
    db_session.commit()
    return temp
