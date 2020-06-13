"""

Revision ID: e435422117c3
Revises: 3baeebd703b9
Create Date: 2020-05-09 19:54:58.438807+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e435422117c3'
down_revision = '3baeebd703b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('note',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=50), nullable=True),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('changed_date', sa.DateTime(), nullable=True),
    sa.Column('changed_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['changed_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_note_description'), 'note', ['description'], unique=False)
    op.create_index(op.f('ix_note_id'), 'note', ['id'], unique=False)
    op.create_index(op.f('ix_note_title'), 'note', ['title'], unique=False)
    op.execute(
        """
        CREATE PROCEDURE insert_note(in n_title varchar(50), in n_desc varchar(50), in n_owner integer, inout id integer)
        LANGUAGE SQL
        AS $$
        INSERT INTO note(title, description, owner_id) VALUES (n_title, n_desc, n_owner) RETURNING id
        $$;
        """
    )
    op.execute(
        """
        CREATE PROCEDURE delete_note(in _id integer)
        LANGUAGE SQL
        AS $$
        DELETE FROM note where id = _id
        $$;
        """
    )
    op.execute(
        """
        create or replace function get_by_id(note_id integer)
        returns TABLE(id integer, title character varying, description character varying, created_date timestamp without time zone, changed_date timestamp without time zone, owner character varying)
        language sql
        AS
        $$
        SELECT n.id, n.title, n.description, n.created_date, n.changed_date, "user".full_name
        FROM note n JOIN "user" ON "user".id = n.owner_id WHERE n.id = note_id ORDER BY n.id;
        $$;
        """
    )
    op.execute(
        """
        create or replace function get_notes_by_owner(ownerid int)
        returns TABLE (
            id int,
            title varchar(50),
            description varchar(50),
            created_date timestamp,
            changed_date timestamp,
            owner varchar
                    )
                        language sql as $$
            SELECT n.id, n.title, n.description, n.created_date, n.changed_date, "user".full_name
        FROM note n JOIN "user" ON "user".id = n.owner_id where owner_id = ownerid ORDER BY n.id;
        $$;
        """
    )
    op.execute(
        """create function get_notes_with_user()
        returns TABLE(id integer, title character varying, description character varying, created_date timestamp without time zone, changed_date timestamp without time zone, owner character varying)
        language sql
        as
        $$
        SELECT n.id, n.title, n.description, n.created_date, n.changed_date, "user".full_name
        FROM note n JOIN "user" ON "user".id = n.owner_id ORDER BY n.id;
        $$;
        """
    )
    op.execute(
        """create or replace function get_owner(in note_id integer, out integer)
        language sql
        as
        $$
        SELECT owner_id FROM note WHERE id = note_id;
        $$;
        """
    )
    op.execute(
        """
        CREATE PROCEDURE update_note(in n_title varchar(50), in n_desc varchar(50), in n_changed_by integer,
        in _id integer, inout id integer)
        LANGUAGE SQL
        AS $$
        UPDATE note SET title = n_title, description = n_desc, changed_by = n_changed_by, changed_date = now()
        WHERE id = _id RETURNING id
        $$;
        """
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_note_title'), table_name='note')
    op.drop_index(op.f('ix_note_id'), table_name='note')
    op.drop_index(op.f('ix_note_description'), table_name='note')
    op.drop_table('note')
    # ### end Alembic commands ###
