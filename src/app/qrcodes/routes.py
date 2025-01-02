from flask import Blueprint, request, jsonify, send_file
from src.app.qrcodes.services import generate_qr_code
from src.app.qrcodes.models import delete_qr_code_by_id, save_qr_code, get_qr_codes_by_user
from src.app.auth.utils import decode_token

qrcodes = Blueprint('qrcodes', __name__)

#Authorized CREATE QR code
@qrcodes.route('/generate', methods=['POST'])
def generate_qr():
    print('Received data:', request.json)

    token = request.headers.get("Authorization").split(" ")[1]
    user_id = decode_token(token)

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    url = data.get("url")
    foreground_color = data.get("foreground_color", "#000000")
    background_color = data.get("background_color", "#ffffff")
    logo = request.files.get("logo")

    if not url:
        return jsonify({"Error: No URL provided"}), 400

    img_io = generate_qr_code(url, foreground_color, background_color, logo)
    qr_code_id = save_qr_code(user_id, url, foreground_color, background_color, None)

    print(f"Create new QR code 🧑🏻‍💻, {qr_code_id}")
    return send_file(img_io, mimetype='image/png')

#Authorized GET QR code
@qrcodes.route('/my_qrcodes', methods=['GET'])
def list_qr_codes():
    token = request.headers.get("Authorization").split(" ")[1]
    user_id = decode_token(token)

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    print(f"Your ID: {user_id} 🛂")

    qr_codes = get_qr_codes_by_user(user_id)

    print(f"Your QR codes are here 📃")
    return jsonify(qr_codes), 200

#Authorized DELETE QR code
@qrcodes.route('/qrcodes/<qr_code_id>', methods=['DELETE'])
def delete_qr_code(qr_code_id):
    token = request.headers.get("Authorization").split(" ")[1]
    user_id = decode_token(token)

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    result = delete_qr_code_by_id(qr_code_id, user_id)
    if result.deleted_count == 0:
        return jsonify({"error": "QR code not found or unauthorized"}), 404

    return jsonify({"message": "QR code deleted successfully"}), 200
