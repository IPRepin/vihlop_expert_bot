"""fix services sequence

Revision ID: fix_services_sequence
Revises: 5ae7d511dc66
Create Date: 2024-12-11 09:45:43.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fix_services_sequence'
down_revision: Union[str, None] = '5ae7d511dc66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Сбрасываем последовательность id в таблице services
    op.execute("""
    SELECT setval(pg_get_serial_sequence('services', 'id'), 
                 COALESCE((SELECT MAX(id) FROM services), 0) + 1, false)
    """)


def downgrade() -> None:
    pass
