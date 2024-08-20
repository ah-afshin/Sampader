from sqlalchemy import (
    String,
    Integer,
    Column,
    ForeignKey
)
from sqlalchemy.orm import relationship
import datetime
import database.helpers as helpers ###
from .constants import school_and_class
from .base import Base
from .associations import (
    followers_table,
    LikesTable,
    blocks_table
)




# def username_available(self, username, email):
#     session = Session()
#     # checking for similar email or username
#     return not session.query(
#         session.query(User).filter_by(username=username, email=email).exists()
#     ).scalar()



class User(Base):
    __tablename__ = "users"

    # unique, not to be duplicated
    userID = Column("userID", String, primary_key=True, default=helpers.generate_uuid)
    username = Column("username", String, unique=True)
    email = Column("email", String, unique=True)
    
    # pubilc details
    name = Column("name", String)
    bio = Column("bio", String)
    profile = Column("profile", String)
    banner = Column("banner", String)

    # profile details
    joined_date = Column("date", String)
    verified = Column("verified", Integer)
    school_and_class = Column("class", String)

    # secret fields
    password = Column("password", String)
    password_salt = Column("salt", String)

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

    def __init__(self, username, email, name, bio, profile, banner, school_class, password, password_salt):
        if (
            (school_class in school_and_class) and
            helpers.profile_exists(profile) and
            helpers.banner_exists(banner) #and
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
            self.verified = 0
    
    def __repr__(self):
        return f"<user {self.username}, id: '{self.userID}'>"



class Post(Base):
    __tablename__ = "posts"

    postID = Column("postID", String, primary_key=True, default=helpers.generate_uuid)
    date = Column("date", String) # when was it posted
    text = Column("text", String, nullable=False)
    
    # post category is going to be set by AI later.
    category = Column("category", String, nullable=True)
    # if the post has any attachments like image, video, etc it would be stored here
    contents = Column("contents", String, nullable=True)
    
    authorID = Column("authorID", String, ForeignKey("users.userID"), nullable=False)
    author = relationship(
        "User",
        back_populates="posts"
    )
    
    # if the post is a comment on another post, it would have a parent id
    parentID = Column("parentID", String, ForeignKey("posts.postID"), nullable=True)
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
        self.date = datetime.datetime.now().strftime("%Y%m%d")
        if parent:
            self.parent = parent
        if contents and helpers.media_exists(contents):
            self.contents = contents
    
    def __repr__(self):
        return f"<post '{self.text[:6]}' by {self.author.username}>"
