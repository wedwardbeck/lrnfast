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