
from datetime import timedelta

import jwt
import pytest

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


def test_password_hashing_and_verification():
    password = "StrongPassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword123!", hashed)


def test_password_hashes_are_unique():
    password = "StrongPassword123!"

    hash_one = hash_password(password)
    hash_two = hash_password(password)

    assert hash_one != hash_two
    assert verify_password(password, hash_one)
    assert verify_password(password, hash_two)


def test_access_token_contains_correct_subject():
    token = create_access_token("1")

    payload = decode_access_token(token)

    assert payload["sub"] == "1"
    assert payload["type"] == "access"
    assert "exp" in payload
    assert "iat" in payload


def test_expired_token_is_rejected():
    token = create_access_token(
        "1",
        expires_delta=timedelta(seconds=-1),
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)


def test_invalid_token_signature_is_rejected():
    token = create_access_token("1")

    parts = token.split(".")
    parts[2] = ("A" if parts[2][0] != "A" else "B") + parts[2][1:]
    tampered_token = ".".join(parts)

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(tampered_token)


def test_invalid_token_is_rejected():
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token("this.is.not.a.valid.jwt")
