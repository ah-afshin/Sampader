from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import exists
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from models.post import Post
from models.user import User
from models.associations import followers_table
from models.associations import likes_table
from core.dependencies import similarity



async def get_post(session: AsyncSession, post_id: str) -> Post | None:
    result = await session.execute(
        select(Post)
        .options(
            joinedload(Post.author),
            joinedload(Post.parent),
            joinedload(Post.likes)
        )
        .where(Post.postID == post_id)
    )
    return result.scalars().first()


async def create_post(session: AsyncSession, post: Post) -> None:
    session.add(post)
    await session.commit()


async def delete_post(session: AsyncSession, post_id: str) -> None:
    query = delete(Post).where(Post.postID == post_id)
    await session.execute(query)
    await session.commit()


async def get_preferred_posts(session: AsyncSession, user_id: str, limit: int = 10) -> list[Post]:
    result = await session.execute(select(User).where(User.userID == user_id))
    user = result.scalars().first()
    
    if not user:
        return []
    
    liked_categories = set(post.category for post in user.likes if post.category)
    query = select(Post).where(Post.category.in_(liked_categories)).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


async def get_posts_by_category(session: AsyncSession, category: str, limit: int) -> list[Post]:
    query = select(Post).where(Post.category == category).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


async def get_following_posts(session: AsyncSession, user_id: str, limit: int = 10) -> list[Post]:
    result = await session.execute(
        select(User.userID)
        .join(followers_table, followers_table.c.followed_id == User.userID)
        .where(followers_table.c.follower_id == user_id)
    )
    following_ids = [row[0] for row in result.all()]

    if not following_ids:
        return []

    query = select(Post).where(Post.authorID.in_(following_ids)).order_by(Post.date.desc()).limit(limit)
    result = await session.execute(query)

    return result.scalars().all()


async def users_posts(session: AsyncSession, userid: str, lim: int|None) -> list [Post]:
    query = select(Post).where(
            (Post.authorID == userid) &
            (Post.parentID == None)
        ).options(
            joinedload(Post.author),
            joinedload(Post.likes)
        ).order_by(Post.date.desc())
    if lim:
        query = query.limit(lim)
    
    result = await session.execute(query)
    return result.scalars().all()



async def users_comments(session: AsyncSession, userid: str, lim: int|None) -> list[Post]:
    query = select(Post).where(
            (Post.authorID == userid) &
            (Post.parentID != None)
        ).order_by(Post.date.desc())
    if lim:
        query = query.limit(lim)
    
    result = await session.execute(query)
    return result.scalars().all()


async def search_post_text(session: AsyncSession, txt: str, limit: int=10) -> list[Post]:
    result = await session.execute( # postgreSQL required
        select(Post)
        .where(
            Post.text.op("%")(txt)  # pg_trgm required
        )
        .order_by(
            func.similarity(Post.text, txt).desc()
        )
        .limit(limit)
    )
    return result.scalars().all()


async def get_post_comments(session: AsyncSession, postid: str, lim: int|None) -> list[Post]:
    query = select(Post).where(
            (Post.parentID == postid)
        ).order_by(Post.date.desc())
    if lim:
        query = query.limit(lim)
    
    result = await session.execute(query)
    return result.scalars().all()


async def like(session: AsyncSession, user_id: str, post_id: str) -> None:
    query = likes_table.insert().values(user_id=user_id, post_id=post_id)
    await session.execute(query)
    await session.commit()


async def unlike(session: AsyncSession, user_id: str, post_id: str) -> None:
    query = likes_table.delete().where(
        (likes_table.c.user_id == user_id) &
        (likes_table.c.post_id == post_id)
    )
    await session.execute(query)
    await session.commit()


async def is_post_liked(session: AsyncSession, user_id: str, post_id: str) -> None:
    query = select(exists().where(
        (likes_table.c.user_id == user_id) &
        (likes_table.c.post_id == post_id)
    ))
    result = await session.execute(query)
    return result.scalar()


async def post_likes(session: AsyncSession, postid: str, lim : int|None) -> list[User]:
    query = select(Post.likes).where(
            (Post.postID == postid)
        ).order_by(Post.date.desc())
    if lim:
        query = query.limit(lim)
    
    result = await session.execute(query)
    return result.scalars().all()
