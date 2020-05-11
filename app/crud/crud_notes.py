import datetime
from app.db.session import database
from app.models.note import Note
from app.schemas.note import NoteSchema
from app.models.user import User


async def post(payload: NoteSchema, owner_id: int):
    query = "INSERT INTO note(title, description, owner_id) VALUES (:title, :description, :owner_id) RETURNING id"
    values = {"title": payload.title, "description": payload.description, "owner_id": owner_id}
    id = await database.fetch_val(query=query, values=values)  # use databases.execute if databases version <=0.3.2
    note = await get(id)
    return note


async def get(id: int):
    query = "SELECT * FROM note WHERE id = :id"
    return await database.fetch_one(query=query, values={"id": id})


async def get_all(*, skip=0, limit=100):
    query = "SELECT n.id, n.title, n.description, n.created_date, n.owner_id, n.changed_date, " \
            "n.changed_by FROM note n ORDER BY n.id LIMIT :limit OFFSET :skip"
    return await database.fetch_all(query=query, values={"skip": skip, "limit": limit})


async def get_all_by_owner(*, owner_id: int, skip=0, limit=100):
    query = "SELECT n.id, n.title, n.description, n.created_date, n.owner_id, n.changed_date, " \
            "n.changed_by FROM note n " \
            "WHERE n.owner_id = :owner_id ORDER BY n.id LIMIT :limit OFFSET :skip"
    return await database.fetch_all(query=query, values={"skip": skip, "limit": limit, "owner_id": owner_id})


async def put(id: int, payload: NoteSchema, current_user: User):
    values = {
        "title": payload.title,
        "description": payload.description,
        "changed_by": current_user.id,
        "id": id,
        "now": datetime.datetime.now()
    }
    query = "UPDATE note SET title = :title, description = :description, changed_by = :changed_by, " \
            "changed_date = :now WHERE id = :id RETURNING id"
    updated: int = await database.execute(query=query, values=values)
    note = await get(updated)
    return note


async def delete(id: int):
    query = "DELETE FROM note where id = :id"
    deleted = await database.execute(query=query, values={"id": id})
    return deleted


async def get_owner(id: int):
    query = "SELECT * FROM note WHERE id = :id"
    return await database.fetch_val(query=query, values={"id": id}, column=4)

