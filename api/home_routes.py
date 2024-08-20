from flask import Blueprint, request, jsonify

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/api/test_home', methods=['GET'])
def test():
    return jsonify({"testing": "hello world!", "api": "home"}), 200
