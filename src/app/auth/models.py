from src.db.database import get_db
from datetime import datetime

db = get_db()
users_collection = db['users']  # Access the `users` collection

# Find a user by email
def find_user_by_email(email):
    return users_collection.find_one({"email": email})

# Find a user by ID
def find_user_by_id(user_id):
    from bson.objectid import ObjectId  # Import here to avoid circular imports
    return users_collection.find_one({"_id": ObjectId(user_id)})

# Create a new user
def create_user(username, email, hashed_password):
    user = {
        "username": username,
        "email": email,
        "password_hash": hashed_password,
        "created_at": datetime.utcnow()
    }
    result = users_collection.insert_one(user)
    return str(result.inserted_id)  # Return the new user's ID as a string
