import os
import dotenv


dotenv.load_dotenv()

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOADS_PATH = os.getenv("UPLOADS_PATH", os.path.join(BASE_DIR, "..", "uploads"))
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite+aiosqlite:///database.db") # "postgresql+asyncpg://<username>:<password>@localhost:5432/database"
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
    DEBUG = os.getenv("DEBUG", "True") == "True"
    LOGS_DIR = "logs"
    LOG_FILE = os.path.join(LOGS_DIR, "sampader.log")
