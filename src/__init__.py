import os

from flask import Flask

from log import Log

LOGGER = Log("atados-challenge").get_logger(logger_name="app")


def create_app(test_config=None):
    LOGGER.info("Initialize Flask app")
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="TEMPORARY",
    )

    if test_config is None:
        LOGGER.info("test-config is None. Get configs from config.py")
        app.config.from_pyfile("config.py", silent=True)
    else:
        LOGGER.info(f"test-config is not None ({test_config}). Add configs from mapping")
        app.config.from_mapping(test_config)

    try:
        LOGGER.info("Create 'instance' folder")
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def hello():
        return "Hello, World!"

    return app
