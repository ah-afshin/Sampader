import logging

from core.config import Config



logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(Config.LOG_FILE, encoding="utf-8"),
        # logging.StreamHandler()  # show it in console
    ]
)

logger = logging.getLogger("SampaderLogger")
