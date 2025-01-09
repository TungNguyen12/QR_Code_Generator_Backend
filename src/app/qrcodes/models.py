from datetime import datetime
from typing import Dict, Any, List, Optional

from bson.objectid import ObjectId
from pymongo.results import InsertOneResult, DeleteResult

# Import database connection function
from src.db.database import get_db

# Get the database instance
db = get_db()
# Access the 'qrcodes' collection
qrcodes_collection = db['qrcodes']

# Save QR code
def save_qr_code(
    user_id: ObjectId,
    url: str,
    title: str,
    foreground_color: str,
    background_color: str,
    logo_path: Optional[str] = None,
) -> str:
    """Saves a QR code to the database.

    Args:
        user_id: The ID of the user who created the QR code (ObjectId).
        url: The URL that the QR code points to (string).
        title: The title associated with the QR code (string).
        foreground_color: The foreground color of the QR code (string).
        background_color: The background color of the QR code (string).
        logo_path: The path to the logo image, if any (string, optional).

    Returns:
        The ID of the newly created QR code as a string.
    """
    # Define the QR code document
    qr_code_data: Dict[str, Any] = {
        "user_id": user_id,
        "url": url,
        "title": title,
        "foreground_color": foreground_color,
        "background_color": background_color,
        "logo_path": logo_path,
        "created_at": datetime.utcnow(), # Add creation timestamp
    }
    # Insert the new QR code document into the collection
    result: InsertOneResult = qrcodes_collection.insert_one(qr_code_data)
    # Return the new QR code's ID as a string
    return str(result.inserted_id)

# Get QR codes by User
def get_qr_codes_by_user(user_id: ObjectId) -> List[Dict[str, Any]]:
    """Retrieves all QR codes created by a specific user.

    Args:
        user_id: The ID of the user (ObjectId).

    Returns:
        A list of dictionaries, where each dictionary represents a QR code.
    """
    # Query the database for all QR codes created by the given user_id
    qr_codes = qrcodes_collection.find({"user_id": user_id})
    # Transform the query results into a list of dictionaries, converting ObjectId fields into strings
    return [
        {
            **qr_code,
            "_id": str(qr_code["_id"]), # Convert ObjectId to string
            "user_id": str(qr_code["user_id"]), # Convert ObjectId to string
        }
        for qr_code in qr_codes
    ]

# Delete QR code by ID
def delete_qr_code_by_id(qr_code_id: ObjectId, user_id: ObjectId) -> DeleteResult:
    """Deletes a QR code by its ID, ensuring the user making the request
       is the owner of the QR code.

    Args:
        qr_code_id: The ID of the QR code to delete (ObjectId).
        user_id: The ID of the user attempting to delete the QR code (ObjectId).

    Returns:
        The result of the delete operation as a `DeleteResult` object.
    """
    # Delete the QR code document matching both the qr_code_id and user_id, ensuring ownership
    return qrcodes_collection.delete_one(
        {"_id": qr_code_id, "user_id": user_id}
    )