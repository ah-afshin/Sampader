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


# run the app

