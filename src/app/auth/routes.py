from flask import Blueprint, request, jsonify
from db.database import users_collection
from app.auth.utils import hash_password, verify_password, generate_token
from app.auth.models import create_user, find_user_by_email

auth = Blueprint('auth', __name__)

#Register route
@auth.route('/register', methods=['POST'])
def register():
    print('Received data:', request.json)
    data = request.json

    # Validate input
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "All fields are required"}), 400

    # Check if the user already exists
    if find_user_by_email(data['email']):
        return jsonify({"error": "User already exists"}), 400

    # Hash the password and create the user
    hashed_password = hash_password(data['password'])
    user_id = create_user(data['username'], data['email'], hashed_password)

    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

#Login route
@auth.route('/login', methods=['POST'])
def login():
    data = request.json

    # Validate input
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    # Find the user by email
    user = find_user_by_email(data['email'])
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    # Verify the password
    if not verify_password(data['password'], user['password_hash']):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate a JWT
    token = generate_token(user['_id'])

    return jsonify({"message": "Login successful", "token": token}), 200
