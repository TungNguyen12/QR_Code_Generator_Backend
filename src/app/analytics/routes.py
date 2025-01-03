from typing import Any, Dict, List, Tuple

from bson.objectid import ObjectId, InvalidId
from flask import Blueprint, jsonify, Response

from src.app.analytics.services import log_qr_code_scan
from src.app.analytics.models import get_scans_by_qr_code, get_total_scans_by_user

analytics = Blueprint('analytics', __name__)

@analytics.route('/scans/<qr_code_id>', methods=['POST'])
def record_scan(qr_code_id: str) -> Tuple[Response, int]:
    """Records a scan for the given QR code ID.

    Args:
        qr_code_id: The ID of the QR code that was scanned.

    Returns:
        A JSON response indicating the success or failure of the operation,
        along with the corresponding HTTP status code.
    """
    try:
        qr_code_id_obj: ObjectId = ObjectId(qr_code_id)  # Convert to ObjectId
    except InvalidId:
        return jsonify({"error": "Invalid QR Code ID"}), 400

    log_qr_code_scan(qr_code_id_obj)
    return jsonify({"message": "Scan recorded successfully"}), 201

@analytics.route('/analytics/<qr_code_id>', methods=['GET'])
def fetch_qr_code_analytics(qr_code_id: str) -> Tuple[Response, int]:
    """Fetches analytics data for a specific QR code.

    Args:
        qr_code_id: The ID of the QR code for which to fetch analytics.

    Returns:
        A JSON response containing the analytics data, along with the
        corresponding HTTP status code.
    """
    try:
        qr_code_id_obj: ObjectId = ObjectId(qr_code_id)
        scans: List[Dict[str, Any]] = get_scans_by_qr_code(qr_code_id_obj)
        return jsonify(scans), 200
    except InvalidId:
        return jsonify({"error": "Invalid QR Code ID"}), 400



@analytics.route('/analytics/user/<user_id>', methods=['GET'])
def fetch_user_analytics(user_id: str) -> Tuple[Response, int]:
    """Fetches analytics data for all QR codes owned by a user.

    Args:
        user_id: The ID of the user for whom to fetch analytics.

    Returns:
        A JSON response containing the total scan count, along with the
        corresponding HTTP status code.
    """
    try:
        user_id_obj: ObjectId = ObjectId(user_id)
        total_scans: List[Dict[str, int]] = get_total_scans_by_user(user_id_obj)
        return jsonify(total_scans), 200
    except InvalidId:
        return jsonify({"error": "Invalid User ID"}), 400