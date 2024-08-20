from flask import Blueprint, request, jsonify

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/api/test_user', methods=['GET'])
def test():
    return jsonify({"testing": "hello world!", "api": "user"}), 200
