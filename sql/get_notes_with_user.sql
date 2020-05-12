create function get_notes_with_user()
    returns TABLE(id integer, title character varying, description character varying, created_date timestamp without time zone, changed_date timestamp without time zone, owner character varying)
    language sql
as
$$
SELECT n.id, n.title, n.description, n.created_date, n.changed_date, "user".full_name
FROM note n JOIN "user" ON "user".id = n.owner_id ORDER BY n.id;
$$;