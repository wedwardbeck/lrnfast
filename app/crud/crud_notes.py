from app.db.session import database
from app.models.note import Note
from app.schemas.note import NoteSchema


async def post(payload: NoteSchema, owner_id: int):
    query = "INSERT INTO note(title, description, owner_id) VALUES (:title, :description, :owner_id)"
    values = {"title": payload.title, "description": payload.description, "owner_id": owner_id}
    print(values)
    return await database.execute(query=query, values=values)
    # TODO: Get return value here.  Getting a NULL returned


async def get(id: int):
    query = "SELECT * FROM note WHERE id = :id"
    return await database.fetch_one(query=query, values={"id": id})


async def get_all():
    query = "SELECT * FROM note"
    return await database.fetch_all(query=query)


async def put(id: int, payload: NoteSchema):
    values = {"title": payload.title, "description": payload.description}
    query = "UPDATE note SET title = :title, description = :description WHERE id = :id RETURNING *"
    return await database.execute(query=query, values=values)


async def delete(id: int):
    query = "DELETE FROM note where id = :id"
    return await database.execute(query=query)
