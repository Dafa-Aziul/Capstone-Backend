"""add superadmin role

Revision ID: ae83f886c6a7
Revises: 08da12236dc7
Create Date: 2026-06-29 15:46:03.951370

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "ae83f886c6a7"
down_revision = "08da12236dc7"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TABLE users
        MODIFY COLUMN role ENUM('superadmin', 'admin', 'user') NOT NULL DEFAULT 'user'
        """
    )


def downgrade():
    op.execute(
        """
        UPDATE users
        SET role = 'admin'
        WHERE role = 'superadmin'
        """
    )
    op.execute(
        """
        ALTER TABLE users
        MODIFY COLUMN role ENUM('admin', 'user') NOT NULL DEFAULT 'user'
        """
    )
