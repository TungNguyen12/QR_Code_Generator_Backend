import bcrypt 
import jwt
from bson import ObjectId
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash)

def generate_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return ObjectId(payload["user_id"])
    except jwt.ExpiredSignatureError:
        return None
