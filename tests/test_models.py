from src.models import Action, User, Volunteer


def test_user_model(app):
    """
    Test number of records in User table
    """

    assert User.query.count() == 2


def test_volunteer_model(app):
    """
    Test number of records in Volunteer table
    """

    assert Volunteer.query.count() == 2


def test_action_model(app):
    """
    Test number of records in Action table
    """

    assert Action.query.count() == 2
