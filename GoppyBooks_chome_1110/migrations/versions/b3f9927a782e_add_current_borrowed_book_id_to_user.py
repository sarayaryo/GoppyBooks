"""Add current_borrowed_book_id to User

Revision ID: 4d44ef50dab9
Revises: 
Create Date: 2024-07-29 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4d44ef50dab9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_borrowed_book_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_current_borrowed_book_id', 'book', ['current_borrowed_book_id'], ['id'])

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('fk_current_borrowed_book_id', type_='foreignkey')
        batch_op.drop_column('current_borrowed_book_id')