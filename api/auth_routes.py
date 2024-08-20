from flask import Blueprint, request, jsonify
import services as s



auth_bp = Blueprint('auth_bp', __name__)
SECRET_KEY = "smpd9561"



@auth_bp.route('/api/test_auth', methods=['GET'])
def test():
    return jsonify({"testing": "hello world!", "api": "auth"}), 200



@auth_bp.route('/api/signin', methods=["POST"])
def signin():
    username = request.json['username']
    password = request.json['password']
    done, userid = s.check_user(username, password)
    if done:
        token = s.new_token(userid, SECRET_KEY)
        return {'token': token}, 200
    return "Wrong password.", 401



# token : token = auth\_header.split(" ")\[1\] if " " in auth\_header else auth\_header
# token : token = request.headers.get('Authorization')