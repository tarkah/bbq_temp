from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from bbq.database import Base, db_session


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'sqlite')
def sl_utcnow(element, compiler, **kw):
    return "DATETIME('now')"


class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    mac = Column(String, unique=True)
    created = Column(DateTime, nullable=False, default=utcnow())
    last_modified = Column(DateTime, onupdate=utcnow())
    sessions = relationship(
        "Session", primaryjoin="Session.device_id==Device.id")

    def __init__(self, mac=None):
        self.mac = mac

    def __repr__(self):
        return '<Device {} - {}>'.format(self.id, self.mac)

    @property
    def last_session(self):
        query = db_session.query(Session).filter(Session.device_id==self.id).order_by(Session.created.desc())
        session = query.first()
        return session


class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    device_session_id = Column(Integer, nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    device = relationship(Device, primaryjoin=device_id == Device.id)
    temps = relationship("Temp", primaryjoin="Temp.session_id==Session.id")
    created = Column(DateTime, nullable=False, default=utcnow())
    last_modified = Column(DateTime, onupdate=utcnow())
    completed = Column(DateTime)

    def __init__(self, Device=None):
        self.device_id = Device.id
        self.device_session_id = len(Device.sessions)+1

    def __repr__(self):
        return '<Session {}/{} - Device {}>'.format(self.id, self.device_session_id, self.device.id)


class Temp(Base):
    __tablename__ = 'temps'
    id = Column(Integer, primary_key=True)
    sesssion_temp_id = Column(Integer, nullable=False)
    temp_1 = Column(Integer, nullable=False)
    temp_2 = Column(Integer, nullable=False)
    volts = Column(Float, nullable=False)
    mode = Column(String)
    runtime_seconds = Column(Integer)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)
    session = relationship(Session, primaryjoin=session_id == Session.id)
    created = Column(DateTime, nullable=False, default=utcnow())
    last_modified = Column(DateTime, onupdate=utcnow())

    def __init__(self, Session=None, temp_1=None, temp_2=None, volts=None, **kwargs):
        self.session_id = Session.id
        self.sesssion_temp_id = len(Session.temps)+1
        self.temp_1 = temp_1
        self.temp_2 = temp_2
        self.volts = volts
        if 'mode' in kwargs:
            self.mode = kwargs['mode']
        if 'runtime_seconds' in kwargs:
            self.runtime_seconds = kwargs['runtime_seconds']

    def __repr__(self):
        return '<Temp {}/{} - Session {}>'.format(self.id, self.sesssion_temp_id, self.session_id)
