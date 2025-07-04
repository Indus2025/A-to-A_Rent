"""Initial Migration for A to A form complete variables

Revision ID: 1b1fa51f2af5
Revises: 
Create Date: 2025-06-30 14:37:52.567111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b1fa51f2af5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agent_agreements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dated', sa.Date(), nullable=True),
    sa.Column('agent_a_establishment', sa.String(length=255), nullable=True),
    sa.Column('agent_a_address', sa.String(length=255), nullable=True),
    sa.Column('agent_a_phone', sa.String(length=50), nullable=True),
    sa.Column('agent_a_fax', sa.String(length=50), nullable=True),
    sa.Column('agent_a_email', sa.String(length=100), nullable=True),
    sa.Column('agent_a_orn', sa.String(length=50), nullable=True),
    sa.Column('agent_a_license', sa.String(length=50), nullable=True),
    sa.Column('agent_a_po_box', sa.String(length=50), nullable=True),
    sa.Column('agent_a_emirates', sa.String(length=50), nullable=True),
    sa.Column('agent_a_name', sa.String(length=100), nullable=True),
    sa.Column('agent_a_brn', sa.String(length=50), nullable=True),
    sa.Column('agent_a_date_issued', sa.Date(), nullable=True),
    sa.Column('agent_a_mobile', sa.String(length=20), nullable=True),
    sa.Column('agent_a_email_personal', sa.String(length=100), nullable=True),
    sa.Column('agent_b_establishment', sa.String(length=255), nullable=True),
    sa.Column('agent_b_address', sa.String(length=255), nullable=True),
    sa.Column('agent_b_phone', sa.String(length=50), nullable=True),
    sa.Column('agent_b_fax', sa.String(length=50), nullable=True),
    sa.Column('agent_b_email', sa.String(length=100), nullable=True),
    sa.Column('agent_b_orn', sa.String(length=50), nullable=True),
    sa.Column('agent_b_license', sa.String(length=50), nullable=True),
    sa.Column('agent_b_po_box', sa.String(length=50), nullable=True),
    sa.Column('agent_b_emirates', sa.String(length=50), nullable=True),
    sa.Column('agent_b_name', sa.String(length=100), nullable=True),
    sa.Column('agent_b_brn', sa.String(length=50), nullable=True),
    sa.Column('agent_b_date_issued', sa.Date(), nullable=True),
    sa.Column('agent_b_mobile', sa.String(length=20), nullable=True),
    sa.Column('agent_b_email_personal', sa.String(length=100), nullable=True),
    sa.Column('property_address', sa.String(length=255), nullable=True),
    sa.Column('master_developer', sa.String(length=100), nullable=True),
    sa.Column('master_project', sa.String(length=100), nullable=True),
    sa.Column('building_name', sa.String(length=100), nullable=True),
    sa.Column('listed_price', sa.String(length=50), nullable=True),
    sa.Column('property_description', sa.Text(), nullable=True),
    sa.Column('landlord_agent_percent', sa.String(length=10), nullable=True),
    sa.Column('tenant_agent_percent', sa.String(length=10), nullable=True),
    sa.Column('tenant_name', sa.String(length=100), nullable=True),
    sa.Column('tenant_passport', sa.String(length=50), nullable=True),
    sa.Column('tenant_budget', sa.String(length=50), nullable=True),
    sa.Column('tenant_contacted_agent', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agent_agreements_id'), 'agent_agreements', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_agent_agreements_id'), table_name='agent_agreements')
    op.drop_table('agent_agreements')
    # ### end Alembic commands ###
