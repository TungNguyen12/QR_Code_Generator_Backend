from typing import Any, Dict

from flask import request
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId

from src.app.analytics.models import record_scan

def log_qr_code_scan(qr_code_id: ObjectId) -> InsertOneResult:
    """Logs a QR code scan with metadata extracted from the request.

    Args:
        qr_code_id: The ID of the QR code that was scanned.

    Returns:
        The result of the insertion operation from record_scan function
    """
    metadata: Dict[str, Any] = {
        "user_agent": request.headers.get("User-Agent"),
        "ip_address": request.remote_addr
    }
    return record_scan(qr_code_id, metadata)