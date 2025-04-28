from datetime import datetime
from datetime import UTC

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import exists
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from models import followers_table
from models import blocks_table
from core.dependencies import similarity



async def create_user(session: AsyncSession, **user_data) -> User | None:
    try:
        new_user = User(**user_data)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except Exception as e:
        await session.rollback()
        return None


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def get_user_by_userid(session: AsyncSession, userid: str) -> User | None:
    result = await session.execute(select(User).where(User.userID == userid))
    return result.scalars().first()


async def search_username(session: AsyncSession, username: str, limit: int=5) -> list[User]: # wtf?
    # query = await session.execute(select(User.username))
    # usernames = query.scalars().all()
    # scores = {name: similarity(username, name) for name in usernames}
    # sorted_scores = sorted(
    #     scores.items(),
    #     key = lambda x: x[1],
    #     reverse=True
    # )[:5]
    # return [get_user_by_username(session, item) for item, _ in sorted_scores]

    result = await session.execute( # postgreSQL required
        select(User)
        .where(
            User.username.op("%")(username)  # pg_trgm required
        )
        .order_by(
            func.similarity(User.username, username).desc()
        )
        .limit(limit)
    )
    return result.scalars().all()


# async def search_user_id(session: AsyncSession, userid: str) -> list[User]:
#     return ...


# async def search_name(session: AsyncSession, username: str) -> list[User]:
#     return ...


async def follow(
        session: AsyncSession,
        follower_id: str,
        followed_id: str
    ) -> None:
    query = followers_table.insert().values(follower_id=follower_id, followed_id=followed_id)
    await session.execute(query)
    await session.commit()


async def unfollow(
        session: AsyncSession,
        follower_id: str,
        followed_id: str
    ) -> None:
    query = followers_table.delete().where(
        (followers_table.c.follower_id == follower_id) &
        (followers_table.c.followed_id == followed_id)
    )
    await session.execute(query)
    await session.commit()


async def is_followed(
        session: AsyncSession,
        follower: str,
        followed: str
    ) -> bool:
    query = select(exists().where(
        (followers_table.c.follower_id == follower) &
        (followers_table.c.followed_id == followed)
    ))
    result = await session.execute(query)
    return result.scalar()


async def block(
        session: AsyncSession,
        blocker_id: str,
        blocked_id: str
    ) -> None:
    query = blocks_table.insert().values(blocker_id=blocker_id, blocked_id=blocked_id)
    await session.execute(query)
    await session.commit()


async def unblock(
        session: AsyncSession,
        blocker_id: str,
        blocked_id: str
    ) -> None:
    query = blocks_table.delete().where(
        (blocks_table.c.blocker_id == blocker_id) & (blocks_table.c.blocked_id == blocked_id)
    )
    await session.execute(query)
    await session.commit()


async def is_blocked(
        session: AsyncSession,
        blocker: str,
        blocked: str
    ) -> bool:
    query = select(exists().where(
        (blocks_table.c.blocker_id == blocker) &
        (blocks_table.c.blocked_id == blocked)
    ))
    result = await session.execute(query)
    return result.scalar()


# async def update_profile_info(
#         session: AsyncSession,
#         userid: str,
#         field: str,
#         value: str
#     ) -> None:
#     stmt = update(User).where(User.userID == userid).values({field: value})
#     await session.execute(stmt)
#     await session.commit()


async def update_profile_info(
        session: AsyncSession,
        user_id: str,
        **fields
    ) -> None:
    stmt = update(User).where(User.userID == user_id).values(**fields)
    await session.execute(stmt)
    await session.commit()


async def update_lastseen(session: AsyncSession, userid: str) -> None:
    stmt = update(User).where(User.userID == userid).values(lastseen=datetime.now(UTC))
    await session.execute(stmt)
    await session.commit()


async def verify(session: AsyncSession, userid: str, v_type: str) -> None:
    stmt = update(User).where(User.userID == userid).values(verified=v_type)
    await session.execute(stmt)
    await session.commit()
