"""autoincrement field id for tasks

Revision ID: 7238c2c5e8ab
Revises: ce64892b817e
Create Date: 2025-10-23 19:19:40.928050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7238c2c5e8ab'
down_revision: Union[str, Sequence[str], None] = 'ce64892b817e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
