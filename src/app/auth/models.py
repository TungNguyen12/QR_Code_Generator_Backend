from typing import Dict, Any, Optional
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId



from src.db.database import get_db
from datetime import datetime

db = get_db()
users_collection = db['users']  # Access the `users` collection

# Find a user by email
def find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Finds a user by their email address.

    Args:
        email: The email address of the user to find.

    Returns:
        The user document if found, otherwise None.
    """ 
    return users_collection.find_one({"email": email})

# Find a user by ID
def find_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Finds a user by their ID.

    Args:
        user_id: The ID of the user to find.

    Returns:
        The user document if found, otherwise None.
    """
    
    return users_collection.find_one({"_id": ObjectId(user_id)})

# Create a new user
def create_user(username: str, email: str, hashed_password: str) -> str:
    """Creates a new user.

    Args:
        username: The username of the new user.
        email: The email address of the new user.
        hashed_password: The hashed password of the new user.

    Returns:
        The ID of the newly created user as a string.
    """
    user: Dict[str, Any] = {
        "username": username,
        "email": email,
        "password_hash": hashed_password,
        "created_at": datetime.utcnow()
    }
    result: InsertOneResult = users_collection.insert_one(user)
    return str(result.inserted_id)  # Return the new user's ID as a string