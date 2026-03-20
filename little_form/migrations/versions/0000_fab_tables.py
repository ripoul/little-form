"""0000_fab_tables

Revision ID: 0000_fab_tables
Revises:
Create Date: 2026-03-20

Creates Flask-AppBuilder security tables (ab_*).
Required when FAB_CREATE_DB is False for proper integration with Flask-Migrate.
"""

from alembic import op
from flask_appbuilder.models.sqla import Base


# revision identifiers, used by Alembic.
revision = "a0b0c0d0e0f0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    fab_tables = [t for t in Base.metadata.sorted_tables if t.name.startswith("ab_")]
    for table in fab_tables:
        table.create(bind, checkfirst=True)


def downgrade():
    bind = op.get_bind()
    fab_tables = [t for t in Base.metadata.sorted_tables if t.name.startswith("ab_")]
    # Drop in reverse order (association tables first, then base tables)
    for table in reversed(fab_tables):
        table.drop(bind, checkfirst=True)
