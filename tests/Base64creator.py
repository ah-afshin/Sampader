import base64

def image_to_base64(image_path):
    """Convert an image to a base64 string."""
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string


image_path = "C:/Users/Afshin/Desktop/roast/prof.jpg"
inp = image_to_base64(image_path)
with open('image_bas64.txt', 'a') as a:
    a.write(inp)
