from models import User
from repositories.user_repo import get_user_by_username
from repositories.user_repo import get_user_by_userid
from repositories.user_repo import search_username
from repositories.user_repo import is_followed
from repositories.user_repo import follow
from repositories.user_repo import unfollow
from repositories.user_repo import is_blocked
from repositories.user_repo import block
from repositories.user_repo import unblock
from repositories.user_repo import update_profile_info
from repositories.user_repo import verify
from repositories.notification_repo import create_notification
from services.media_service import save_image
from core.logger import logger
from core.database import get_db



async def get_by_userid(userid:str) -> User | None:
    try:
        async with get_db() as session:
            return await get_user_by_userid(session, userid)
    except Exception as e:
        logger.error(f"services.user_service.get_by_userid: {e}")
        return None


async def get_by_username(username:str) -> User | None:
    try:
        async with get_db() as session:
            return await get_user_by_username(session, username)
    except Exception as e:
        logger.error(f"services.user_service.get_by_username: {e}")
        return None


async def search_user(username: str) -> list[User]:
    try:
        async with get_db() as session:
            return await search_username(session, username)
    except Exception as e:
        logger.error(f"services.user_service.search_user: {e}")
        return []


# async def search_user_by_userid(userid: str) -> list[User]:
#     try:
#         async with get_db() as session:
#             return await search_user_id(session, userid)
#     except Exception as e:
#         logger.error(f"services.user_service.search_userid: {e}")
#         return []


# async def search_user_by_name(name: str) -> list[User]:
#     try:
#         async with get_db() as session:
#             return await search_name(session, name)
#     except Exception as e:
#         logger.error(f"services.user_service.search_user_by_name: {e}")
#         return []


async def follow_user(follower_id: str, followed_id: str) -> bool:
    try:
        async with get_db() as session:
            await follow(session, follower_id, followed_id)
            await create_notification(session, followed_id, f"{followed_id} followed you.", "follow")
            return True
    except Exception as e:
        logger.error(f"services.user_service.follow_user: {e}")
        return False


async def unfollow_user(follower_id: str, followed_id: str) -> bool:
    try:
        async with get_db() as session:
            await unfollow(session, follower_id, followed_id)
            return True
    except Exception as e:
        logger.error(f"services.user_service.unfollow_user: {e}")
        return False


async def is_user_followed(follower: str, followed: str) -> bool | None:
    try:
        async with get_db() as session:
            return await is_followed(session, follower, followed)
    except Exception as e:
        logger.error(f"services.user_service.is_user_followed: {e}")
        return None


async def block_user(blocker_id: str, blocked_id: str) -> bool:
    try:
        await unfollow_user(blocked_id, blocked_id)
        async with get_db() as session:
            await block(session, blocker_id, blocked_id)
            return True
    except Exception as e:
        logger.error(f"services.user_service.block_user: {e}")
        return False


async def unblock_user(blocker_id: str, blocked_id: str) -> bool:
    try:
        async with get_db() as session:
            await unblock(session, blocker_id, blocked_id)
            return True
    except Exception as e:
        logger.error(f"services.user_service.unblock_user: {e}")
        return False


async def is_user_blocked(blocker: str, blocked: str) -> bool | None:
    try:
        async with get_db() as session:
            return await is_blocked(session, blocker, blocked)
    except Exception as e:
        logger.error(f"services.user_service.is_user_blocked: {e}")
        return None


# async def change_profile_picture(userid: str, new_picture: str) -> None:
#     async with get_db() as session:
#         return await update_profile_info(session, userid, "profile", new_picture)


async def update_user_profile(user_id: str, **fields: dict) -> bool:
    try:
        async with get_db() as session:
            if "profile" in fields:
                done, img_id = save_image(fields["profile"], "profile")
                if not done:
                    logger.error(f"services.user_service.update_user_profile: failed to upload profile image.")
                    return False
                fields["profile"] = img_id
            
            if "banner" in fields:
                done, img_id = save_image(fields["banner"], "banner")
                if not done:
                    logger.error(f"services.user_service.update_user_profile: failed to upload banner image.")
                    return False
                fields["banner"] = img_id

            await update_profile_info(session, user_id, **fields)
            # logger.info(f"User {user_id} updated profile fields: {list(fields.keys())}")
            return True

    except Exception as e:
        logger.error(f"services.user_service.update_user_profile: {e}")
        return False


async def verify_user(user_id: str, v_type: str) -> bool:
    try:
        async with get_db() as session:
            await verify(session, user_id, v_type)
            return True
    except Exception as e:
        logger.error(f"services.user_service.verify_user: {e}")
        return False
