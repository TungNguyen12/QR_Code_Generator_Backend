from datetime import datetime
from typing import Dict, Any, List, Optional

from bson.objectid import ObjectId
from pymongo.results import InsertOneResult, DeleteResult

from src.db.database import get_db

db = get_db()
qrcodes_collection = db['qrcodes']

# Save QR code
def save_qr_code(
    user_id: ObjectId,
    url: str,
    foreground_color: str,
    background_color: str,
    logo_path: Optional[str] = None,
) -> str:
    """Saves a QR code to the database.

    Args:
        user_id: The ID of the user who created the QR code.
        url: The URL that the QR code points to.
        foreground_color: The foreground color of the QR code.
        background_color: The background color of the QR code.
        logo_path: The path to the logo image, if any.

    Returns:
        The ID of the newly created QR code as a string.
    """
    qr_code_data: Dict[str, Any] = {
        "user_id": user_id,
        "url": url,
        "foreground_color": foreground_color,
        "background_color": background_color,
        "logo_path": logo_path,
        "created_at": datetime.utcnow(),
    }
    result: InsertOneResult = qrcodes_collection.insert_one(qr_code_data)
    return str(result.inserted_id)

# Get QR codes by User
def get_qr_codes_by_user(user_id: ObjectId) -> List[Dict[str, Any]]:
    """Retrieves all QR codes created by a specific user.

    Args:
        user_id: The ID of the user.

    Returns:
        A list of dictionaries, where each dictionary represents a QR code.
    """
    qr_codes = qrcodes_collection.find({"user_id": user_id})
    return [
        {
            **qr_code,
            "_id": str(qr_code["_id"]),
            "user_id": str(qr_code["user_id"]),
        }
        for qr_code in qr_codes
    ]

# Delete QR code by ID
def delete_qr_code_by_id(qr_code_id: ObjectId, user_id: ObjectId) -> DeleteResult:
    """Deletes a QR code by its ID, ensuring the user making the request
       is the owner of the QR code.

    Args:
        qr_code_id: The ID of the QR code to delete.
        user_id: The ID of the user attempting to delete the QR code.

    Returns:
        The result of the delete operation.
    """
    return qrcodes_collection.delete_one(
        {"_id": qr_code_id, "user_id": user_id}
    )