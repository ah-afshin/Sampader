from sqlalchemy import String, Integer, Column, ForeignKey, delete, or_
import db.constants as const
import datetime


class Post(const.Base):
    __tablename__ = "posts"

    postID = Column("postID", String, primary_key=True, default=const.generate_uuid)
    authorID = Column("authorID", String, ForeignKey("users.userID"))
    # when was it posted
    date = Column("date", String)
    text = Column("text", String)
    # post category is going to be set by AI later.
    category = Column("category", String, nullable=True)
    # if the post has any attachments like image, video, etc it would be stored here
    contents = Column("contents", String, nullable=True)
    # if the post is a comment on another post, it would have a parent id
    parentID = Column("parentID", String, ForeignKey("posts.postID"), nullable=True)
    # views = Column("views", Integer)
    likes = Column("views", Integer)
    def __init__(self, authorid, text, parentid=None, contents=None):
        self.authorID = authorid
        self.text = text
        self.date = datetime.datetime.now().strftime("%Y%m%d")
        self.views = 0
        self.likes = 0
        if parentid:
            self.parentID = parentid
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
        return False


def get_post(postid):
    return const.session.query(Post).filter(Post.postID == postid).first()


def get_users_posts(userid):
    return const.session.query(Post).filter(Post.authorID == userid, Post.parentID == None).all()


def get_users_last_posts(userid, n):
    return const.session.query(Post).filter(Post.authorID == userid, Post.parentID == None).order_by(Post.date.desc()).limit(n).all()


def get_last_posts(n):
    return const.session.query(Post).filter(Post.parentID == None).order_by(Post.date.desc()).limit(n).all()


def get_comments(postid):
    return const.session.query(Post).filter(Post.parentID == postid).order_by(Post.likes).all()


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
        return False
