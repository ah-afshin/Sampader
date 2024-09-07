from flask import Blueprint, request, jsonify
from services import *


home_bp = Blueprint('home_bp', __name__)
from .constants import SECRET_KEY
from .post_routes import post_dto
from .user_routes import user_dto2

def notif_dto(notifObj, userid):
    actions = {"l": "like", "c": "comment", "f": "follow"}
    data = user_dto2(get_user_by_userid(notifObj.content), userid) if notifObj.notification_type=="f" else notifObj.content
    return {
        "user": notifObj.user_id,
        "action": actions[notifObj.notification_type],
        "data": data,
        "seen": False
    }


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
        seen(user)
        return jsonify([post_dto(p) for p in posts]), 200
    return "User not found (Invalid token)"


@home_bp.route('/api/notifications-number', methods=["POST", "GET"])
def notifnum_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    return str(get_notification_number(userid)), 200

@home_bp.route('/api/notifications', methods=["POST", "GET"])
def notif_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    return [notif_dto(i, userid) for i in get_notifications(userid)]
