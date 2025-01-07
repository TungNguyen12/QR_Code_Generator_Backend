import os
from dotenv import load_dotenv

load_dotenv()


# ✅ Secret keys for JWT and encryption
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# ✅ JWT Token Expiry (in seconds)
ACCESS_TOKEN_EXPIRES = int(os.getenv("ACCESS_TOKEN_EXPIRES", 3600))
REFRESH_TOKEN_EXPIRES = int(os.getenv("REFRESH_TOKEN_EXPIRES", 86400))

# ✅ MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")

# ✅ Flask App Settings
DEBUG = os.getenv("DEBUG") == "True"  # Convert to boolean
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))