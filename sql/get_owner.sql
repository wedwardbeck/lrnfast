create or replace function get_owner(in note_id integer, out integer)
    language sql
as
$$
SELECT owner_id FROM note WHERE id = note_id;
$$;