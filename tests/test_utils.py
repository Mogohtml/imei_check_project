import pytest
from app.utils import check_imei, is_token_valid, is_user_allowed

def test_check_imei():
    imei = "123456789012345"
    result = check_imei(imei)
    assert result is not None

def test_is_token_valid():
    token = "valid_token_1"
    assert is_token_valid(token) == True
    token = "invalid_token"
    assert is_token_valid(token) == False

def test_is_user_allowed():
    user_id = 123456789
    assert is_user_allowed(user_id) == True
    user_id = 999999999
    assert is_user_allowed(user_id) == False
