from sqlalchemy import (
    String,
    Integer,
    Column,
    select,
    update
)
from sqlalchemy.orm import relationship
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
import os, datetime
import db.constants as const
from db.associations import (
    followers_table,
    LikesTable,
    blocks_table
)



# helpers
# does profile exist
def profile_exists(profile):
    profile_path = const.uploads_path + "/profile"
    if profile in os.listdir(profile_path):
        return True
    return False
# does banner exist
def banner_exists(banner):
    banner_path = const.uploads_path + "/banner"
    if banner in os.listdir(banner_path):
        return True
    return False


class User(const.Base):
    __tablename__ = "users"

    # unique, not to be duplicated
    userID = Column("userID", String, primary_key=True, default=const.generate_uuid)
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

    def __username_available(self, username, email):
        # checking for similar email or username
        return not const.session.query(
            const.session.query(User).filter_by(username=username, email=email).exists()
        ).scalar()

    def __init__(self, username, email, name, bio, profile, banner, school_class, password, password_salt):
        if (
            (school_class in const.school_and_class) and
            profile_exists(profile) and
            banner_exists(banner) and
            self.__username_available(username, email)
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



# basic events with user class
def new_user(username, email, name, bio, profile, banner, school_class, password):
    # password should be hashed
    salt = os.urandom(16)  # Generate a random salt
    password = generate_password_hash(password + salt.hex()) # hashing the password    
    # creating user
    user = User(username, email, name, bio, profile, banner, school_class, password, salt.hex())
    if user.name is not None:

        # if user was created succesfully
        const.session.add(user)
        const.session.commit()
        return True
    # if failed to create user
    return False

def check_user(username, password):
    query = select(User.password, User.password_salt).where(User.username==username) # a query to get password and salt of user
    try:
        hashed_password, salt = const.session.execute(query).fetchone() # getting data
        return check_password_hash(hashed_password, password + salt) # checking password if it fits the user
    except Exception as e:
        # if the user doesn't exist there would be an error.
        const.session.rollback()
        return None
    
def search_user(username):
    # getting usernames
    query = select(User.username)
    usernames = const.session.execute(query).fetchall()
    scores = {}
    
    # comparing each username with ours.
    for i in usernames:
        # similarity score
        count = 0
        # which one is shorter?
        min_len = min(len(username), len(i[0]))
        
        for j in range(min_len):
            # if they have the same character in the same index
            count += 2 if username[j] == i[0][j] else 0
            # if they just have same characters
            count += 1 if username[j] in i[0] else 0
        # count is the similarity score of this username
        scores[i[0]] = count
    
    # choosing 3 top matches
    sorted_scores = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]
    closest_matches = [item[0] for item in sorted_scores]
    return closest_matches

def get_user_by_username(username):
    return const.session.query(User).filter(User.username == username).first()

def get_user_by_userid(userid):
    return const.session.query(User).filter(User.userID == userid).first()



# events related to follow
def follow(follower, tobefollowed):
    if not is_followed(follower, tobefollowed):
        user_a = const.session.query(User).filter_by(userID=follower).first()
        user_b = const.session.query(User).filter_by(userID=tobefollowed).first()
        if user_a and user_b:
            user_a.followings.append(user_b)
            const.session.commit()
            return True
    return False

def unfollow(follower, followed): # this function won't return anything or yell any error
    const.session.query(followers_table).filter_by(follower_id=follower, followed_id=followed).delete()
    const.session.commit()

def is_followed(follower, followed):
    return const.session.query(
        const.session.query(followers_table).filter_by(follower_id=follower, followed_id=followed).exists()
    ).scalar()

def followers(userid):
    user = const.session.query(User).filter_by(userID=userid).first()
    return user.followers

def followings(userid):
    user = const.session.query(User).filter_by(userID=userid).first()
    return user.followings



# events related to block
def block(blocker, tobeblocked):
    if not is_blocked(blocker, tobeblocked):
        user_a = const.session.query(User).filter_by(userID=blocker).first()
        user_b = const.session.query(User).filter_by(userID=tobeblocked).first()
        if user_b and user_a:
            user_a.blockings.append(user_b)
            const.session.commit()
            return True
    return False

def unblock(blocker, blocked): # this function won't return anything or yell any error
    const.session.query(blocks_table).filter_by(blocker_id=blocker, blocked_id=blocked).delete()
    const.session.commit()

def is_blocked(blocker, blocked):
    return const.session.query(
        const.session.query(blocks_table).filter_by(blocker_id=blocker, blocked_id=blocked).exists()
    ).scalar()



# functions to update profile
def update_name(userid, name):
    stmt = (
        update(User).
        where(User.userID == userid).
        values(name=name)
    )
    # Execute the update statement
    result = const.session.execute(stmt)
    # Commit the changes to the database
    const.session.commit()
    if result.rowcount > 0:
        return True
    return False

def update_bio(userid, bio):
    stmt = (
        update(User).
        where(User.userID == userid).
        values(bio=bio)
    )
    # Execute the update statement
    result = const.session.execute(stmt)
    # Commit the changes to the database
    const.session.commit()
    if result.rowcount > 0:
        return True
    return False

def update_profile(userid, profile):
    if profile_exists(profile):
        stmt = (
            update(User).
            where(User.userID == userid).
            values(profile=profile)
        )
        # Execute the update statement
        result = const.session.execute(stmt)
        # Commit the changes to the database
        const.session.commit()
        if result.rowcount > 0:
            return True
    return False

def update_banner(userid, banner):
    if banner_exists(banner):
        stmt = (
            update(User).
            where(User.userID == userid).
            values(banner=banner)
        )
        # Execute the update statement
        result = const.session.execute(stmt)
        # Commit the changes to the database
        const.session.commit()
        if result.rowcount > 0:
            return True
    return False

def update_class(userid, school_class):
    stmt = (
        update(User).
        where(User.userID == userid).
        values(school_and_class=school_class)
    )
    # Execute the update statement
    result = const.session.execute(stmt)
    # Commit the changes to the database
    const.session.commit()
    if result.rowcount > 0:
        return True
    return False

def verify(userid, vtype):
    stmt = (
        update(User).
        where(User.userID == userid).
        values(verified=vtype)
    )
    # Execute the update statement
    result = const.session.execute(stmt)
    # Commit the changes to the database
    const.session.commit()
    if result.rowcount > 0:
        return True
    return False

def update_password(userid, password):
    # password should be hashed
    salt = os.urandom(16)  # Generate a random salt
    password = generate_password_hash(password + salt.hex()) # hashing the password
    stmt = (
        update(User).
        where(User.userID == userid).
        values(password=password, password_salt=salt.hex())
    )
    # Execute the update statement
    result = const.session.execute(stmt)
    # Commit the changes to the database
    const.session.commit()
    if result.rowcount > 0:
        return True
    return False


def get_user_likes(userid):
    # list of posts which this user liked
    user = const.session.query(User).filter_by(userID=userid).first()
    if user:
        return user.likes
    return False
