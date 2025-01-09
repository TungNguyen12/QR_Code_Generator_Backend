import bcrypt

from bson.objectid import ObjectId
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Import configurations for JWT tokens
from src.config import JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRES, REFRESH_TOKEN_EXPIRES

import jwt

def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.

    Args:
        password: The password to hash (string).

    Returns:
        The hashed password as bytes.
    """
    # Hashes the password using bcrypt with a randomly generated salt.
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, password_hash: bytes) -> bool:
    """Verifies a password against a hashed password.

    Args:
        password: The password to verify (string).
        password_hash: The hashed password to compare against (bytes).

    Returns:
        True if the password matches the hash, False otherwise.
    """
    # Checks if the provided password matches the stored hash using bcrypt.
    return bcrypt.checkpw(password.encode('utf-8'), password_hash)

def generate_token(user_id: ObjectId, token_type: str = "access") -> str:
    """Generates a JWT (JSON Web Token) for a user.

    Args:
        user_id: The ID of the user for whom to generate the token (ObjectId).
        token_type: The type of token to generate, either "access" or "refresh" (string, default is "access").

    Returns:
        The generated JWT token as a string.
    """
    # Determine the token's expiration time based on its type.
    expiration_time: int = (
        ACCESS_TOKEN_EXPIRES if token_type == "access" else REFRESH_TOKEN_EXPIRES
    )

    # Define the payload of the token, including user ID and expiry time.
    payload: Dict[str, Any] = {
        "user_id": str(user_id),  # Convert ObjectId to string for serialization.
        "exp": datetime.utcnow() + timedelta(seconds=expiration_time) # Set expiration time for the token.
    }
    # Encode the payload into a JWT using the provided secret key and HS256 algorithm.
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> Optional[ObjectId]:
    """Decodes a JWT token and returns the user ID.

    Args:
        token: The JWT token to decode (string).

    Returns:
        The user ID as an ObjectId if the token is valid, None otherwise.
    """
    try:
        # Decode the JWT token using the secret key and HS256 algorithm.
        payload: Dict[str, Any] = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=["HS256"]
        )
         # Return the user ID as an ObjectId
        return ObjectId(payload["user_id"])
    except jwt.ExpiredSignatureError:
        # Return None if the token has expired.
        return None
    except jwt.InvalidTokenError:
        # Return None if the token is invalid for any other reason.
        return None
    
def is_token_expired(token: str) -> bool:
    """Checks if a JWT token is expired.

    Args:
        token: The JWT token to check (string).

    Returns:
        True if the token is expired, False otherwise.
    """
    try:
        # Try to decode the token. Will raise an ExpiredSignatureError if the token is expired
        jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        # Return False if no exception is raised
        return False
    except jwt.ExpiredSignatureError:
        # Return True if the token has expired.
        return True