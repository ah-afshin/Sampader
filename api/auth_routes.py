from flask import Blueprint, request, jsonify
import services as s



auth_bp = Blueprint('auth_bp', __name__)
from .constants import SECRET_KEY


@auth_bp.route('/api/test_auth', methods=['GET'])
def test():
    return jsonify({"testing": "hello world!", "api": "auth"}), 200



@auth_bp.route('/api/signin', methods=["POST"])
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



# token : token = auth\_header.split(" ")\[1\] if " " in auth\_header else auth\_header
# token : token = request.headers.get('Authorization')