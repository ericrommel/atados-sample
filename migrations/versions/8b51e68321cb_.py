"""empty message

Revision ID: 8b51e68321cb
Revises:
Create Date: 2020-09-13 16:01:58.277830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8b51e68321cb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "actions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("reference_id", sa.String(length=10), nullable=True),
        sa.Column("action_name", sa.String(length=60), nullable=True),
        sa.Column("organizing_institution", sa.String(length=60), nullable=True),
        sa.Column("address", sa.String(length=60), nullable=True),
        sa.Column("district", sa.String(length=60), nullable=True),
        sa.Column("city", sa.String(length=60), nullable=True),
        sa.Column("description", sa.String(length=350), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_actions_action_name"), "actions", ["action_name"], unique=False)
    op.create_index(op.f("ix_actions_address"), "actions", ["address"], unique=False)
    op.create_index(op.f("ix_actions_city"), "actions", ["city"], unique=False)
    op.create_index(op.f("ix_actions_description"), "actions", ["description"], unique=False)
    op.create_index(op.f("ix_actions_district"), "actions", ["district"], unique=False)
    op.create_index(op.f("ix_actions_organizing_institution"), "actions", ["organizing_institution"], unique=False)
    op.create_index(op.f("ix_actions_reference_id"), "actions", ["reference_id"], unique=True)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=60), nullable=True),
        sa.Column("last_name", sa.String(length=60), nullable=True),
        sa.Column("email", sa.String(length=60), nullable=True),
        sa.Column("username", sa.String(length=60), nullable=True),
        sa.Column("password_hash", sa.String(length=100), nullable=True),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_first_name"), "users", ["first_name"], unique=False)
    op.create_index(op.f("ix_users_last_name"), "users", ["last_name"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_table(
        "volunteers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=60), nullable=True),
        sa.Column("first_name", sa.String(length=60), nullable=True),
        sa.Column("last_name", sa.String(length=60), nullable=True),
        sa.Column("district", sa.String(length=60), nullable=True),
        sa.Column("city", sa.String(length=60), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_volunteers_city"), "volunteers", ["city"], unique=False)
    op.create_index(op.f("ix_volunteers_district"), "volunteers", ["district"], unique=False)
    op.create_index(op.f("ix_volunteers_email"), "volunteers", ["email"], unique=True)
    op.create_index(op.f("ix_volunteers_first_name"), "volunteers", ["first_name"], unique=False)
    op.create_index(op.f("ix_volunteers_last_name"), "volunteers", ["last_name"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_volunteers_last_name"), table_name="volunteers")
    op.drop_index(op.f("ix_volunteers_first_name"), table_name="volunteers")
    op.drop_index(op.f("ix_volunteers_email"), table_name="volunteers")
    op.drop_index(op.f("ix_volunteers_district"), table_name="volunteers")
    op.drop_index(op.f("ix_volunteers_city"), table_name="volunteers")
    op.drop_table("volunteers")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_last_name"), table_name="users")
    op.drop_index(op.f("ix_users_first_name"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_actions_reference_id"), table_name="actions")
    op.drop_index(op.f("ix_actions_organizing_institution"), table_name="actions")
    op.drop_index(op.f("ix_actions_district"), table_name="actions")
    op.drop_index(op.f("ix_actions_description"), table_name="actions")
    op.drop_index(op.f("ix_actions_city"), table_name="actions")
    op.drop_index(op.f("ix_actions_address"), table_name="actions")
    op.drop_index(op.f("ix_actions_action_name"), table_name="actions")
    op.drop_table("actions")
    # ### end Alembic commands ###
