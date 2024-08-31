from .constants import UPLOADS_PATH
import os, uuid


# # does profile exist
# def profile_exists(profile):
#     profile_path = UPLOADS_PATH + "/profile"
#     if profile in os.listdir(profile_path):
#         return True
#     return False

# # does banner exist
# def banner_exists(banner):
#     banner_path = UPLOADS_PATH + "/banner"
#     if banner in os.listdir(banner_path):
#         return True
#     return False


# # checking for content if exists.
# def media_exists(content):
#     media_path = UPLOADS_PATH + "/media"
#     if content in os.listdir(media_path):
#         return True
#     return False


# generate random id
def generate_uuid():
    # length of result would be 36 characters
    return str(uuid.uuid4())
