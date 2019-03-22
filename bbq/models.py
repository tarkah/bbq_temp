from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from bbq.database import Base

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
    temps = relationship("Temp", primaryjoin="Temp.device_id==Device.id")

    def __init__(self, mac=None):
        self.mac = mac

    def __repr__(self):
        return '<Device {}>'.format(self.mac)

class Temp(Base):
    __tablename__ = 'temps'
    id = Column(Integer, primary_key=True)
    temp_1 = Column(Integer, nullable=False)
    temp_2 = Column(Integer, nullable=False)
    volts = Column(Float, nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    device = relationship(Device, primaryjoin=device_id == Device.id)

    def __init__(self, device_id=None, temp_1=None, temp_2=None, volts=None):
        self.device_id = device_id
        self.temp_1 = temp_1
        self.temp_2 = temp_2
        self.volts = volts

    def __repr__(self):
        return '<Temp {} - {}, {}>'.format(self.device.mac, self.temp_1, self.temp_2)
