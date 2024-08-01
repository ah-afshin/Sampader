# from db import user
# from db import block
# from db import follow
# from db import post
# from db import view
import db.constants as const
print("database module was imported")

const.Base.metadata.create_all(bind=const.engine)
print("database initialized")
