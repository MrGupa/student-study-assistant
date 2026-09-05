from app.auth.password import hash_password, verify_password


def test_hash_password_returns_hash() -> None:
    password = "correct horse battery staple"

    hashed_password = hash_password(password)

    assert hashed_password
    assert hashed_password != password


def test_verify_password_returns_true_for_correct_password() -> None:
    password = "correct horse battery staple"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_returns_false_for_incorrect_password() -> None:
    password = "correct horse battery staple"
    hashed_password = hash_password(password)

    assert verify_password("wrong password", hashed_password) is False


def test_verify_password_returns_false_for_malformed_hash() -> None:
    assert verify_password("test password", "not-a-valid-password-hash") is False


def test_same_password_produces_different_hashes() -> None:
    password = "correct horse battery staple"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash
    assert verify_password(password, first_hash) is True
    assert verify_password(password, second_hash) is True
