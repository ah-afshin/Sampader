from sqlalchemy import String, Integer, Column, select
from werkzeug.security import generate_password_hash, check_password_hash
import db.constants as const
import os, datetime


class User(const.Base):
    __tablename__ = "users"

    # unique, not to be duplicated
    userID = Column("userID", String, primary_key=True, default=const.generate_uuid)
    username = Column("username", String)
    email = Column("email", String)
    
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

    # does profile exist
    def __profile_exists(self, profile):
        profile_path = const.uploads_path + "/profile"
        if profile in os.listdir(profile_path):
            return True
        return False
    
    # does banner exist
    def __banner_exists(self, banner):
        banner_path = const.uploads_path + "/banner"
        if banner in os.listdir(banner_path):
            return True
        return False
    
    # checking for similar email or username
    def __username_available(self, username, email):
        try:
            exist = len(
                const.session.query(User)
                    .filter(User.username == username or User.email == email)
                    .all()
                ) > 0
            return not exist
        except:
            return True   

    def __init__(self, username, email, name, bio, profile, banner, school_class, password, password_salt):
        if (
            (school_class in const.school_and_class) and
            self.__profile_exists(profile) and
            self.__banner_exists(banner) and
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
