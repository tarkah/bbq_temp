import time
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from flask_bootstrap import Bootstrap
from bbq.database import db_session
from bbq.models import Device, Session, Temp
from bbq.constants import TEMP_TIMEOUT, LOCAL_TZ

app = Flask('bbq')
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    query = db_session.query(Device)
    devices = query.all()
    return render_template('index.html', devices=devices)


@app.route('/session/<int:id>', methods=['GET'])
def session(id):
    query = db_session.query(Session).filter(Session.id==id)
    session = query.first()
    return render_template('temps.html', session=session)


@app.route('/device/<int:id>', methods=['GET'])
def device(id):
    query = db_session.query(Device).filter(Device.id==id)
    device = query.first()
    sessions = device.sessions
    return render_template('device.html', device=device, sessions=sessions)


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
    response = {'status': 'failure', 'error_message': 'Not yet implemented'}
    return jsonify(response)


@app.route('/api/session/<int:id>', methods=['GET'])
def api_session(id):
    query = db_session.query(Session).filter(Session.id==id)
    _session = query.first()
    session = _session.asdict()
    response = {'status': 'success', 'data': {'session': session}}
    return jsonify(response)


@app.route('/api/session/<int:id>/temps', methods=['GET'])
def api_session_temps(id):
    query = db_session.query(Session).filter(Session.id==id)
    _session = query.first()
    _temps = _session.temps
    session = _session.asdict()
    temps = [temp.asdict() for temp in _temps[::-1]]
    response = {'status': 'success', 'data': {'session': session, 'temps': temps}}
    return jsonify(response)


@app.route('/api/session/<int:id>/temps/last', methods=['GET'])
def api_session_last_temp(id):
    query = db_session.query(Session).filter(Session.id==id)
    _session = query.first()
    session = _session.asdict()
    temps = [_session.last_temp.asdict()]
    response = {'status': 'success', 'data': {'session': session, 'temps': temps}}
    return jsonify(response)

@app.route('/api/devices', methods=['GET'])
def api_devices():
    query = db_session.query(Device).all()
    devices = [device.asdict() for device in query[::-1]]
    response = {'status': 'success', 'data': {'devices': devices}}
    return jsonify(response)


@app.route('/api/devices/<int:id>/sessions', methods=['GET'])
def api_device_sessions(id):
    query = db_session.query(Session).filter(Session.device_id==id)
    sessions = [session.asdict() for session in query[::-1]]
    response = {'status': 'success', 'data': {'sessions': sessions}}
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
