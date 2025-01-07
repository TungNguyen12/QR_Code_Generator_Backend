import pytest
from src.app.auth.models import create_user, find_user_by_email, find_user_by_id
from src.db.database import get_db
from bson import ObjectId

# Fixture to clear the database before each test
@pytest.fixture(autouse=True)
def clear_database():
    db = get_db()
    db.users.delete_many({})


def test_create_user():
    user_id = create_user("testuser", "test@example.com", "hashedpassword")
    assert user_id is not None


def test_find_user_by_email():
    user_id = create_user("testuser", "test@example.com", "hashedpassword")

    user = find_user_by_email("test@example.com")
    assert user is not None
    assert user['username'] == "testuser"
    assert user["email"] == "test@example.com"


    user = find_user_by_email("nonexistent@example.com")
    assert user is None


def test_find_user_by_id():
    user_id = create_user("testuser", "test@example.com", "hashedpassword")

    user = find_user_by_id(user_id)
    assert user is not None
    assert user['username'] == "testuser"
    assert user["email"] == "test@example.com"

    # Check for the case where we are passing invalid objectID, we should get none.
    user = find_user_by_id(str(ObjectId())) # Generate a valid objectID, which will not correspond to an existing user, and test
    assert user is None