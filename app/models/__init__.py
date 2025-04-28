from .base import Base
from .user import User
from .post import Post
from .notification import Notification
from .associations import blocks_table, followers_table, likes_table



def init_models():
    from core.database import engine
    import asyncio

    async def async_init():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(async_init())
