from sqlalchemy import String, Integer, Column, ForeignKey, delete, or_
from sqlalchemy.orm import relationship
from db.like import LikesTable
from db.user import get_user_by_userid
import db.constants as const
import datetime


class Post(const.Base):
    __tablename__ = "posts"

    postID = Column("postID", String, primary_key=True, default=const.generate_uuid)
    # when was it posted
    date = Column("date", String)
    text = Column("text", String)
    
    # post category is going to be set by AI later.
    category = Column("category", String, nullable=True)
    # if the post has any attachments like image, video, etc it would be stored here
    contents = Column("contents", String, nullable=True)
    
    authorID = Column("authorID", String, ForeignKey("users.userID"))
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

    # likes = Column("views", Integer)
    likes = relationship(
        "User",
        secondary=LikesTable,
        back_populates="likes"
    )

    def __init__(self, authorID, text, parentID=None, contents=None):
        self.authorID = authorID
        # self.author = author
        self.text = text
        self.date = datetime.datetime.now().strftime("%Y%m%d")
        # self.likes = 0
        if parentID:
            # self.parent = parent
            self.parentID = parentID
        if contents:
            self.contents = contents


def new_post(author, text, parent=None, contents=None):
    # to add a post we add a record
    try:
        p = Post(author, text, parent, contents)
        const.session.add(p)
        const.session.commit()
        return True
    except:
        const.session.rollback()
        return False


def get_post(postid):
    return const.session.query(Post).filter(Post.postID == postid).first()


def get_users_posts(userid):
    return const.session.query(Post).filter(Post.authorID == userid, Post.parentID == None).all()


def get_users_last_posts(userid, n):
    return const.session.query(Post).filter(Post.authorID == userid, Post.parentID == None).order_by(Post.date.desc()).limit(n).all()


def get_last_posts(n):
    return const.session.query(Post).filter(Post.parentID == None).order_by(Post.date.desc()).limit(n).all()


# needs update
def get_comments(postid):
    return const.session.query(Post).filter_by(parentID=postid).order_by(Post.likes).all()


# needs update
def delete_post(id):
    # to delete a post we should delete a record
    try:
        query = delete(Post).where(or_(
            Post.postID == id, # delete the post
            Post.parentID == id # delete post's comments
        ))
        const.session.execute(query)
        const.session.commit()
        return True
    except:
        const.session.rollback()
        return False

def add_like(userid, postid):
    # to add a like
    try:
        if not is_liked(userid, postid):
            post = const.session.query(Post).filter(Post.postID == postid).first()
            post.likes.append(get_user_by_userid(userid))
            const.session.commit()
            return True
        return False
    except:
        const.session.rollback()
        return False

def is_liked(userid, postid):
    # did this user liked this post?
    return const.session.query(
        const.session.query(LikesTable).filter_by(postid=postid, userid=userid).exists()
    ).scalar()

def remove_like(user, post):
    # to remove someuser's like on a post
    try:
        #    remove a record from likes table
        if const.session.query(LikesTable).filter_by(postid=post, userid=user).delete():
            const.session.commit()
            return True
        return False
    except:
        const.session.rollback()
        return False

# def get_user_likes(user):
#     # list of user's liked posts
#     query = select(Like.postID).where(Like.userID == user)
#     result = const.session.execute(query).all()
#     return list(map(
#         lambda a: a[0],
#         result
#     ))

def get_post_likes(post):
    # list of users who liked this post
    post = const.session.query(Post).filter_by(postID=post).first()
    return post.likes
