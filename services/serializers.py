from database import *
from .post_service import (
    get_users_posts,
    get_users_comments,
    get_comments
)
from .user_service import (
    get_user_by_userid,
    is_followed,
    is_blocked
)


def user_dto(userObj:User, userid:str, urlpath:str):
    if is_blocked(userObj.userID, userid):
        return {
            "id": userObj.userID,
            "username": userObj.username,
            "email": "unavailable.",
            "name": userObj.name,
            "bio": "this user has blocked you.",
            "profile": urlpath+"/profile/block.jpg",
            "banner": urlpath+"/banner/block.jpg",
            "joined_date": userObj.joined_date,
            "verified": userObj.verified,
            "school_and_class": userObj.school_and_class,
            "followers": 0,
            "followings": 0,
            "posts": [],
            "comment": [],
            "likes": [],
            "isfollowed": str(False),
            "isfollowing": str(False)
        }
    return {
        "id": userObj.userID,
        "username": userObj.username,
        "email": userObj.email,
        "name": userObj.name,
        "bio": userObj.bio,
        "profile": urlpath+"/profile/"+userObj.profile,
        "banner": urlpath+"/banner/"+userObj.banner,
        "joined_date": userObj.joined_date,
        "verified": userObj.verified,
        "school_and_class": userObj.school_and_class,
        "followers": len(userObj.followers),
        "followings": len(userObj.followings),
        "posts": [post_dto(post) for post in get_users_posts(userObj.userID)],
        "comment": [comments_dto(post) for post in get_users_comments(userObj.userID)],
        "likes": [post_dto(post) for post in userObj.get_likes()],
        "isfollowed": str(is_followed(userid, userObj.userID)),
        "isfollowing": str(is_followed(userObj.userID, userid))
    }


def user_dto2(userObj:User, userid:str, urlpath:str):
    return {
        "id": userObj.userID,
        "username": userObj.username,
        "name": userObj.name,
        "profile": urlpath+"/profile/"+userObj.profile,
        "joined_date": userObj.joined_date,
        "verified": userObj.verified,
        "school_and_class": userObj.school_and_class,
        "followers": len(userObj.followers),
        "followings": len(userObj.followings),
        "isfollowed": str(is_followed(userid, userObj.userID)),
        "isfollowing": str(is_followed(userObj.userID, userid))
    }


def post_dto(postObj:Post, urlpath:str):
    return {
        "text": postObj.text,
        "contents": [
            urlpath+"/media/"+postObj.contents if postObj.contents else "" # just an image yet.
        ],
        "date": postObj.date,
        "id": postObj.postID,
        "name": postObj.author.name,
        "user_id": postObj.author.userID,
        "username": postObj.author.username,
        "profile": postObj.author.profile,
        "verified": postObj.author.verified,
        "public_data": {
            "views": "0", ###
            "likes": len(postObj.likes),
            "comments": len(get_comments(postObj.postID))
        },
        "parent": "0", ###
        "category": str(postObj.category)
    }


def comments_dto(commentObj:Post, urlpath):
    return {
        "text": commentObj.text,
        "contents": [
            urlpath+"/media/"+commentObj.contents if commentObj.contents else "" # just an image yet.
        ],
        "date": commentObj.date,
        "id": commentObj.postID,
        "name": commentObj.author.name,
        "user_id": commentObj.author.userID,
        "username": commentObj.author.username,
        "profile": urlpath+"/profile/"+commentObj.author.profile,
        "verified": commentObj.author.verified,
        "public_data": {
            "views": "0", ###
            "likes": len(commentObj.likes),
            "comments": len(get_comments(commentObj.postID))
        },
        "parent": commentObj.parentID,
        "parent_data": post_dto(commentObj.parent) ###
    }


def notif_dto(notifObj, userid):
    actions = {"l": "like", "c": "comment", "f": "follow"}
    data = user_dto2(get_user_by_userid(notifObj.content), userid) if notifObj.notification_type=="f" else notifObj.content
    return {
        "user": notifObj.user_id,
        "action": actions[notifObj.notification_type],
        "data": data,
        "seen": False
    }
