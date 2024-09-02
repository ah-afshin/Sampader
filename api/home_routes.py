from flask import Blueprint, request, jsonify
from services import *


home_bp = Blueprint('home_bp', __name__)
from .constants import SECRET_KEY
from .post_routes import post_dto


@home_bp.route('/api/test_home', methods=['GET'])
def test():
    return jsonify({"testing": "hello world!", "api": "home"}), 200


@home_bp.route('/api/home', methods=["POST", "GET"])
def homepage_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401

    user = get_user_by_userid(userid)
    if user:
        posts = homepage_feed(user)
        return jsonify([post_dto(p) for p in posts]), 200
    return "User not found (Invalid token)"
