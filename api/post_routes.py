from flask import Blueprint, request, jsonify, send_file
from database import Post
from services import *

post_bp = Blueprint('post_bp', __name__)
from .constants import UPLOADS_PATH, URL_PATH


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
