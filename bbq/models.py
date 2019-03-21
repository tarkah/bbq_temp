from sqlalchemy import Column, Integer, String, DateTime
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

    def __init__(self, mac=None):
        self.mac = mac

    def __repr__(self):
        return '<Device {}>'.format(self.mac)
