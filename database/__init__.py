from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from .base import Base
from .models import User, Post, Notification
from .associations import LikesTable, followers_table, blocks_table



def shutdown_session():
    # session needs to be refreshed by each request
    # we are making instant session objects in `services`
    # and these sessions need to be removed
    Session.remove()



from configs import DATABASE_URI
engine = create_engine(DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine)) # instant session maker.
try:
    Base.metadata.create_all(bind=engine)
    print("database initialized successfully.")

except Exception as e:
    print("data base initialization error:")
    print("\t", e)
