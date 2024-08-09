from sqlalchemy import ForeignKey, String, Column, delete, select, Table
import db.constants as const

# from db.user import User

# class Like(const.Base):
#     __tablename__ = "likes"
#     likeID = Column("likeID", String, primary_key=True, default=const.generate_uuid)
#     userID = Column("userID", String, ForeignKey("users.userID"))
#     postID = Column("postID", String, ForeignKey("posts.postID"))

#     def __init__(self, user, post):
#         self.userID = user
#         self.postID = post

# def is_liked(user, post):
#     # did this user liked this post?
#     try:
#         exist = len(
#             const.session.query(Like)
#                 .filter(Like.userID == user, Like.postID == post)
#                 .all()
#             ) > 0
#         return exist
#     except:
#         return False

# def add_like(user, post):
#     # to like a post by a user
#     #    add a record to likes table
#     if not is_liked(user, post):
#         l = Like(user, post)
#         const.session.add(l)
#         const.session.commit()
#         return True
#     return False

# def remove_like(user, post):
#     # to remove someuser's like on a post
#     #    remove a record from likes table
#     if is_liked(user, post):
#         query = delete(Like).where(Like.userID == user, Like.postID == post)
#         const.session.execute(query)
#         const.session.commit()
#         return True
#     return False

# def get_user_likes(user):
#     # list of user's liked posts
#     query = select(Like.postID).where(Like.userID == user)
#     result = const.session.execute(query).all()
#     return list(map(
#         lambda a: a[0],
#         result
#     ))

# def get_post_likes(post):
#     # list of users who liked this post
#     query = select(Like.userID).where(Like.postID == post)
#     result = const.session.execute(query).all()
#     return list(map(
#         lambda a: a[0],
#         result
#     ))



LikesTable = Table(
    "likes",
    const.Base.metadata,
    Column("userid", ForeignKey("users.userID")),
    Column("postid", ForeignKey("posts.postID"))
)
