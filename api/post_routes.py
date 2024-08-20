from flask import Blueprint, request, jsonify

post_bp = Blueprint('post_bp', __name__)

@post_bp.route('/api/test_post', methods=['GET'])
def test():
    return jsonify({"testing": "hello world!", "api": "post"}), 200
