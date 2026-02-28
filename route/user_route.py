from flask import Blueprint, request, jsonify
from service.user_service import add_user, get_all_users

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    if not username:
        return jsonify({'message': 'Field username is required'}), 400
    if not email:
        return jsonify({'message': 'Field email is required'}), 400
    user, error = add_user(username, email)
    if error:
        return jsonify({'message': error}), 409
    return jsonify(user.to_dict()), 201

@user_bp.route('/users', methods=['GET'])
def list_users():
    users = get_all_users()
    return jsonify([u.to_dict() for u in users])
