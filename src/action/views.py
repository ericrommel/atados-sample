from flask import abort, jsonify, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from log import Log
from . import action
from .. import db
from ..models import Action, action_schema, actions_schema

LOGGER = Log("atados-challenge").get_logger(logger_name="app")


def check_admin():
    """
    Prevent non-admins from accessing the page
    """

    LOGGER.info(f"Current user: {current_user}")
    if not current_user.is_admin:
        abort(403, "The current volunteer is not an admin")


# Action views
@action.route("/actions")
def list_actions():
    """
    List all actions
    """

    LOGGER.info("Get the list of actions from the database")
    try:
        all_actions = actions_schema.dump(Action.query.order_by(Action.id.asc()))
    except OperationalError:
        LOGGER.info("There is no actions in the database")
        all_actions = None

    if all_actions is None:
        return jsonify({"warning": "There is no data to show"})

    LOGGER.info("Response the list of actions")
    return jsonify(all_actions)


@action.route("/actions/<int:id>", methods=["GET"])
def action_detail(id):
    """
    List details for a action
    """

    action = Action.query.get_or_404(id)
    return action_schema.jsonify(action)


@action.route("/actions/add", methods=["GET", "POST"])
@login_required
def add_action():
    """
    Add an action to the database
    """

    check_admin()

    reference_id, action_name, organizing_institution, address, district, city, description = "", "", "", "", "", "", ""

    LOGGER.info("Set variables from request")
    try:
        action_name = request.json["action_name"]
        reference_id = request.json["reference_id"]
        organizing_institution = request.json["organizing_institution"]
        address = request.json["address"]
        district = request.json["district"]
        city = request.json["city"]
        description = request.json["description"]
    except KeyError as e:
        abort(400, f"There is no key with that value: {e}")

    action = Action(
        reference_id=reference_id,
        action_name=action_name,
        organizing_institution=organizing_institution,
        address=address,
        district=district,
        city=city,
        description=description,
    )

    LOGGER.info(f"Add action {action.action_name} to the database")
    try:
        # Add action to the database
        db.session.add(action)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(403, f"Action reference id {action.reference_id} already exists in the database.")
    except Exception as e:
        abort(500, e)

    return action_schema.jsonify(action), 201


@action.route("/actions/edit/<int:id>", methods=["GET", "PUT"])
@login_required
def edit_action(id):
    """
    Edit an action
    """

    check_admin()

    action = Action.query.get_or_404(id)
    LOGGER.info("Set variables from request")
    try:
        action.reference_id = request.json["reference_id"]
        action.action_name = request.json["action_name"]
        action.organizing_institution = request.json["organizing_institution"]
        action.district = request.json["district"]
        action.city = request.json["city"]
        action.description = request.json["description"]

    except KeyError as e:
        abort(400, f"There is no key with that value: {e}")

    LOGGER.info(f"Edit action {action.action_name} in the database")
    try:
        # Edit action in the database
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(400, f"Actio reference id {action.reference_id} already exists.")
    except Exception as e:
        abort(500, e)

    return action_schema.jsonify(action), 200


@action.route("/actions/delete/<int:id>", methods=["GET", "DELETE"])
@login_required
def delete_action(id):
    """
    Delete an action from the database
    """

    check_admin()

    action = Action.query.get_or_404(id)

    LOGGER.info(f"Delete {action} from the database")
    try:
        db.session.delete(action)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(400, f"Action reference id {action.reference_id} already deleted.")
    except Exception as e:
        abort(500, e)

    return jsonify({"message": "The action has successfully been deleted."}), 200
