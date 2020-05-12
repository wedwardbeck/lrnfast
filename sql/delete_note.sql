CREATE PROCEDURE delete_note(in _id integer)
LANGUAGE SQL
AS $$
DELETE FROM note where id = _id
    $$;