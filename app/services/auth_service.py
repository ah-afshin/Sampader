from repositories.auth_repo import authenticate_user
from repositories.user_repo import get_user_by_username
from repositories.user_repo import create_user
from core.security import hash_password
from core.security import create_access_token
from core.database import get_db
from core.logger import logger



async def login_user(username: str, password: str) -> str | None:
    try:
        async with get_db() as session:
            userid = await authenticate_user(session, username, password)

            if not userid:
                return None

            return create_access_token(userid)
    except Exception as e:
        logger.error(f"services.auth_service.loggin_user: {e}")
        return None


async def register_user(
        username: str,
        email: str,
        password: str,
        name: str,
        bio: str="",
        profile: str="default.jpg",
        banner: str="default.jpg"
    ) -> tuple[bool, str]:
    try:
        async with get_db() as session:
            existing_user = await get_user_by_username(session, username)
            if existing_user:
                return False, "Username already taken"

            hashed_password, salt = hash_password(password)
            user_data = {
                "username": username,
                "email": email,
                "password": hashed_password,
                "password_salt": salt,
                "name": name,
                "bio": bio,
                "profile": profile,
                "banner": banner
            }

            new_user = await create_user(session, **user_data)
            if new_user:
                logger.info(f"User {username} registered successfully.")
                return True, create_access_token(new_user.userID)
            logger.info(f"failed to sign up {username}.")
            return False, "failed to sign up."

    except Exception as e:
        logger.error(f"services.auth_service.register_user: {e}")
        return False, f"Error: {str(e)}"
