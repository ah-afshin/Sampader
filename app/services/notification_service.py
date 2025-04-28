from repositories.notification_repo import get_notifications
from repositories.notification_repo import mark_notifications_as_read
from repositories.notification_repo import create_notification
from repositories.notification_repo import delete_notifications
from repositories.notification_repo import notif_num
from core.database import get_db
from core.logger import logger
from models.notification import Notification



async def fetch_notifications(user_id: str) -> list[Notification]:
    try:
        async with get_db() as session:
            return await get_notifications(session, user_id)
    except Exception as e:
        logger.error(f"services.notification_service.fetch_notifications: {e}")
        return []


async def get_notifications_number(userid: str) -> int | None:
    try:
        async with get_db() as session:
            return await notif_num(session, userid)
    except Exception as e:
        logger.error(f"services.notification_service.get_notifications_number: {e}")
        return None


async def mark_all_as_read(user_id: str) -> bool:
    try:
        async with get_db() as session:
            await mark_notifications_as_read(session, user_id)
            return True
    except Exception as e:
        logger.error(f"services.notification_service.mark_all_as_read: {e}")
        return False


async def send_notification(user_id: str, content: str, notif_type: str) -> bool:
    try:
        async with get_db() as session:
            await create_notification(session, user_id, content, notif_type)
            return True
    except Exception as e:
        logger.error(f"services.notification_service.send_notification: {e}")
        return False


async def clear_notifications(user_id: str) -> bool:
    try:
        async with get_db() as session:
            await delete_notifications(session, user_id)
            return True
    except Exception as e:
        logger.error(f"services.notification_service.clear_notifications: {e}")
        return False
