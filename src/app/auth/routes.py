from typing import Tuple, Dict

from flask import Blueprint, request, jsonify, Response

from src.app.auth.utils import decode_token, hash_password, verify_password, generate_token
from src.app.auth.models import create_user, find_user_by_email

auth = Blueprint('auth', __name__)

# Register route
@auth.route('/register', methods=['POST'])
def register() -> Tuple[Response, int]:
    """Registers a new user.

    Returns:
        A JSON response indicating the success or failure of the registration,
        along with the corresponding HTTP status code.
    """
    print('Received data:', request.json)
    data: Dict = request.json

    # Validate input
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "All fields are required"}), 400

    # Check if the user already exists
    if find_user_by_email(data['email']):
        return jsonify({"error": "User already exists"}), 400

    # Hash the password and create the user
    hashed_password: str = hash_password(data['password'])
    user_id: str = create_user(data['username'], data['email'], hashed_password)

    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

# Login route
@auth.route('/login', methods=['POST'])
def login() -> Tuple[Response, int]:
    """Logs in an existing user.

    Returns:
        A JSON response indicating the success or failure of the login, along
        with the corresponding HTTP status code.
    """
    data: Dict = request.json

    # Validate input
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    # Find the user by email
    user: Dict = find_user_by_email(data['email'])
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    # Verify the password
    if not verify_password(data['password'], user['password_hash']):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate a JWT
    access_token: str = generate_token(user['_id'])
    refresh_token: str = generate_token(user["_id"], token_type="refresh")

    print(f"Generated token: {access_token} 🔐 at login route")

    return jsonify({"message": "Login successful", "access_token": access_token, "refresh_token": refresh_token}), 200

# Generate access token with refresh token route  
@auth.route('/auth/refresh', methods=['POST'])
def refresh_token():
    """Refreshes an expired access token using a refresh token."""
    data = request.json
    refresh_token = data.get("refresh_token")
    
    # Decode the refresh token
    user_id = decode_token(refresh_token)
    if not user_id:
        return jsonify({"error": "Invalid or expired refresh token"}), 401

    # Issue a new access token
    new_access_token = generate_token(user_id)
    return jsonify({"access_token": new_access_token}), 200