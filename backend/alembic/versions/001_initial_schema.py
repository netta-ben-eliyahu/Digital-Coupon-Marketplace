"""initial schema

Revision ID: 001
Revises: 
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('products',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('type', sa.Enum('COUPON', name='producttype'), nullable=False),
        sa.Column('image_url', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('coupons',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('cost_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('margin_percentage', sa.Numeric(5, 2), nullable=False),
        sa.Column('minimum_sell_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('is_sold', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('value_type', sa.Enum('STRING', 'IMAGE', name='couponvaluetype'), nullable=False),
        sa.Column('value', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['products.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('resellers',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )


def downgrade() -> None:
    op.drop_table('coupons')
    op.drop_table('products')
    op.drop_table('resellers')
    op.execute('DROP TYPE IF EXISTS producttype')
    op.execute('DROP TYPE IF EXISTS couponvaluetype')