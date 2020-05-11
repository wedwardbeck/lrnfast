import datetime
from app.db.session import database
from app.models.note import Note
from app.schemas.note import NoteSchema
from app.models.user import User


async def post(payload: NoteSchema, owner_id: int):
    query = "INSERT INTO note(title, description, owner_id) VALUES (:title, :description, :owner_id) RETURNING id"
    values = {"title": payload.title, "description": payload.description, "owner_id": owner_id}
    id = await database.execute(query=query, values=values)
    q2 = "SELECT * FROM note WHERE id = :id"
    note = await database.fetch_one(query=q2, values={"id": id})
    return note
    # TODO: Refactor to use dependency injection or call get().


async def get(id: int):
    query = "SELECT * FROM note WHERE id = :id"
    return await database.fetch_one(query=query, values={"id": id})


async def get_all():
    query = "SELECT n.id, n.title, n.description, n.created_date, n.owner_id, n.changed_on, " \
            "n.changed_by FROM note n"
    print(query)
    return await database.fetch_all(query=query)


async def put(id: int, payload: NoteSchema, uid: User):
    values = {
        "title": payload.title,
        "description": payload.description,
        "changed_by": uid.id,
        "id": id,
        "now": datetime.datetime.now()
    }
    # print(values)
    query = "UPDATE note SET title = :title, description = :description, changed_by = :changed_by, " \
            "changed_on = :now WHERE id = :id RETURNING id"
    # print(query)
    await database.execute(query=query, values=values)
    q2 = "SELECT * FROM note WHERE id = :id"
    note = await database.fetch_one(query=q2, values={"id": id})
    # print(note)
    return note


async def delete(id: int):
    query = "DELETE FROM note where id = :id"
    return await database.execute(query=query, values={"id": id})
