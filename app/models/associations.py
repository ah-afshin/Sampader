from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey

from .base import Base



# Association table for the many-to-many self-referencing relationship in `User`
blocks_table = Table(
    'block',
    Base.metadata,
    Column('blocker_id', String, ForeignKey('users.userID'), primary_key=True),
    Column('blocked_id', String, ForeignKey('users.userID'), primary_key=True)
)


# Association table for the many-to-many self-referencing relationship in `User`
followers_table = Table(
    'follow',
    Base.metadata,
    Column('follower_id', String, ForeignKey('users.userID'), primary_key=True),
    Column('followed_id', String, ForeignKey('users.userID'), primary_key=True)
)


# Association table for the many-to-many relationship in `User` and `Post`
likes_table = Table(
    "likes",
    Base.metadata,
    Column("user_id", ForeignKey("users.userID")),
    Column("post_id", ForeignKey("posts.postID"))
)
