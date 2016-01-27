"""empty message

Revision ID: 1075e56c5f5b
Revises: None
Create Date: 2016-01-27 17:07:09.518522

"""

# revision identifiers, used by Alembic.
revision = '1075e56c5f5b'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    from app import app
    op.create_table('boards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('locale', sa.String(length=2), nullable=True),
    sa.Column('num_marking', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('qualifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('locale', sa.String(length=2), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('num_students', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('is_compulsory', sa.Boolean(), nullable=True),
    sa.Column('is_higher', sa.Boolean(), nullable=True),
    sa.Column('perc_exam', sa.Float(), nullable=True),
    sa.Column('total_marks', sa.Integer(), nullable=True),
    sa.Column('num_modules', sa.Integer(), nullable=True),
    sa.Column('num_students', sa.Integer(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('qualification_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['qualification_id'], ['qualifications.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_live', sa.Boolean(), nullable=True),
    sa.Column('password_hash', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_table('exams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.Column('marks', sa.Integer(), nullable=True),
    sa.Column('total_num_q', sa.Integer(), nullable=True),
    sa.Column('required_num_q', sa.Integer(), nullable=True),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('num_retakes', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic', sa.String(), nullable=False),
    sa.Column('exam_id', sa.Integer(), nullable=True),
    sa.Column('marks', sa.Integer(), nullable=True),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=True),
    sa.Column('marks', sa.Integer(), nullable=True),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('meta', app.models.TextPickleType(), nullable=True),
    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('questions')
    op.drop_table('sections')
    op.drop_table('exams')
    op.drop_table('users')
    op.drop_table('subjects')
    op.drop_table('roles')
    op.drop_table('qualifications')
    op.drop_table('boards')
    ### end Alembic commands ###
