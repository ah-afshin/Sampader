from sqlalchemy import (
    select,
    update
)
from werkzeug.security import (
    generate_password_hash
)
import os
from database import (
    User,
    followers_table,
    blocks_table,
    Session,
)
from database.constants import (
    verified,
    school_and_class
)
from database.helpers import (
    profile_exists,
    banner_exists
)




# basic events with user class
def new_user(username, email, name, bio, profile, banner, school_class, password):
    try:
        session = Session()
        # password should be hashed
        salt = os.urandom(16)  # Generate a random salt
        password = generate_password_hash(password + salt.hex()) # hashing the password    
        # creating user
        user = User(username, email, name, bio, profile, banner, school_class, password, salt.hex())
        if user.name is not None:

            # if user was created succesfully
            session.add(user)
            session.commit()
            return True
        # if failed to create user
        return False
    except:
        session.rollback()
        return False
    
def search_user(username):
    session = Session()
    # getting usernames
    query = select(User.username)
    usernames = session.execute(query).fetchall()
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

def search_user_id(userID):
    session = Session()
    # getting userIDs
    query = select(User.userID)
    userIDs = session.execute(query).fetchall()
    scores = {}
    
    # comparing each username with ours.
    for i in userIDs:
        # similarity score
        count = 0
        # which one is shorter?
        min_len = min(len(userID), len(i[0]))
        
        for j in range(min_len):
            # if they have the same character in the same index
            count += 2 if userID[j] == i[0][j] else 0
            # if they just have same characters
            count += 1 if userID[j] in i[0] else 0
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
    session = Session()
    return session.query(User).filter(User.username == username).first()

def get_user_by_userid(userid):
    session = Session()
    return session.query(User).filter(User.userID == userid).first()



# events related to follow
def follow(follower, tobefollowed):
    session = Session()
    if not is_followed(follower, tobefollowed):
        user_a = session.query(User).filter_by(userID=follower).first()
        user_b = session.query(User).filter_by(userID=tobefollowed).first()
        if user_a and user_b:
            user_a.followings.append(user_b)
            session.commit()
            return True
    return False

def unfollow(follower, followed): # this function won't return anything or yell any error
    session = Session()
    session.query(followers_table).filter_by(follower_id=follower, followed_id=followed).delete()
    session.commit()

def is_followed(follower, followed):
    session = Session()
    return session.query(
        session.query(followers_table).filter_by(follower_id=follower, followed_id=followed).exists()
    ).scalar()

def followers(userid):
    session = Session()
    user = session.query(User).filter_by(userID=userid).first()
    return user.followers

def followings(userid):
    session = Session()
    user = session.query(User).filter_by(userID=userid).first()
    return user.followings



# events related to block
def block(blocker, tobeblocked):
    session = Session()
    if not is_blocked(blocker, tobeblocked):
        user_a = session.query(User).filter_by(userID=blocker).first()
        user_b = session.query(User).filter_by(userID=tobeblocked).first()
        if user_b and user_a:
            user_a.blockings.append(user_b)
            session.commit()
            return True
    return False

def unblock(blocker, blocked): # this function won't return anything or yell any error
    session = Session()
    session.query(blocks_table).filter_by(blocker_id=blocker, blocked_id=blocked).delete()
    session.commit()

def is_blocked(blocker, blocked):
    session = Session()
    return session.query(
        session.query(blocks_table).filter_by(blocker_id=blocker, blocked_id=blocked).exists()
    ).scalar()



# functions to update profile
def update_name(userid, name):
    session = Session()
    stmt = (
        update(User).
        where(User.userID == userid).
        values(name=name)
    )
    # Execute the update statement
    result = session.execute(stmt)
    # Commit the changes to the database
    session.commit()
    if result.rowcount > 0:
        return True
    return False

def update_bio(userid, bio):
    session = Session()
    stmt = (
        update(User).
        where(User.userID == userid).
        values(bio=bio)
    )
    # Execute the update statement
    result = session.execute(stmt)
    # Commit the changes to the database
    session.commit()
    if result.rowcount > 0:
        return True
    return False

def update_profile(userid, profile):
    session = Session()
    if profile_exists(profile):
        stmt = (
            update(User).
            where(User.userID == userid).
            values(profile=profile)
        )
        # Execute the update statement
        result = session.execute(stmt)
        # Commit the changes to the database
        session.commit()
        if result.rowcount > 0:
            return True
    return False

def update_banner(userid, banner):
    session = Session()
    if banner_exists(banner):
        stmt = (
            update(User).
            where(User.userID == userid).
            values(banner=banner)
        )
        # Execute the update statement
        result = session.execute(stmt)
        # Commit the changes to the database
        session.commit()
        if result.rowcount > 0:
            return True
    return False

def update_class(userid, school_class):
    session = Session()
    if school_class in school_and_class:
        stmt = (
            update(User).
            where(User.userID == userid).
            values(school_and_class=school_class)
        )
        # Execute the update statement
        result = session.execute(stmt)
        # Commit the changes to the database
        session.commit()
        if result.rowcount > 0:
            return True
    return False

def verify(userid, vtype):
    session = Session()
    if vtype in verified:
        stmt = (
            update(User).
            where(User.userID == userid).
            values(verified=vtype)
        )
        # Execute the update statement
        result = session.execute(stmt)
        # Commit the changes to the database
        session.commit()
        if result.rowcount > 0:
            return True
    return False

def update_password(userid, password):
    session = Session()
    # password should be hashed
    salt = os.urandom(16)  # Generate a random salt
    password = generate_password_hash(password + salt.hex()) # hashing the password
    stmt = (
        update(User).
        where(User.userID == userid).
        values(password=password, password_salt=salt.hex())
    )
    # Execute the update statement
    result = session.execute(stmt)
    # Commit the changes to the database
    session.commit()
    if result.rowcount > 0:
        return True
    return False






"""
### maybe here? ###
# def username_available(self, username, email):
#     session = Session()
#     # checking for similar email or username
#     return not session.query(
#         session.query(User).filter_by(username=username, email=email).exists()
#     ).scalar()"""
