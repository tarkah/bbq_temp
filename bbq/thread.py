import time
import datetime
from threading import Thread
from bbq.constants import TEMP_TIMEOUT
from bbq.database import db_session
from bbq.models import Session, Temp


def temp_timeout(db_session):
    while True:
        query = db_session.query(Session).filter(Session.completed.is_(None))
        sessions = query.all()
        for session in sessions:
            query = db_session.query(Temp).filter(
                Temp.session_id == session.id).order_by(Temp.sesssion_temp_id.desc())
            temp = query.first()
            delta = datetime.datetime.utcnow() - temp.created
            seconds = delta.seconds
            print('Session {}. Seconds since last temp update: {}'.format(
                session.id, seconds))
            if seconds > TEMP_TIMEOUT:
                session.completed = temp.created
                db_session.commit()
        time.sleep(10)


temp_thread = Thread(target=temp_timeout, args=(db_session,), daemon=True)
