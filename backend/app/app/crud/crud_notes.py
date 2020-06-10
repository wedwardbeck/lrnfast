import datetime
from app.db.session import database
from app.models.note import Note
from app.schemas.note import NoteSchema
from app.models.user import User


async def post(payload: NoteSchema, owner_id: int):
    query = "CALL insert_note(:title, :description, :owner_id, 0)"  # noinspection
    values = {"title": payload.title, "description": payload.description, "owner_id": owner_id}
    id = await database.fetch_val(query=query, values=values)  # use databases.execute if databases version <=0.3.2
    note = await get(id)
    return note


async def get(id: int):
    query = "SELECT * FROM get_by_id(:id)"
    return await database.fetch_one(query=query, values={"id": id})


async def get_all(*, skip=0, limit=100):
    query = "select * from get_notes_with_user() LIMIT :limit OFFSET :skip"
    return await database.fetch_all(query=query, values={"skip": skip, "limit": limit})


async def get_all_by_owner(*, owner_id: int, skip=0, limit=100):
    query = "select * from get_notes_by_owner(:owner_id) LIMIT :limit OFFSET :skip;"
    return await database.fetch_all(query=query, values={"skip": skip, "limit": limit, "owner_id": owner_id})


async def put(id: int, payload: NoteSchema, current_user: User):
    values = {
        "title": payload.title,
        "description": payload.description,
        "changed_by": current_user.id,
        "id": id
    }
    query = "CALL update_note(:title, :description, :changed_by, :id, 0)"
    updated: int = await database.execute(query=query, values=values)
    note = await get(updated)
    return note


async def delete(id: int):
    query = "CALL delete_note(:id)"
    return await database.execute(query=query, values={"id": id})


async def get_owner(id: int):
    query = "SELECT get_owner(:id)"
    return await database.fetch_val(query=query, values={"id": id})
