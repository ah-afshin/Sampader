from sqlalchemy import ForeignKey, String, Column, delete, select
import db.constants as const


class Follow(const.Base):
    __tablename__ = "follows"
    followID = Column("followID", String, primary_key=True, default=const.generate_uuid)
    followerID = Column("follower", String, ForeignKey("users.userID"))
    followedID = Column("followed", String, ForeignKey("users.userID"))
     
    def __init__(self, follower, followed):        
        self.followerID = follower
        self.followedID = followed


def is_followed(follower, followed):
    # did follower user followed this guy?
    try:
        exist = len(
            const.session.query(Follow)
                .filter(Follow.followerID == follower, Follow.followedID == followed)
                .all()
            ) > 0
        return exist
    except:
        return False


def follow(follower, followed_user):
    # following someone:
    #    add a record to follows table
    if not is_followed(follower, followed_user):
        f = Follow(follower, followed_user)
        const.session.add(f)
        const.session.commit()
        return True
    return False


def unfollow(follower, followed_user):
    # unfollowing someone:
    #    remove a record from follows table
    if is_followed(follower, followed_user):
        query = delete(Follow).where(Follow.followedID == followed_user, Follow.followerID == follower)
        # print(query)
        const.session.execute(query)
        const.session.commit()
        return True
    return False


def followings(userid):
    # list of user's followed accounts
    query = select(Follow.followedID).where(Follow.followerID==userid)
    result = const.session.execute(query).all()
    return list(map(
        lambda a: a[0],
        result
    ))


def followers(userid):
    # list of user's followers
    query = select(Follow.followerID).where(Follow.followedID==userid)
    result = const.session.execute(query).all()
    return list(map(
        lambda a: a[0],
        result
    ))
