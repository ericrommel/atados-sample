import os


class Config(object):
    """
    Common configurations
    """

    # Flask settings
    DEBUG = True
    TESTING = False
    DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    DATABASE_URI = os.getenv("DATABASE_URI")


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True


app_config = {"development": DevelopmentConfig, "production": ProductionConfig, "testing": TestingConfig}
