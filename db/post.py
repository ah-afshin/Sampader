from sqlalchemy import (
    String,
    Column,
    ForeignKey,
    delete,
    or_,
    func,
)
from sqlalchemy.orm import relationship
import datetime, os
from db.associations import LikesTable
from db.user import get_user_by_userid
import db.constants as const



# helpers:
# checking for content if exists.
def media_exists(content):
    media_path = const.uploads_path + "/media"
    if content in os.listdir(media_path):
        return True
    return False



class Post(const.Base):
    __tablename__ = "posts"

    postID = Column("postID", String, primary_key=True, default=const.generate_uuid)
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
        if contents and media_exists(contents):
            self.contents = contents
    
    def __repr__(self):
        return f"<post '{self.text[:6]}' by {self.author.username}>"


def new_post(authorID, text, parentID=None, contents=None):
    # to add a post we add a record
    try:
        author = get_user_by_userid(authorID)
        parent = get_post(parentID)
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


def get_comments(postid):
    # Alias for counting likes
    likes_count = func.count(LikesTable.c.userid)

    # Query to get comments with like counts
    comments = (
        const.session.query(Post)
        .outerjoin(LikesTable, Post.postID == LikesTable.c.postid)  # Join with the likes table
        .filter(Post.parentID == postid)  # Filter by parent post ID
        .group_by(Post.postID)  # Group by the post ID to count likes per comment
        .order_by(likes_count.asc())  # Order by the count of likes, descending
        .all()
    )
    return comments


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


def get_post_likes(post):
    # list of users who liked this post
    post = const.session.query(Post).filter_by(postID=post).first()
    if post:
        return post.likes
    return False
