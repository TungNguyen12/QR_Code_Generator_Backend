from datetime import datetime
from src.db.database import get_db
from bson.objectid import ObjectId

db = get_db()
qrcodes_collection = db['qrcodes']

#Save QR code
def save_qr_code(user_id, url, foreground_color, background_color, logo_path=None):
    qr_code_data = {
        "user_id": user_id,
        "url": url,
        "foreground_color": foreground_color,
        "background_color": background_color,
        "logo_path": logo_path,
        "created_at": datetime.utcnow()
    }
    result = qrcodes_collection.insert_one(qr_code_data)
    return str(result.inserted_id)

#Get QR codes by User
def get_qr_codes_by_user(user_id):
    qr_codes = qrcodes_collection.find({"user_id": user_id})
    return [
        {
            **qr_code,
            "_id": str(qr_code["_id"]),
            "user_id": str(qr_code["user_id"]),
        }
        for qr_code in qr_codes
    ]

#Delete QR code by ID
def delete_qr_code_by_id(qr_code_id, user_id):
    return qrcodes_collection.delete_one({"_id": ObjectId(qr_code_id), "user_id": user_id})