CREATE PROCEDURE update_note(in n_title varchar(50), in n_desc varchar(50), in n_changed_by integer,
in _id integer, inout id integer)
LANGUAGE SQL
AS $$
UPDATE note SET title = n_title, description = n_desc, changed_by = n_changed_by, changed_date = now()
WHERE id = _id RETURNING id
    $$;