# make sure directories exist
import os
from core.config import Config

if not os.path.exists(Config.LOGS_DIR):
    os.makedirs(Config.LOGS_DIR)

if not os.path.exists(Config.UPLOADS_PATH):
    os.makedirs(Config.UPLOADS_PATH)
    os.makedirs(os.path.join(Config.UPLOADS_PATH, "profile"))
    os.makedirs(os.path.join(Config.UPLOADS_PATH, "banner"))
    os.makedirs(os.path.join(Config.UPLOADS_PATH, "media"))


# init database
from models import init_models

if ...:
    ...
init_models()

# run the tests
import asyncio
from .tests import *

asyncio.run(test_signin())
asyncio.run(test_login())
asyncio.run(test_get_current_user())

# async def t():
#     from services import get_by_userid
#     u = await get_by_userid("575eb3d7-209b-4292-a6b5-108218f3c787")
#     print(u)
# asyncio.run(t())

# run the app

