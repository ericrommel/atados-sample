from src import create_app


def test_config():
    assert not create_app().testing
    assert create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:telecom-test.db",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    ).testing
