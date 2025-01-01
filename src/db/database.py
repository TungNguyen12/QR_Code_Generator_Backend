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


users_collection = db["users"]

# Insert a test document
users_collection.insert_one({"username": "test", "email": "test@example.com"})

# Fetch the document
user = users_collection.find_one({"username": "test"})
print(user)

# Helper function to get the database instance
def get_db():
    return db

