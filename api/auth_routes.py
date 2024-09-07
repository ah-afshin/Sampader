from flask import Blueprint, request, jsonify
import services as s
from extensions import limiter


auth_bp = Blueprint('auth_bp', __name__)
from .constants import SECRET_KEY



@auth_bp.route('/api/signin', methods=["POST"])
@limiter.limit("24 per 12 hour")
def signin():
    username = request.json.get('USERNAME')
    password = request.json.get('PASSWORD')
    if username and password:
        done, userid = s.check_user(username, password)
        if done:
            token = s.new_token(userid, SECRET_KEY)
            return {'token': token}, 200
        return "Wrong password.", 400
    return "Username and password needed.", 400
