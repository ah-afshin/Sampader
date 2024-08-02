from db import user
from db import block
from db import follow
from db import post
from db import like
import db.constants as const
print("database module was imported")

try:
    from db.user import User
    from db.post import Post
    const.Base.metadata.create_all(bind=const.engine)
    print("database initialized")
except Exception as e:
    print("data base error:")
    print(e)