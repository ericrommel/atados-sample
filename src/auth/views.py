from flask import abort, jsonify, request
from flask_login import login_required, login_user, logout_user

from log import Log
from . import auth
from .. import db
from ..models import User, user_schema

LOGGER = Log("atados-challenge").get_logger(logger_name="app")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handle requests to the /register route. Here an user will be added to the database
    """

    email, username, first_name, last_name, password, is_admin = "", "", "", "", "", ""

    LOGGER.info("Set user variables from request")
    try:
        email = request.json["email"]
        username = request.json["username"]
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        password = request.json["password"]
        is_admin = request.json["is_admin"]
    except KeyError as e:
        LOGGER.error(f"KeyError: {e}")
        abort(400, f"There is no key with that value: {e}")

    if User.query.filter_by(email=email).first():
        LOGGER.error(f"{email} is already in use.")
        abort(403, description=f"{email} is already in use.")

    if User.query.filter_by(username=username).first():
        LOGGER.error(f"{username} is already in use.")
        abort(403, description=f"{username} is already in use.")

    user = User(
        email=email, username=username, first_name=first_name, last_name=last_name, password=password, is_admin=is_admin
    )

    LOGGER.info(f'Add "{user}" to database')
    db.session.add(user)
    db.session.commit()

    result = user_schema.dump(user)
    return jsonify(result), 201


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle requests to the /login route. Log an user
    """

    if request.method == "POST":
        email, password = "", ""
        LOGGER.info("Set email and password from request")
        try:
            email = request.json["email"]
            password = request.json["password"]
        except KeyError as e:
            LOGGER.error(f"KeyError: {e}")
            abort(400, f"There is no key with that value: {e}")

        # Check if the user exists in the database and if the password entered matches the password in the database
        LOGGER.info(f"Check DB for {email}")
        user = User.query.filter_by(email=email).first()
        result = ""
        if user is not None and user.check_password(password):
            LOGGER.info(f"{user.username} found. Logging in")
            result = user_schema.dump(user)
            # log volunteer in
            login_user(user)
        else:
            abort(401, "Invalid email or password.")

        return jsonify(result), 200
    else:
        abort(401, "It looks like you are not logged in yet.")


@auth.route("/logout")
@login_required
def logout():
    """
    Handle requests to the /logout route. Log an user out
    """

    logout_user()
    return jsonify({"message": "You have successfully been logged out."}), 200
