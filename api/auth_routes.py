from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/api/test_auth', methods=['GET'])
def test():
    return jsonify({"testing": "hello world!", "api": "auth"}), 200
