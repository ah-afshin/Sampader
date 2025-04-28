from collections import Counter
from random import shuffle

from repositories.post_repo import get_posts_by_category
from repositories.user_repo import get_user_by_userid
from repositories.user_repo import update_lastseen
from core.database import get_db
from repositories.post_repo import get_following_posts
from models.post import Post
from core.logger import logger



async def get_preferred_posts(user_id: str, limit: int = 10) -> list[Post]:
    async with get_db() as session:
        user = await get_user_by_userid(session, user_id)
        if not user:
            return []

        category_counts = Counter(post.category for post in user.likes if post.category)
        sorted_categories = [category for category, _ in category_counts.most_common()]

        posts = []
        for category in sorted_categories:
            category_posts = await get_posts_by_category(session, category, limit // len(sorted_categories))
            posts.extend(category_posts)

        return posts


def mix_lists_preserving_order(list1, list2) -> list:
    combined = [(1, elem) for elem in list1] + [(2, elem) for elem in list2]
    shuffle(combined)
    return [elem for _, elem in sorted(combined, key=lambda x: x[0])]


async def homepage_feed(user_id: str) -> list[Post]:
    try:
        async with get_db() as session:
            user = await get_user_by_userid(session, user_id)
            if not user:
                return []

            following_posts = await get_following_posts(session, user_id)
            preferred_posts = await get_preferred_posts(session, user)
            return mix_lists_preserving_order(following_posts, preferred_posts)

    except Exception as e:
        logger.error(f"services.home_service.homepage_feed: {e}")
        return []


async def update_last_seen(user_id: str) -> bool:
    try:
        async with get_db() as session:
            await update_lastseen(session, user_id)
        return True
    except Exception as e:
        logger.error(f"services.home_service.update_last_seen: {e}")
        return False
