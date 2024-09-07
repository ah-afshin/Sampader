from .constants import UPLOADS_PATH
import os, uuid


# generate random id
def generate_uuid():
    # length of result would be 36 characters
    return str(uuid.uuid4())
