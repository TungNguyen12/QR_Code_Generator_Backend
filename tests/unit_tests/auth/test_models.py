from src.app.auth.models import create_user, find_user_by_email, find_user_by_id
from src.app.auth.utils import hash_password

def test_create_and_find_user():
    # Test user creation
    hashed_password = hash_password("secure_password")
    user_id = create_user("test_user", "test@example.com", hashed_password)

    # Test finding by email
    user = find_user_by_email("test@example.com")
    assert user is not None
    assert user["username"] == "test_user"
    assert user["email"] == "test@example.com"

    # Test finding by ID
    found_user = find_user_by_id(user_id)
    assert found_user is not None
    assert found_user["_id"] == user["_id"]
