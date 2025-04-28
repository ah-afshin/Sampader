from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from models.notification import Notification



async def get_notifications(session: AsyncSession, user_id: str) -> list[Notification]:
    result = await session.execute(
        select(Notification).where(Notification.user_id == user_id, Notification.is_read == False)
    )
    return result.scalars().all()


async def mark_notifications_as_read(session: AsyncSession, user_id: str) -> None:
    query = update(Notification).where(Notification.user_id == user_id).values(is_read=True)
    await session.execute(query)
    await session.commit()


async def create_notification(session: AsyncSession, user_id: str, content: str, notif_type: str) -> None:
    notification = Notification(user_id=user_id, content=content, notification_type=notif_type)
    session.add(notification)
    await session.commit()


async def delete_notifications(session: AsyncSession, user_id: str) -> None:
    query = delete(Notification).where(Notification.user_id == user_id)
    await session.execute(query)
    await session.commit()


async def notif_num(session: AsyncSession, user_id: str) -> int: # wtf?
    result = await session.execute(
        select(Notification).where(Notification.user_id == user_id, Notification.is_read == False)
    )
    return len(result.scalars().all())
