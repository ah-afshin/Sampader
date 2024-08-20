from sqlalchemy import (
    delete,
    or_,
    func
)
from database import (
    Post,
    LikesTable,
    Session
)
from . import get_user_by_userid ###
# from .user_service import get_user_by_userid



def new_post(authorID, text, parentID=None, contents=None):
    session = Session()
    # to add a post we add a record
    try:
        author = get_user_by_userid(authorID)
        parent = get_post(parentID)
        p = Post(author, text, parent, contents)
        session.add(p)
        session.commit()
        return True
    except:
        session.rollback()
        return False


def get_post(postid):
    session = Session()
    return session.query(Post).filter(Post.postID == postid).first()


def get_users_posts(userid):
    session = Session()
    return session.query(Post).filter(Post.authorID == userid, Post.parentID == None).all()


def get_users_last_posts(userid, n):
    session = Session()
    return session.query(Post).filter(Post.authorID == userid, Post.parentID == None).order_by(Post.date.desc()).limit(n).all()


def get_last_posts(n):
    session = Session()
    return session.query(Post).filter(Post.parentID == None).order_by(Post.date.desc()).limit(n).all()


def get_comments(postid):
    session = Session()
    # Alias for counting likes
    likes_count = func.count(LikesTable.c.userid)

    # Query to get comments with like counts
    comments = (
        session.query(Post)
        .outerjoin(LikesTable, Post.postID == LikesTable.c.postid)  # Join with the likes table
        .filter(Post.parentID == postid)  # Filter by parent post ID
        .group_by(Post.postID)  # Group by the post ID to count likes per comment
        .order_by(likes_count.asc())  # Order by the count of likes, descending
        .all()
    )
    return comments


def delete_post(id):
    session = Session()
    # to delete a post we should delete a record
    try:
        query = delete(Post).where(or_(
            Post.postID == id, # delete the post
            Post.parentID == id # delete post's comments
        ))
        session.execute(query)
        session.commit()
        return True
    except:
        session.rollback()
        return False


def add_like(userid, postid):
    session = Session()
    # to add a like
    try:
        if not is_liked(userid, postid):
            post = session.query(Post).filter(Post.postID == postid).first()
            post.likes.append(get_user_by_userid(userid))
            session.commit()
            return True
        return False
    except:
        session.rollback()
        return False


def is_liked(userid, postid):
    session = Session()
    # did this user liked this post?
    return session.query(
        session.query(LikesTable).filter_by(postid=postid, userid=userid).exists()
    ).scalar()


def remove_like(user, post):
    session = Session()
    # to remove someuser's like on a post
    try:
        #    remove a record from likes table
        if session.query(LikesTable).filter_by(postid=post, userid=user).delete():
            session.commit()
            return True
        return False
    except:
        session.rollback()
        return False


def get_post_likes(post):
    session = Session()
    # list of users who liked this post
    post = session.query(Post).filter_by(postID=post).first()
    if post:
        return post.likes
    return False
