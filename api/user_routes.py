from flask import Blueprint, request, jsonify, send_file
from services import *
from database import User
from .post_routes import post_dto, comments_dto


user_bp = Blueprint('user_bp', __name__)
from .constants import *


def user_dto(userObj:User, userid:str):
    return {
        "id": userObj.userID,
        "username": userObj.username,
        "email": userObj.email,
        "name": userObj.name,
        "bio": userObj.bio,
        "profile": URL_PATH+"/profile/"+userObj.profile,
        "banner": URL_PATH+"/banner/"+userObj.banner,
        "joined_date": userObj.joined_date,
        "verified": userObj.verified,
        "school_and_class": userObj.school_and_class,
        "followers": len(userObj.followers),
        "followings": len(userObj.followings),
        # "block": [u.username for u in userObj.blockings], 
        "posts": [post_dto(post) for post in get_users_posts(userObj.userID)],
        "comment": [comments_dto(post) for post in get_users_comments(userObj.userID)],
        "likes": [post_dto(post) for post in userObj.get_likes()],
        "isfollowed": str(is_followed(userid, userObj.userID)),
        "isfollowing": str(is_followed(userObj.userID, userid))
    }


def user_dto2(userObj:User, userid:str):
    return {
        "id": userObj.userID,
        "username": userObj.username,
        "name": userObj.name,
        "profile": URL_PATH+"/profile/"+userObj.profile,
        "joined_date": userObj.joined_date,
        "verified": userObj.verified,
        "school_and_class": userObj.school_and_class,
        "followers": len(userObj.followers),
        "followings": len(userObj.followings),
        "isfollowed": str(is_followed(userid, userObj.userID)),
        "isfollowing": str(is_followed(userObj.userID, userid))
    }


@user_bp.route('/profile/<img>', methods=['GET'])
def profile_image(img):
    try:
        return send_file(UPLOADS_PATH+"/profile/"+img)
    except Exception as e:
        return f"Error: {e}", 500


@user_bp.route('/banner/<img>', methods=['GET'])
def banner_image(img):
    try:
        return send_file(UPLOADS_PATH+"/banner/"+img)
    except Exception as e:
        return f"Error: {e}", 500



@user_bp.route('/api/test_user', methods=['GET'])
def test():
    return jsonify({"testing": "hello world!", "api": "user"}), 200



@user_bp.route('/api/signup', methods=['POST'])
def sign_up_api():
    try:
        done, profile = new_profile_image(request.json["PROFILE"])
        if not done:
            return profile, 400
        done, banner = new_banner_image(request.json["BANNER"])
        if not done:
            return banner, 400

        done = new_user(
            request.json["USERNAME"],
            request.json["EMAIL"],
            request.json["NAME"],
            request.json["BIO"],
            profile,
            banner,
            request.json["CLASS"],
            request.json["PASSWORD"]
        )
        if done:
            return "User was successfully created.", 201
        return "Failed to creat the user.", 400
    except Exception as e:
        return f"Failed to creat the user. err: {str(e)}", 400
    


@user_bp.route('/api/search', methods=['POST'])
def search_api(): # and post
    term = request.json.get("SEARCH_TERM")
    if term:
        return jsonify(
            [user_dto2(get_user_by_username(i), "") for i in search_user(term)]
        ), 200
    return "Search term is required.", 400



@user_bp.route('/api/get_user', methods=['POST'])
def get_single_user_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401

    userid = request.json.get("ID")
    if userid:
        result = get_user_by_userid(userid)
        if result is None:
            return "User not found.", 404
        return jsonify(user_dto(result, userid)), 200
    return "User ID is required.", 400



@user_bp.route('/api/get_users', methods=['POST'])
def get_many_users_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401

    lst = request.json.get("USER_ID_LST")
    if lst:
        result = []
        for i in lst:
            user = get_user_by_userid(i)
            if user:
                result.append(user_dto(user, userid))
        return jsonify(result), 200
    return "User ID list is required.", 400



@user_bp.route('/api/get_follow', methods=['POST'])
def get_follow_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401

    username = request.json.get("USERNAME")
    if username:
        user = get_user_by_username(username)
        return jsonify({
            'followers': [user_dto(i, userid) for i in user.followers],
            'followings': [user_dto(i, userid) for i in user.followings]
        }), 200
    return "Username is required", 400



@user_bp.route('/api/follow', methods=['POST'])
def follow_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    
    followid = request.json['FOLLOW_ID']
    if followid is None:
        return "Follow ID is required.", 400

    if is_followed(userid, followid):
        unfollow(userid, followid)
        return "User was successfully unfollowed.", 200
    if follow(userid, followid):
        return "User was successfully followed.", 200
    return "Failed to follow user.", 400

    # if request.json.get('FOLLOW_ID') and follow(userid, request.json['FOLLOW_ID']):
    #     return "User was successfully followed.", 200
    # return "Failed to follow user.", 400



# @user_bp.route('/api/unfollow', methods=['POST'])
def unfollow_api(): ###
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    
    if request.json.get('FOLLOW_ID'):
        unfollow(userid, request.json['FOLLOW_ID'])
        return "User was successfully unfollowed.", 200
    return "Failed to unfollow user.", 400



@user_bp.route('/api/is_followed', methods=['POST'])
def is_followed_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    
    if request.json.get('FOLLOW_ID'):
        return str(is_followed(userid, request.json['FOLLOW_ID'])), 200
    return "Follow ID is required.", 400



@user_bp.route('/api/block', methods=['POST'])
def block_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401

    if is_blocked(userid, request.json['BLOCK_ID']):
        unblock(userid, request.json['BLOCK_ID'])
        return "User was successfully unblocked.", 200
    if block(userid, request.json['BLOCK_ID']):
        unfollow(userid, request.json['BLOCK_ID'])
        return "User was successfully blocked.", 200
    return "Failed to block user.", 400
    
    # if request.json.get('BLOCK_ID') and block(userid, request.json['BLOCK_ID']):
    #     return "User was successfully blocked.", 200
    # return "Failed to block user.", 400



# @user_bp.route('/api/unblock', methods=['POST'])
def unblock_api(): ###
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401

    if request.json.get('BLOCK_ID'):
        unblock(userid, request.json['BLOCK_ID'])
        return "User was successfully unblocked.", 200
    return "Failed to unblock user.", 400



@user_bp.route('/api/is_blocked', methods=['POST'])
def is_blocked_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    
    if request.json.get('BLOCK_ID'):
        return str(
            is_blocked(userid, request.json['BLOCK_ID'])
        ), 200
    return "Follow ID is required.", 400



@user_bp.route('/api/change_profile', methods=['POST'])
def change_account_detail_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401

    response = {}

    if request.json.get("NAME"):
        if update_name(userid, request.json["NAME"]):
            response["name"] = "Changed successfully."
        else:
            response["name"] = "Failed to change."

    if request.json.get("BIO"):
        if update_bio(userid, request.json["BIO"]):
            response["bio"] = "Changed successfully."
        else:
            response["bio"] = "Failed to change."

    if request.json.get("CLASS"):
        if update_class(userid, request.json["CLASS"]):
            response["class"] = "Changed successfully."
        else:
            response["class"] = "Failed to change."

    if request.json.get("PASSWORD"):
        if update_password(userid, request.json["PASSWORD"]):
            response["password"] = "Changed successfully."
        else:
            response["password"] = "Failed to change."

    if request.json.get("PROFILE"):
        done, profile = new_profile_image(request.json["PROFILE"])
        if done:
            if update_profile(userid, profile):
                response["profile"] = "Changed successfully."
        else:
            response["profile"] = "Failed to change."

    if request.json.get("BANNER"):
        done, banner = new_banner_image(request.json["BANNER"])
        if done:
            if update_banner(userid, banner):
                response["banner"] = "Changed successfully."
        else:
            response["banner"] = "Failed to change."

    return jsonify(response), 200
