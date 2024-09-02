from sqlalchemy import (
    String,
    Column,
    ForeignKey
)
from sqlalchemy.orm import relationship
import datetime
import database.helpers as helpers ###
from .constants import *
from .base import Base
from .associations import (
    followers_table,
    LikesTable,
    blocks_table
)





class User(Base):
    __tablename__ = "users"

    # unique, not to be duplicated
    userID = Column("userID", String(36), primary_key=True, default=helpers.generate_uuid)
    username = Column("username", String(MAX_USERNAME_LEN), unique=True)
    email = Column("email", String(MAX_EMAIL_LEN), unique=True)
    
    # pubilc details
    name = Column("name", String(MAX_NAME_LEN))
    bio = Column("bio", String(MAX_BIO_LEN))
    profile = Column("profile", String(40))
    banner = Column("banner", String(40))

    # profile details
    joined_date = Column("date", String(8))
    verified = Column("verified", String(1))
    school_and_class = Column("class", String)###

    # secret fields
    password = Column("password", String(MAX_PASSWORD_LEN))
    password_salt = Column("salt", String(32))

    # relations
    posts = relationship(
        "Post",
        back_populates="author"
    )
    likes = relationship(
        "Post",
        secondary=LikesTable,
        back_populates="likes"
    )
    followers = relationship(
        'User',
        secondary=followers_table,
        primaryjoin=userID == followers_table.c.followed_id,
        secondaryjoin=userID == followers_table.c.follower_id,
        backref="followings"
    )
    blockers = relationship(
        'User',
        secondary=blocks_table,
        primaryjoin=userID == blocks_table.c.blocked_id,
        secondaryjoin=userID == blocks_table.c.blocker_id,
        backref="blockings"
    )
    status = relationship(
        "UserStatus",
        back_populates="user",
        uselist=False
    )

    def __init__(self, username, email, name, bio, profile, banner, school_class, password, password_salt):
        if (
            (school_class in school_and_class) #and
            # helpers.profile_exists(profile) and
            # helpers.banner_exists(banner) #and
            # helpers.username_available(username, email)
        ):
            self.username = username
            self.email = email
            self.name = name
            self.bio = bio
            self.profile = profile
            self.school_and_class = school_class
            self.banner = banner
            self.password = password
            self.password_salt = password_salt
            self.joined_date = datetime.datetime.now().strftime("%Y%m%d")
            self.verified = "f"
    
    def __repr__(self):
        return f"<user {self.username}, id: '{self.userID}'>"

    def get_likes(self, n=5):
        return self.likes[-n:]


class Post(Base):
    __tablename__ = "posts"

    postID = Column("postID", String(36), primary_key=True, default=helpers.generate_uuid)
    date = Column("date", String(12)) # when was it posted
    text = Column("text", String(MAX_POST_LEN), nullable=False)
    
    # post category is going to be set by AI later.
    category = Column("category", String, nullable=True) #???
    # if the post has any attachments like image, video, etc it would be stored here
    contents = Column("contents", String(40), nullable=True)
    
    authorID = Column("authorID", String(36), ForeignKey("users.userID"), nullable=False)
    author = relationship(
        "User",
        back_populates="posts"
    )
    
    # if the post is a comment on another post, it would have a parent id
    parentID = Column("parentID", String(36), ForeignKey("posts.postID"), nullable=True)
    parent = relationship(
        "Post",
        remote_side=[postID]
    )

    likes = relationship(
        "User",
        secondary=LikesTable,
        back_populates="likes"
    )

    def __init__(self, author, text, parent=None, contents=None):
        self.author = author
        self.text = text
        self.date = datetime.datetime.now().strftime("%Y%m%d%H%M")
        if parent:
            self.parent = parent
        self.contents = contents
    
    def __repr__(self):
        return f"<post '{self.text[:6]}' by {self.author.username}>"


class UserStatus(Base):
    __tablename__ = "user_status"
    ID = Column("ID", String(36), ForeignKey("users.userID"), primary_key=True)
    # categories = Column("categories", String) ###
    lastseen = Column("lastseen", String(12))
    notifications = Column("notifs", String)
    user = relationship(
        "User",
        back_populates="status"
    )

    def __init__(self, userid):
        self.ID = userid
        self.lastseen = datetime.datetime.now().strftime("%Y%m%d%H%M")
        self.notifications = ""
