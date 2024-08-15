from db import (
    user,
    post,
    associations,
    constants as __const
)

print("database module was imported")
try:
    __const.Base.metadata.create_all(bind=__const.engine)
    print("database initialized")
except Exception as e:
    print("data base initialization error:")
    print("\t", e)