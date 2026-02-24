from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["veltrix"]

def get_db():
    return db
