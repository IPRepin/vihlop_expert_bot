"""add user

Revision ID: 40a6aa3b7d37
Revises: f50b97a3f24a
Create Date: 2024-12-01 11:22:53.160263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40a6aa3b7d37'
down_revision: Union[str, None] = 'f50b97a3f24a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
