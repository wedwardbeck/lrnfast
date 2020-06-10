CREATE PROCEDURE insert_note(in n_title varchar(50), in n_desc varchar(50), in n_owner integer, inout id integer)
LANGUAGE SQL
AS $$
INSERT INTO note(title, description, owner_id) VALUES (n_title, n_desc, n_owner) RETURNING id
    $$;