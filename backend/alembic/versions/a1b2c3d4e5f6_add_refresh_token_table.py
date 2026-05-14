"""add_refresh_token_table

Revision ID: a1b2c3d4e5f6
Revises: d21e73513818
Create Date: 2026-05-13 21:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'd21e73513818'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('refreshtokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('token_hash', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('family_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_refreshtokens_usuario_id'), 'refreshtokens', ['usuario_id'], unique=False)
    op.create_index(op.f('ix_refreshtokens_token_hash'), 'refreshtokens', ['token_hash'], unique=False)
    op.create_index(op.f('ix_refreshtokens_family_id'), 'refreshtokens', ['family_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_refreshtokens_usuario_id'), table_name='refreshtokens')
    op.drop_index(op.f('ix_refreshtokens_token_hash'), table_name='refreshtokens')
    op.drop_index(op.f('ix_refreshtokens_family_id'), table_name='refreshtokens')
    op.drop_table('refreshtokens')
