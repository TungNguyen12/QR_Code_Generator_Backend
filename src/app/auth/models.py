from typing import Dict, Any, Optional
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
from bson.son import SON

# Import the function to get database connection
from src.db.database import get_db
from datetime import datetime

# Get the database instance
db = get_db()
# Access the 'users' collection from the database
users_collection = db['users']

# Find a user by email
def find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Finds a user by their email address.

    Args:
        email: The email address of the user to find (string).

    Returns:
        The user document as a dictionary if found, otherwise None.
    """
    # Query the 'users' collection to find a user with the given email.
    return users_collection.find_one({"email": email})

# Find a user by ID
def find_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Finds a user by their ID.

    Args:
        user_id: The ID of the user to find (string).

    Returns:
        The user document as a dictionary if found, otherwise None.
    """
    # Convert the user_id string to an ObjectId for MongoDB querying.
    # Queries the 'users' collection to find a user with the given _id.
    return users_collection.find_one({"_id": ObjectId(user_id)})

# Create a new user
def create_user(username: str, email: str, hashed_password: str) -> str:
    """Creates a new user.

    Args:
        username: The username of the new user (string).
        email: The email address of the new user (string).
        hashed_password: The hashed password of the new user (string).

    Returns:
        The ID of the newly created user as a string.
    """
    # Define the user document with the given information.
    user: Dict[str, Any] = {
        "username": username,
        "email": email,
        "password_hash": hashed_password,
        "created_at": datetime.utcnow() # Set the creation timestamp.
    }
    # Insert the new user document into the 'users' collection.
    result: InsertOneResult = users_collection.insert_one(user)
    # Return the newly inserted user's ID as a string.
    return str(result.inserted_id)