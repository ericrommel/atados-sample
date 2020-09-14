def test_development_config(app):
    app.config.from_object("config.DevelopmentConfig")
    assert app.config["DEBUG"]
    assert not app.config["TESTING"]


def test_production_config(app):
    app.config.from_object("config.ProductionConfig")
    assert not app.config["DEBUG"]
    assert not app.config["TESTING"]


def test_testing_config(app):
    app.config.from_object("config.TestingConfig")
    assert app.config["DEBUG"]
    assert app.config["TESTING"]
    assert not app.config["PRESERVE_CONTEXT_ON_EXCEPTION"]
