from flask import abort, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from . import volunteer
from .. import db, LOGGER
from ..models import Volunteer, volunteer_schema, volunteers_schema


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    LOGGER.debug(f"Current User: {current_user}")
    if not current_user.is_admin:
        abort(403, "The current user is not an admin")


# Volunteer views
@volunteer.route("/volunteers")
def list_volunteers():
    """
    List all volunteers
    """

    LOGGER.info("Get the list of volunteers from the database")
    try:
        all_volunteers = volunteers_schema.dump(Volunteer.query.order_by(Volunteer.id.asc()))
    except OperationalError:
        LOGGER.info("There is no volunteers in the database")
        all_volunteers = None

    if all_volunteers is None:
        return jsonify({"warning": "There is no data to show"})

    LOGGER.info("Response the list of volunteers")
    return jsonify(all_volunteers)


@volunteer.route("/volunteers/<int:id>", methods=["GET"])
def volunteer_detail(id):
    """
    List details for a volunteer
    """

    volunteer = Volunteer.query.get_or_404(id)
    return volunteer_schema.jsonify(volunteer)


@volunteer.route("/volunteers/add", methods=["GET", "POST"])
def add_volunteer():
    """
    Add a volunteer to the database
    """

    first_name, last_name, email, district, city = "", "", "", "", ""

    LOGGER.info("Set volunteer variables from request")
    try:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        email = request.json["email"]
        district = request.json["district"]
        city = request.json["city"]
    except KeyError as e:
        abort(400, f"There is no key with that value: {e}")

    volunteer = Volunteer(
        first_name=first_name,
        last_name=last_name,
        email=email,
        district=district,
        city=city,
    )

    LOGGER.info(f"Add volunteer {volunteer.first_name} to the database")
    try:
        # Add volunteer to the database
        db.session.add(volunteer)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(403, f"Volunteer email {volunteer.email} already exists in the database.")
    except Exception as e:
        abort(500, e)

    return volunteer_schema.jsonify(volunteer), 201


@volunteer.route("/volunteers/edit/<int:id>", methods=["GET", "PUT"])
@login_required
def edit_volunteer(id):
    """
    Edit a volunteer
    """

    check_admin()

    volunteer = Volunteer.query.get_or_404(id)

    LOGGER.info("Set volunteer variables from request")
    try:
        volunteer.first_name = request.json["first_name"]
        volunteer.last_name = request.json["last_name"]
        volunteer.email = request.json["email"]
        volunteer.district = request.json["district"]
        volunteer.city = request.json["city"]
    except KeyError as e:
        abort(400, f"There is no key with that value: {e}")

    LOGGER.info(f"Edit volunteer {volunteer.first_name} in the database")
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(400, f"Volunteer email {volunteer.email} already exists.")
    except Exception as e:
        abort(500, e)

    return volunteer_schema.jsonify(volunteer), 200


@volunteer.route("/volunteers/delete/<int:id>", methods=["GET", "DELETE"])
@login_required
def delete_volunteer(id):
    """
    Delete a volunteer from the database
    """

    check_admin()

    volunteer = Volunteer.query.get_or_404(id)
    LOGGER.info(f"Delete {volunteer} from the database")
    try:
        db.session.delete(volunteer)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(400, f"Volunteer email {volunteer.email} already deleted.")
    except Exception as e:
        abort(500, e)

    return jsonify({"message": "The volunteer has successfully been deleted."}), 200
