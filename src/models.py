from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from src import db, login_manager, ma
from log import Log

LOGGER = Log("atados-challenge").get_logger(logger_name="app")


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)

    def check_password(self, password):
        """
        Check if hashed password matches with actual password
        """

        LOGGER.info("Check if the password is correct")
        return check_password_hash(self.password_hash, password)

    def __init__(self, first_name, last_name, email, username, password, is_admin=False):
        LOGGER.info("Create an user instance")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return f"<User: {self.username}>"


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        fields = ("id", "first_name", "last_name", "email", "username", "is_admin")
        model = User
        load_instance = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    LOGGER.info("Set up an user loader")
    return User.query.get(int(user_id))


class Volunteer(db.Model):
    """
    Create a volunteer table
    """

    __tablename__ = "volunteers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    district = db.Column(db.String(60), index=True)
    city = db.Column(db.String(60), index=True)

    def __init__(self, first_name, last_name, email, district, city):
        LOGGER.info("Create a volunteer instance")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.district = district
        self.city = city

    def __repr__(self):
        return f"<Volunteer: {self.first_name} {self.last_name}>"


class VolunteerSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "first_name", "last_name", "email", "district", "city")
        model = Volunteer
        load_instance = True


volunteer_schema = VolunteerSchema()
volunteers_schema = VolunteerSchema(many=True)


class Action(db.Model):
    """
    Create an action table
    """

    __tablename__ = "actions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reference_id = db.Column(db.String(10), index=True, unique=True)
    action_name = db.Column(db.String(60), index=True)
    organizing_institution = db.Column(db.String(60), index=True)
    address = db.Column(db.String(60), index=True)
    district = db.Column(db.String(60), index=True)
    city = db.Column(db.String(60), index=True)
    description = db.Column(db.String(350), index=True)

    def __init__(self, reference_id, action_name, organizing_institution, address, district, city, description):
        LOGGER.info("Create an action instance")
        self.reference_id = reference_id
        self.action_name = action_name
        self.organizing_institution = organizing_institution
        self.address = address
        self.district = district
        self.city = city
        self.description = description

    def __repr__(self):
        return f"<Action: {self.action_name} from {self.organizing_institution}>"


class ActionSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = (
            "id",
            "reference_id",
            "action_name",
            "organizing_institution",
            "address",
            "district",
            "city",
            "description",
        )
        model = Action
        load_instance = True


action_schema = ActionSchema()
actions_schema = ActionSchema(many=True)
