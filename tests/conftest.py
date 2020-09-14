import json
import os
import string
from random import choice

import pytest
from flask import url_for

from src import create_app, db
from src.models import Action, User, Volunteer


def get_url(app, url, next_url=None, id=None):
    with app.test_request_context():
        return url_for(url, next=next_url, id=id)


class AuthActions(object):
    def __init__(self, app, client):
        self._app = app
        self._client = client

    def signup(self, a_dict):
        """
        Sign up request
        """

        return self._client.post(
            get_url(app=self._app, url="auth.signup"),
            data=json.dumps(a_dict),
            content_type="application/json",
            follow_redirects=True,
        )

    def login(self, a_dict):
        """
        Logo in request
        """

        return self._client.post(
            get_url(app=self._app, url="auth.login"),
            data=json.dumps(a_dict),
            content_type="application/json",
            follow_redirects=True,
        )

    def logout(self):
        """
        Log out request
        """

        return self._client.get(get_url(app=self._app, url="auth.logout"), follow_redirects=True)

    def generic_put(self, url, a_dict):
        """
        Generic PUT request
        """

        return self._client.put(url, data=json.dumps(a_dict), content_type="application/json", follow_redirects=True)

    def generic_post(self, url, a_dict):
        """
        Generic POST request
        """

        return self._client.post(url, data=json.dumps(a_dict), content_type="application/json", follow_redirects=True)


@pytest.fixture
def auth(app, client):
    return AuthActions(app, client)


@pytest.fixture()
def app():
    """
    Create app with a database test
    """

    SQLALCHEMY_DATABASE_URI = "sqlite:///./atados-test.db"

    app = create_app()
    app.config.from_object("config.TestingConfig")
    app.config.update(SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI)
    app.config.update(PRESERVE_CONTEXT_ON_EXCEPTION=False)

    with app.app_context():
        # Will be called before every test
        db.create_all()

        # Create 2 Actions
        action_1 = Action(
            action_name="Action Name",
            reference_id="ReF01",
            organizing_institution="Institution",
            address="Address street 1",
            district="District IX",
            city="Budapest",
            description="Description about that Action",
        )

        action_2 = Action(
            action_name="Action Name 2",
            reference_id="ReF02",
            organizing_institution="Institution 2",
            address="Address street 2",
            district="District X",
            city="Budapest",
            description="Description about that Action",
        )

        # Create test admin user
        admin = User(
            username="admin",
            password="123456",
            is_admin=True,
            first_name="First Name",
            last_name="Last Name",
            email="admin@admin.com",
        )

        # Create test non-admin user
        user = User(
            username="non-admin",
            password="123456",
            is_admin=False,
            first_name="First Name",
            last_name="Last Name",
            email="non-admin@admin.com",
        )

        # Create 2 DID numbers
        volunteer_1 = Volunteer(
            first_name="First Name",
            last_name="Last Name",
            email="one@volunteer.com",
            district="District IX",
            city="Budapest",
        )

        volunteer_2 = Volunteer(
            first_name="First Name 2",
            last_name="Last Name 2",
            email="two@volunteer.com",
            district="District IX",
            city="Budapest",
        )

        # Save users to database
        db.session.add(admin)
        db.session.add(user)
        db.session.add(action_1)
        db.session.add(action_2)
        db.session.add(volunteer_1)
        db.session.add(volunteer_2)
        db.session.commit()

        yield app

        # Will be called after every test
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """
    Make requests to the application without running the server
    """

    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def json_of_response(response):
    """
    Decode json from response
    """

    return json.loads(response.data.decode("utf8"))


def get_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    a_string = "".join(choice(letters) for i in range(length))
    return a_string


def get_random_int(length: int) -> int:
    if length > 10:
        length = 10

    numbers = "0123456789"
    a_string = "".join(choice(numbers) for i in range(length))
    return int(a_string)


def populate_volunteers(n):
    for i in range(n):
        volunteer = Volunteer(
            first_name="First Name",
            last_name="Last Name",
            email=f"{get_random_string(10)}@email.com",
            district="District IX",
            city="Budapest",
        )

        try:
            db.session.add(volunteer)
            db.session.commit()
        except Exception as e:
            print(e)


def populate_actions(n):
    for i in range(n):
        action = Action(
            action_name="Action Name",
            reference_id=f"Ref{get_random_int(5)}",
            organizing_institution="Institution",
            address="Address street 1",
            district="District IX",
            city="Budapest",
            description="Description about that Action",
        )

        # save users to database
        try:
            db.session.add(action)
            db.session.commit()
        except Exception as e:
            print(e)
