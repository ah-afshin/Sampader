from sqlalchemy.ext.asyncio import AsyncSession

from core.security import verify_password
from repositories.user_repo import get_user_by_username
from models.user import User



async def authenticate_user(session: AsyncSession, username: str, password: str) -> str | None:
    user = await get_user_by_username(session, username)
    if not user:
        return None

    if verify_password(password, user.password, user.password_salt):
        return user.userID
    return None
