from typing import Tuple, Dict

from flask import Blueprint, request, jsonify, Response

from src.app.auth.utils import hash_password, verify_password, generate_token
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
    token: str = generate_token(user['_id'])

    print(f"Generated token: {token} 🔐 at login route")

    return jsonify({"message": "Login successful", "token": token}), 200