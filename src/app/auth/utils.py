import bcrypt
import jwt
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from src.config import JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRES, REFRESH_TOKEN_EXPIRES

def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.

    Args:
        password: The password to hash.

    Returns:
        The hashed password as bytes.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, password_hash: bytes) -> bool:
    """Verifies a password against a hashed password.

    Args:
        password: The password to verify.
        password_hash: The hashed password to compare against.

    Returns:
        True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), password_hash)

def generate_token(user_id: ObjectId, token_type: str = "access") -> str:
    """Generates a JWT token for a user.

    Args:
        user_id: The ID of the user for whom to generate the token.

    Returns:
        The generated JWT token as a string.
    """
    expiration_time = (
        ACCESS_TOKEN_EXPIRES if token_type == "access" else REFRESH_TOKEN_EXPIRES
    )

    payload: Dict[str, Any] = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(seconds=expiration_time)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> Optional[ObjectId]:
    """Decodes a JWT token and returns the user ID.

    Args:
        token: The JWT token to decode.

    Returns:
        The user ID if the token is valid, None otherwise.
    """
    try:
        payload: Dict[str, Any] = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=["HS256"]
        )
        return ObjectId(payload["user_id"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:  # Catch a more general exception for invalid tokens
        return None
    
def is_token_expired(token: str) -> bool:
    """Check if the token is expired."""
    try:
        jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return False
    except jwt.ExpiredSignatureError:
        return True