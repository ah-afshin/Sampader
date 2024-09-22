import os
import base64
from io import BytesIO
from PIL import Image
from configs import UPLOADS_PATH
from database.models import generate_uuid



MAX_SIZE = (400, 400) # Maximum size for the banner and post-content images
MAX_SIZE_PROFILE = (200, 200) # Maximum size for the profile images



def resize_image(image, max_size):
    """Resize image maintaining the aspect ratio."""
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image



def new_profile_image(image_base64):
    try:
        # Decode the base64 image
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))
        # Resize the image
        image = resize_image(image, MAX_SIZE_PROFILE)
        # choose a name for image
        name = generate_uuid()+".jpg"
        # Save the image to the uploads directory
        save_path = os.path.join(UPLOADS_PATH+"/profile", name)
        image.save(save_path)
        return True, name
    except Exception as e:
        print(e)
        return False, "Failed to process and save the image"



def new_banner_image(image_base64):
    try:
        # Decode the base64 image
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))
        # Resize the image
        image = resize_image(image, MAX_SIZE)
        # choose a name for image
        name = generate_uuid()+".jpg"
        # Save the image to the uploads directory
        save_path = os.path.join(UPLOADS_PATH+"/banner", name)
        image.save(save_path)
        return True, name
    except Exception as e:
        print(e)
        return False, "Failed to process and save the image"



def new_content_image(image_base64):
    try:
        # Decode the base64 image
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))
        # Resize the image
        image = resize_image(image, MAX_SIZE)
        # choose a name for image
        name = generate_uuid()+".jpg"
        # Save the image to the uploads directory
        save_path = os.path.join(UPLOADS_PATH+"/media", name)
        image.save(save_path)
        return True, name
    except Exception as e:
        return False, "Failed to process and save the image"
