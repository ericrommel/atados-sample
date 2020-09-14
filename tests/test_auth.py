import json

import pytest
from flask import session


def test_signup_view(auth):
    """
    Test that a sign up can be done
    """

    a_dict = dict(
        email="test@test.com",
        username="test",
        first_name="test",
        last_name="test",
        password="123456",
        is_admin=False,
    )
    response = auth.signup(a_dict)
    assert response.status_code == 201


def test_login_view(auth, client):
    """
    Test that a login can be done with right credentials
    """

    a_dict = dict(email="non-admin@admin.com", password="123456")
    response = auth.login(a_dict)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data.get("id") == 2
    assert data.get("email") == "non-admin@admin.com"
    assert data.get("first_name") == "First Name"
    assert data.get("last_name") == "Last Name"
    assert data.get("username") == "non-admin"
    assert data.get("is_admin") is False

    # Accessing context variables after the response
    with client:
        client.get("/")
        assert session["_user_id"] == "2"


@pytest.mark.parametrize(
    ("email", "password", "message"),
    (
        ("non-admin@admin.com", "654321", b"Invalid email or password."),
        ("123456", "non-admin@admin.com", b"Invalid email or password."),
    ),
)
def test_login_fail_view(auth, email, password, message):
    """
    Test that a login cannot be done with wrong credentials
    """

    a_dict = dict(email=email, password=password)
    response = auth.login(a_dict)
    assert response.status_code == 401
    assert message in response.data


def test_logout_without_login_before_view(auth):
    """
    Test that logout cannot be done without a login before
    """

    response = auth.logout()
    assert response.status_code == 401


def test_logout_with_login_before_view(auth):
    """
    Test that logout cannot be done without a login before
    """

    auth.login(dict(email="non-admin@admin.com", password="123456"))
    response = auth.logout()
    assert response.status_code == 200
