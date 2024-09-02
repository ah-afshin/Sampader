from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from . import constants, helpers
from .base import Base
from .models import User, Post , UserStatus
from .associations import LikesTable, followers_table, blocks_table



def shutdown_session(exception=None):
    # session needs to be refreshed by each request
    # we are making instant session objects in `services`
    # and these sessions need to be removed
    Session.remove()



# creating data base engine object
from .constants import DATABASE_URI
engine = create_engine(DATABASE_URI)
# this is an instant session maker.
Session = scoped_session(sessionmaker(bind=engine))
try:
    Base.metadata.create_all(bind=engine)
    print("database initialized successfully.")

except Exception as e:
    print("data base initialization error:")
    print("\t", e)










"""
### some other structure ###

# from flask import g
    # engine = create_engine(DATABASE_URI) # , echo=True?
    # Session = sessionmaker(bind=engine)
    # session = Session() # db_session = scoped_session(Session)?
    # Session = scoped_session(sessionmaker(bind=engine))
    # session = Session()

# def get_session():
#     if 'db_session' not in g:
#         g.db_session = Session()
#     return g.db_session
# def shutdown_session(exception=None):
#     db_session = g.pop('db_session', None)
#     if db_session is not None:
#         db_session.remove()
"""