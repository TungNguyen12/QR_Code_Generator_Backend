from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = "mongodb://localhost:27017/"

# Create a connection to MongoDB
client = MongoClient(MONGO_URI)

# Access a specific database
db = client["qr_code_app"]

users_collection = db['users']
qrcodes_collection = db['qrcodes']
analytics_collection = db['analytics']

# Helper function to get the database instance
def get_db():
    return db

