import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from bson.objectid import ObjectId
from app import app, mongo


@pytest.fixture
def client():
    app.config["TESTING"] = True

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
