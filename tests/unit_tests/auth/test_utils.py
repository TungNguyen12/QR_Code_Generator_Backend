from src.app.auth.utils import hash_password, verify_password, generate_token, decode_token

def test_password_hashing():
    password = "my_secure_password"
    hashed_password = hash_password(password)
    assert verify_password(password, hashed_password) == True
    assert verify_password("wrong_password", hashed_password) == False

def test_jwt_token():
    user_id = "12345"
    token = generate_token(user_id)
    decoded_user_id = decode_token(token)
    assert decoded_user_id == user_id

    # Test expired token
    import time
    time.sleep(2)  # Simulate token expiration
    expired_token = generate_token(user_id)
    time.sleep(2)  # Expire token
    assert decode_token(expired_token) is None
