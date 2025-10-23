"""autoincrement field id for categories

Revision ID: ce64892b817e
Revises: 7308ce0ab937
Create Date: 2025-10-23 19:11:15.279059

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce64892b817e'
down_revision: Union[str, Sequence[str], None] = '7308ce0ab937'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
