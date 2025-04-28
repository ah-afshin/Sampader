from difflib import SequenceMatcher

from core.database import get_db



async def get_current_user(token: str) -> str | None:
    from core.security import verify_access_token
    from repositories.user_repo import get_user_by_userid

    user_id = verify_access_token(token)
    return user_id
    # if not user_id:
    #     return None
    
    # async with get_db() as session:
    #     return await get_user_by_userid(session, user_id)


def similarity(a: str, b: str) -> float:
    matcher = SequenceMatcher(None, a.lower(), b.lower())
    return matcher.ratio()
