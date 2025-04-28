import os
import jwt
from datetime import datetime
from datetime import timedelta
from datetime import UTC

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from core.config import Config



def hash_password(password: str) -> tuple[str, str]:
    salt = os.urandom(16)  # Generate a random salt
    password = generate_password_hash(password + salt.hex()) # hashing the password
    return password, salt.hex()


def verify_password(password: str, hashed_password: str, salt: str) -> bool:
    return check_password_hash(hashed_password, password + salt)


def create_access_token(user_id: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"id": user_id, "exp": expire}
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")


def verify_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload["id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
