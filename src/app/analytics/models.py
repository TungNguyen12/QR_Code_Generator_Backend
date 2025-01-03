from datetime import datetime
from typing import Any, Dict, List, Optional

from pymongo.results import InsertOneResult

from src.db.database import get_db

db = get_db()
scans_collection = db['scans']

def record_scan(qr_code_id: str, metadata: Dict[str, Any]) -> InsertOneResult:
    """Records a scan event with associated metadata.

    Args:
        qr_code_id: The ID of the scanned QR code.
        metadata: A dictionary containing additional metadata about the scan.

    Returns:
        The result of the insertion operation.
    """
    scan_data = {
        "qr_code_id": qr_code_id,
        "timestamp": datetime.utcnow(),
        **metadata  # Include additional metadata like user agent, location, etc.
    }
    return scans_collection.insert_one(scan_data)

def get_scans_by_qr_code(qr_code_id: str) -> List[Dict[str, Any]]:
    """Retrieves all scan events for a given QR code.

    Args:
        qr_code_id: The ID of the QR code.

    Returns:
        A list of dictionaries, where each dictionary represents a scan event.
    """
    scans = scans_collection.find({"qr_code_id": qr_code_id})

    return [
        {
            **scan,
            "_id": str(scan["_id"]),
            "qr_code_id": str(scan["qr_code_id"]),
        }
        for scan in scans
    ]

def get_total_scans_by_user(user_id: str) -> List[Dict[str, int]]:
    """Calculates the total number of scans for all QR codes owned by a user.

    Args:
        user_id: The ID of the user.

    Returns:
        A list containing a single dictionary with the total scan count.
    """
    # Aggregate scans for all QR codes owned by a user
    pipeline = [
        {"$lookup": {
            "from": "qrcodes",
            "localField": "qr_code_id",
            "foreignField": "_id",
            "as": "qr_code_details"
        }},
        {"$unwind": "$qr_code_details"},
        {"$match": {"qr_code_details.user_id": user_id}},
        {"$count": "total_scans"}
    ]
    result = list(scans_collection.aggregate(pipeline))

    return result if result else [{"total_scans": 0}]