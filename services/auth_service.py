import jwt
from datetime import datetime, timedelta
from sqlalchemy import select
from werkzeug.security import check_password_hash
from database import (
    User,
    Session
)


def check_user(username, password):
    session = Session()
    try:
        query = select(User.password, User.password_salt, User.userID).where(User.username==username) # a query to get password and passsalt of user
        hashed_password, salt, userid = session.execute(query).fetchone() # getting data
        return check_password_hash(hashed_password, password + salt), userid # checking password if it fits the user
    except Exception as e:
        # if the user doesn't exist.
        session.rollback()
        return False, ""


def new_token(userid:str, key:str):
    date = datetime.now()+timedelta(hours=24)
    data = {
        "id": userid,
        "ex": date.strftime("%Y%m%d%H")
    }
    return jwt.encode(data, key, algorithm="HS256")


def token_validate(token:str, key:str):
    try:
        now = datetime.now()
        data = jwt.decode(token, key, algorithms=["HS256"])
        if datetime.strptime(data["ex"], "%Y%m%d%H") > now:
            return True, data["id"]
        return False, "TOKEN_EXPIRED"
    except:
        return False, "INVALID_TOKEN"
