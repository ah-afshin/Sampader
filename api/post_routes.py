from flask import Blueprint, request, jsonify, send_file
from services import *
import threading
from extensions import limiter


post_bp = Blueprint('post_bp', __name__)
from .constants import *


@post_bp.route('/media/<img>', methods=['GET'])
@limiter.limit("1/second")
def content_image(img):
    try:
        return send_file(UPLOADS_PATH+"/media/"+img)
    except Exception as e:
        return f"Error: {e}", 500



@post_bp.route('/api/create_post', methods=["POST"])
@limiter.limit("50 per 1 hour")
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
    done, postid = new_post(userid, text, parentid, content)
    if done:
        if parentid is not None:
            # its a comment
            new_notification(get_post(parentid).authorID, userid, "c")
        thread = threading.Thread(target=handle_post_category, kwargs={"postid": postid})
        thread.start()
        return "Post was successfully created.", 201
    return "Failed to create the post.", 400



@post_bp.route('/api/get_post', methods=["POST"])
@limiter.limit("60 per 1 hour")
def get_single_post_api():
    post = request.json.get("POST_ID")
    if post:
        result = get_post(post)
        if result is None:
            return "Post not found.", 404
        return jsonify(post_dto(result, URL_PATH)), 200
    return "Post ID is required.", 400



@post_bp.route('/api/get_posts', methods=["POST"])
@limiter.limit("60 per 1 hour")
def get_many_posts_api():
    lst = request.json.get("POST_ID_LST")
    if lst:
        result = []
        for i in lst:
            post = get_post(i)
            if post:
                result.append(post_dto(post, URL_PATH))
        return jsonify(result), 200
    return "Post ID list is required.", 400



@post_bp.route('/api/post_comments', methods=["POST"])
@limiter.limit("100 per 1 hour")
def get_post_comments_api():
    postid = request.json.get("POST_ID")
    if postid:
        res = [comments_dto(i, URL_PATH) for i in get_comments(postid)]
        return jsonify(res), 200
    return "Post ID is required.", 400



@post_bp.route('/api/is_post_liked', methods=["POST"])
@limiter.limit("1 per 1 second")
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
@limiter.limit("3 per 5 second")
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
        new_notification(get_post(postid).authorID, userid, "l")
        return "Post was successfully liked.", 200
    return "Failed to like post.", 400



@post_bp.route('/api/delete_post', methods=["POST"])
@limiter.limit("1 per 2 second")
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
