import os
from uuid import uuid4
import base64

from io import BytesIO
from PIL import Image
from PIL import UnidentifiedImageError

from core.config import Config
from core.logger import logger



generate_uuid = lambda: str(uuid4())

MAX_SIZES = {
    "profile": (200, 200),
    "banner": (400, 400),
    "media": (400, 400)
}


def resize_image(image: Image, max_size: tuple[int]) -> Image:
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image


def save_image(image_base64: str, category: str) -> tuple[bool, str]:
    try:
        if category not in MAX_SIZES:
            return False, "Invalid category"

        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))

        image = resize_image(image, MAX_SIZES[category])
        name = f"{generate_uuid()}.jpg"
        save_path = os.path.join(Config.UPLOADS_PATH, category, name)
        image.save(save_path)

        return True, name
    except (UnidentifiedImageError, Exception) as e:
        logger.error(f"services.media_service.save_image: {e}")
        return False, f"Failed to process image: {e}"
