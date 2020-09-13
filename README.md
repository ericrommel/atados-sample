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
    $ git clone git@github.com:ericrommel/


This project is using pipenv as a packaging tool. Learn more about pipenv here (<https://realpython.com/pipenv-guide/>)::

    $ pip install pipenv
    $ pipenv sync -d
    $ pipenv shell

It will install all requirements needed and create a virtual environment.


Run
---
Note: The pipenv virtual environment should be done.

Set the environment variables::

    $ export FLASK_CONFIG=development
    $ export FLASK_APP=run.py

Or on Windows cmd::

    > set FLASK_CONFIG=development
    > set FLASK_APP=run.py

Create the database::

    $ flask db init
    $ flask db migrate
    $ flask db upgrade

Run the application::

    $ flask run

Open http://127.0.0.1:5000 in a browser.


Tests
----

From Postman::
- Import the collection file: postman/
- Import the environment file: postman/

From Python code tests (unit tests)::

    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser