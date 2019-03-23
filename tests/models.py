import sys
sys.path.append("..")

from bbq.models import Device, Session, Temp
from bbq.database import db_session
from bbq.database import init_db

init_db()


d = Device('AABBCCDDEEFF')
d2 = Device('FFEEDDCCBBAA')
db_session.add(d)
db_session.add(d2)
db_session.commit()

d = db_session.query(Device).all()[0]
d2 = db_session.query(Device).all()[1]
s = Session(d)
s2 = Session(d2)
db_session.add(s)
db_session.add(s2)
db_session.commit()

d = db_session.query(Device).all()[0]
d2 = db_session.query(Device).all()[1]
s = Session(d)
s2 = Session(d2)
db_session.add(s)
db_session.add(s2)
db_session.commit()

s = db_session.query(Session).all()[0]
for x in range(0, 10):
    t = Temp(s, 150, 200, 5.55)
    db_session.add(t)
    db_session.commit()

s = db_session.query(Session).all()[1]
for x in range(0, 10):
    t = Temp(s, 150, 200, 5.55)
    db_session.add(t)
    db_session.commit()

sessions = db_session.query(Session).all()
print(sessions)

devices = db_session.query(Device).all()
print(devices)

temps = db_session.query(Temp).all()
print(temps)
