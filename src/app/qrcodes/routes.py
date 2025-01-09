from typing import Tuple, List, Dict, Any
from flask import Blueprint, request, jsonify, send_file, Response
from bson.objectid import ObjectId

from werkzeug.datastructures import FileStorage
from io import BytesIO

# Import QR code related services and data models
from src.app.qrcodes.services import generate_qr_code
from src.app.qrcodes.models import (
    delete_qr_code_by_id,
    save_qr_code,
    get_qr_codes_by_user,
)
# Import utility for decoding tokens
from src.app.auth.utils import decode_token
from pymongo.results import DeleteResult

# Define the blueprint for QR code related routes
qrcodes = Blueprint('qrcodes', __name__)

# Authorized CREATE QR code
@qrcodes.route('/generate', methods=['POST'])
def generate_qr() -> Tuple[Response, int]:
    """Generates and returns a QR code image.

    Requires an Authorization header with a valid JWT token.

    Returns:
        A tuple containing the QR code image file and the HTTP status code.
    """
    # Extract token from the Authorization header
    token: str = request.headers.get("Authorization").split(" ")[1]
    # Decode token to get user id
    user_id: Optional[ObjectId] = decode_token(token)

    # Return 401 if user is not authorized
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Get request data
    data: Dict[str, Any] = request.get_json()
    # Extract data from the request body.
    url: str = data.get("url")
    title: str = data.get("title", "")
    foreground_color: str = data.get("foreground_color", "#000000")
    background_color: str = data.get("background_color", "#ffffff")
    logo: FileStorage = request.files.get("logo")

    # Check if url is provided
    if not url:
        return jsonify({"Error: No URL provided"}), 400

    # Generate the QR code
    img_io: BytesIO = generate_qr_code(
        url, title, foreground_color, background_color, logo
    )
    # Save the QR code metadata and associate it to the user ID
    qr_code_id: str = save_qr_code(
        user_id, url, title, foreground_color, background_color, None
    )

    # Return the generated QR code image as a file response
    return send_file(img_io, mimetype='image/png', download_name=f'{qr_code_id}.png')

# Authorized GET QR code
@qrcodes.route('/my_qrcodes', methods=['GET'])
def list_qr_codes() -> Tuple[Response, int]:
    """Retrieves a list of QR codes associated with the authenticated user.

    Requires an Authorization header with a valid JWT token.

    Returns:
        A tuple containing the JSON response with the list of QR codes and
        the HTTP status code.
    """
    # Extract token from the Authorization header
    token: str = request.headers.get("Authorization").split(" ")[1]
    # Decode the token to get user ID
    user_id: Optional[ObjectId] = decode_token(token)

    # Return 401 if user is not authorized
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Fetch the list of QR codes associated with the user ID
    qr_codes: List[Dict[str, Any]] = get_qr_codes_by_user(user_id)

    # Return the list of QR codes as JSON response
    return jsonify(qr_codes), 200

# Authorized DELETE QR code
@qrcodes.route('/qrcodes/<qr_code_id>', methods=['DELETE'])
def delete_qr_code(qr_code_id: str) -> Tuple[Response, int]:
    """Deletes a specific QR code.

    Requires an Authorization header with a valid JWT token. The user can
    only delete QR codes they own.

    Args:
        qr_code_id: The ID of the QR code to delete (string).

    Returns:
        A tuple containing the JSON response and the HTTP status code.
    """
    # Extract token from the Authorization header
    token: str = request.headers.get("Authorization").split(" ")[1]
    # Decode the token to get user ID
    user_id: Optional[ObjectId] = decode_token(token)

    # Return 401 if user is not authorized
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Delete the QR code by ID, checking user ownership
    result: DeleteResult = delete_qr_code_by_id(ObjectId(qr_code_id), user_id)
    # Return 404 if QR code was not found or user is not authorized
    if result.deleted_count == 0:
        return jsonify({"error": "QR code not found or unauthorized"}), 404

    # Return a success message upon successful deletion
    return jsonify({"message": "QR code deleted successfully"}), 200