from flask import Blueprint, request, jsonify, send_file
from database import Post
from services import *

post_bp = Blueprint('post_bp', __name__)
from .constants import *


def post_dto(postObj:Post):
    return {
        "text": postObj.text,
        "contents": [
            URL_PATH+"/media/"+postObj.contents if postObj.contents else "" # just an image yet.
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


def comments_dto(commentObj:Post):
    return {
        "text": commentObj.text,
        "contents": [
            URL_PATH+"/media/"+commentObj.contents if commentObj.contents else "" # just an image yet.
        ],
        "date": commentObj.date,
        "id": commentObj.postID,
        "name": commentObj.author.name,
        "user_id": commentObj.author.userID,
        "username": commentObj.author.username,
        "profile": URL_PATH+"/profile/"+commentObj.author.profile,
        "verified": commentObj.author.verified,
        "public_data": {
            "views": "0", ###
            "likes": len(commentObj.likes),
            "comments": len(get_comments(commentObj.postID))
        },
        "parent": commentObj.parentID,
        "parent_data": post_dto(commentObj.parent) ###
    }


@post_bp.route('/media/<img>', methods=['GET'])
def content_image(img):
    try:
        return send_file(UPLOADS_PATH+"/media/"+img)
    except Exception as e:
        return f"Error: {e}", 500



@post_bp.route('/api/test_post', methods=['GET'])
def test():
    return jsonify({"testing": "hello world!", "api": "post"}), 200



@post_bp.route('/api/create_post', methods=["POST"])
def create_post_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    
    text = request.json.get("POST_TEXT")
    if text is None:
        return "Text is required.", 400
    
    parentid = None if request.json.get("POST_PARENT")=="0" else request.json.get("POST_PARENT")
    content = None if request.json.get("POST_CONTENT")==[] else request.json.get("POST_CONTENT")[0]
    if new_post(userid, text, parentid, content):
        return "Post was successfully created.", 201
    return "Failed to create the post.", 400



@post_bp.route('/api/get_post', methods=["POST"])
def get_single_post_api():
    post = request.json.get("POST_ID")
    if post:
        result = get_post(post)
        if result is None:
            return "Post not found.", 404
        return jsonify(post_dto(result)), 200
    return "Post ID is required.", 400



@post_bp.route('/api/get_posts', methods=["POST"])
def get_many_posts_api():
    lst = request.json.get("POST_ID_LST")
    if lst:
        result = []
        for i in lst:
            post = get_post(i)
            if post:
                result.append(post_dto(post))
        return jsonify(result), 200
    return "Post ID list is required.", 400



@post_bp.route('/api/post_comments', methods=["POST"])
def get_post_comments_api():
    postid = request.json.get("POST_ID")
    if postid:
        res = [comments_dto(i) for i in get_comments(postid)]
        return jsonify(res), 200
    return "Post ID is required.", 400



@post_bp.route('/api/is_post_liked', methods=["POST"])
def is_post_liked_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    
    postid = request.json["POST_ID"]
    if postid is None:
        return "Post ID is required.", 400
    return str(is_liked(userid, postid))



@post_bp.route('/api/like', methods=["POST"])
def like_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    
    postid = request.json["POST_ID"]
    if postid is None:
        return "Post ID is required.", 400
    
    if is_liked(userid, postid):
        if remove_like(userid, postid):
            return "Post was successfully unliked.", 200
        return "Failed to unlike post.", 400
    if add_like(userid, postid):
        return "Post was successfully liked.", 200
    return "Failed to like post.", 400



@post_bp.route('/api/delete_post', methods=["POST"])
def delete_post_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    
    postid = request.json["POST_ID"]
    if postid is None:
        return "Post ID is required.", 400
    if get_post(postid).authorID == userid:
        if delete_post(postid):
            return "Post was successfully deleted", 200
        return "Failed to deleted the post.", 400
    return "You can delete your own posts only.", 403



# @post_bp.route('/api/', methods=["POST"])
def p():
    pass
