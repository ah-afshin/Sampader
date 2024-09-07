from sqlalchemy import (
    select,
    update,
    delete
)
from database import (
    Notification,
    Session
)
from database.constants import (
    notification_type
)


def new_notification(userid, content, ntype):
    session = Session()
    # to add a post we add a record
    try:
        if ntype in notification_type:
            n = Notification(userid, content, ntype)
            session.add(n)
            session.commit()
            return True
        return False
    except: #Exception as e:
        # print(e)
        session.rollback()
        return False


def delete_notification(id): ###
    session = Session()
    # to delete a post we should delete a record
    try:
        query = delete(Notification).where(
            Notification.id == id
        )
        session.execute(query)
        session.commit()
        return True
    except:
        session.rollback()
        return False


def delete_all_notifications(userid):
    session = Session()
    # to delete a post we should delete a record
    try:
        query = delete(Notification).where(
            Notification.user_id == userid
        )
        session.execute(query)
        session.commit()
        return True
    except:
        session.rollback()
        return False


def get_notifications(userid):
    session = Session()
    result = session.query(Notification).filter(Notification.user_id == userid).all()
    delete_all_notifications(userid) ###
    return result


def get_notification_number(userid):
    session = Session()
    return len(
        session.query(Notification)
        .filter(Notification.user_id == userid)
        .all()
    )
