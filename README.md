Atados Sample Project
======

A simple API built in Flask/SQLAlchemy.

[![Build Status](https://travis-ci.com/ericrommel/atados-sample.svg?branch=master)](https://travis-ci.com/ericrommel/atados-sample)
[![codecov](https://codecov.io/gh/ericrommel/atados-sample/branch/master/graph/badge.svg)](https://codecov.io/gh/ericrommel/atados-sample)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


Requirements
======

- [Python 3](http://python.org/)
- [Pip](https://pip.pypa.io/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLite](http://sqlite.org/) (or any other supported database)

These are optional but recommended.

- [Black](http://black.readthedocs.io/)
- [Codecov](http://codecov.io/)
- [Flake8](http://flake8.pycqa.org/)
- [Pipenv](http://pipenv.readthedocs.io)
- [Pre-commit](http://pre-commit.com/)


Installing
-------

The default Git version is the master branch. ::

    # clone the repository
    $ cd desired/path/
    $ git clone git@github.com:ericrommel/


The next step is install the project's Python dependencies. Just like _Git_ if you still don't have it go to the [official site](http://python.org/) and get it done. You'll also need [Pip](https://pip.pypa.io/), same rules applies here. Another interesting tool that is not required but strongly recommended is [Pipenv](http://pipenv.readthedocs.io), it helps to manage dependencies and virtual environments.

Installing with **Pip**:

    $ cd path/to/atados-project
    $ pip install --upgrade flask flask-sqlalchemy # and any other optional packages


Installing with **Pipenv**:

    $ pip install --upgrade pipenv
    $ cd path/to/atados-project
    $ pipenv sync -d


Finally, configure the application. This will require you to define a few variables and create the database.

Run
-------
Note: The pipenv virtual environment should be done.

Set the environment variables::

    $ export FLASK_APP=src
    $ export FLASK_ENV=development


Or on Windows cmd::

    > set FLASK_APP=src
    > set FLASK_ENV=development

Create the database::

    $ flask db init
    $ flask db migrate
    $ flask db upgrade

Run the application::

    $ flask run


Open http://127.0.0.1:5000 in a browser.


Tests
-------

From Postman::
- Import the collection file: postman/
- Import the environment file: postman/
- Click on Runner button
- Select the collection imported
- Select the environment imported
- Click on Run button

From Python code tests (unit tests)::

    $ pytest


Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser


About
======
This project is part of the Atados challenge.

Author
======
- [Eric Dantas](https://www.linkedin.com/in/ericrommel)
