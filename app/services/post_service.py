from repositories.post_repo import create_post
from repositories.post_repo import delete_post
from repositories.post_repo import get_post
from repositories.post_repo import users_posts
from repositories.post_repo import users_comments
from repositories.post_repo import search_post_text
from repositories.post_repo import get_post_comments
from repositories.post_repo import like
from repositories.post_repo import unlike
from repositories.post_repo import is_post_liked
from repositories.post_repo import post_likes
from repositories.notification_repo import create_notification
from services.media_service import save_image
from core.database import get_db
from core.logger import logger
from models.post import Post
from models.user import User



async def new_post(author_id: str, text: str, parent_id=None, contents=None) -> Post | None:
    try:
        async with get_db() as session:
            # post category?
            post = Post(authorID=author_id, text=text, parentID=parent_id)
            
            if contents is not None:
                done, img_id = save_image(contents, "media")
                if not done:
                    logger.error(f"services.post_service.new_post: failed to upload media.")
                    return None
                post.contents = img_id

            await create_post(session, post)

            if parent_id is not None:
                parent_post = await get_post(session, parent_id)
                if parent_post.authorID != author_id:
                    await create_notification(session, parent_post.authorID, f"{author_id} commented on your post.", "comment")
            
            return post

    except Exception as e:
        logger.error(f"services.post_service.new_post: {e}")
        return None


async def find_post(post_id: str) -> Post | None:
    try:
        async with get_db() as session:
            return await get_post(session, post_id)
    except Exception as e:
        logger.error(f"services.post_service.find_post: {e}")
        return None


async def get_users_posts(userid: str, lim: int=None) -> list[Post]:
    try:
        async with get_db() as session:
            return await users_posts(session, userid, lim)
    except Exception as e:
        logger.error(f"services.post_service.get_users_posts: {e}")
        return []


async def get_users_comments(userid: str, lim: int=None) -> list[Post]:
    try:
        async with get_db() as session:
            return await users_comments(session, userid, lim)
    except Exception as e:
        logger.error(f"services.post_service.get_users_comments: {e}")
        return []


async def search_post(sttm: str) -> list[Post]:
    try:
        async with get_db() as session:
            return await search_post_text(session, sttm)
    except Exception as e:
        logger.error(f"services.post_service.search_post: {e}")
        return []


async def get_comments(postid: str, lim: int=None) -> list[Post]:
    try:
        async with get_db() as session:
            return await get_post_comments(session, postid, lim)
    except Exception as e:
        logger.error(f"services.post_service.get_comments: {e}")
        return []


async def remove_post(post_id: str, authorID: str) -> bool:
    try:
        async with get_db() as session:
            post:Post = await get_post(post_id)
            if authorID==post.authorID:
                await delete_post(session, post_id)
                return True
            else:
                return False
    except Exception as e:
        logger.error(f"services.post_service.remove_post: {e}")
        return False


async def like_post(userid: str, postid: str) -> bool:
    try:
        async with get_db() as session:
            await like(session, userid, postid)
            parent_post = await get_post(session, postid)
            if parent_post.authorID != userid:
                await create_notification(session, parent_post.authorID, f"{userid} liked your post.", "like")
            return True
    except Exception as e:
        logger.error(f"services.post_service.like_post: {e}")
        return False


async def unlike_post(userid: str, postid: str) -> bool:
    try:
        async with get_db() as session:
            await unlike(session, userid, postid)
            return True
    except Exception as e:
        logger.error(f"services.post_service.unlike_post: {e}")
        return False


async def is_liked(userid: str, postid: str) -> bool:
    try:
        async with get_db() as session:
            return await is_post_liked(session, userid, postid)
    except Exception as e:
        logger.error(f"services.post_service.unlike_post: {e}")
        return None


async def get_post_likes(postid: str) -> list[User]:
    try:
        async with get_db() as session:
            return await post_likes(session, postid)
    except Exception as e:
        logger.error(f"services.post_service.: {e}")
        return []
