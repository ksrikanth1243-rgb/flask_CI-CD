import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from bson.objectid import ObjectId
import mongomock
from app import app, mongo

@pytest.fixture
def client():
    app.config["TESTING"] = True
    # Overwrite the URI to an in-memory mock structure
    app.config["MONGO_URI"] = "mongodb://localhost:27017/testdb"
   
    # Force PyMongo to use the mock client wrapper
    mongo.cx = mongomock.MongoClient()
    mongo.db = mongo.cx.get_database("testdb")    

    with app.app_context():
        mongo.db.students.delete_many({})
        mongo.db.students.insert_one({
            "_id": ObjectId("66fddff25f4b5f6a0a123456"),
            "name": "Test Student",
            "email": "test@student.com",
            "course": "Flask"
        })

    with app.test_client() as client:
        yield client

    with app.app_context():
        mongo.db.students.delete_many({})
