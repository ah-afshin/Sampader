from flask import Blueprint, request, jsonify
from services import *
from extensions import limiter


home_bp = Blueprint('home_bp', __name__)
from configs import SECRET_KEY
from .post_routes import post_dto
from .user_routes import user_dto2


@home_bp.route('/api/home', methods=["POST", "GET"])
@limiter.limit("10 per 12 hour")
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
@limiter.limit("20 per 1 hour")
def notifnum_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    return str(get_notification_number(userid)), 200


@home_bp.route('/api/notifications', methods=["POST", "GET"])
@limiter.limit("30 per 2 hour")
def notif_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    return [notif_dto(i, userid) for i in get_notifications(userid)]


@home_bp.route('/api/recommended-people', methods=["POST", "GET"])
@limiter.limit("10 per 1 hour")
def recommended_people_api():
    token = request.headers.get('Authorization')
    if token is None:
        return "Missing Authorization Header (JWT)", 401
    done, userid = token_validate(token.split()[1], SECRET_KEY)
    if not done:
        return "Your token in expired.", 401
    return [user_dto2(i, userid) for i in suggest_people(userid)], 200
