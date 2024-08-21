from services import new_profile_image, new_banner_image
import base64

def image_to_base64(image_path):
    """Convert an image to a base64 string."""
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string


image_path = "D:/temp/mosque.jpg"
inp = image_to_base64(image_path)
print(new_profile_image(inp))
print(new_banner_image(inp))
