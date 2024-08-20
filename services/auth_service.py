
from sqlalchemy import select
from werkzeug.security import check_password_hash
from database import (
    User,
    Session
    # get_session
)


def check_user(username, password):
    query = select(User.password, User.password_salt).where(User.username==username) # a query to get password and salt of user
    # session = get_session()
    session = Session()
    try:
        hashed_password, salt = session.execute(query).fetchone() # getting data
        return check_password_hash(hashed_password, password + salt) # checking password if it fits the user
    except Exception as e:
        # if the user doesn't exist there would be an error.
        session.rollback()
        return None
