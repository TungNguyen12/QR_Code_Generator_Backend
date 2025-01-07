import os
from pymongo import MongoClient

   
def get_db():
       """Returns a MongoDB database client."""
       uri = os.getenv("MONGODB_URI")
       print(f"MONGODB_URI: {uri}")
       client = MongoClient(uri)
       return client.get_database("qr_code_app")