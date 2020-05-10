from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path

from app.api.utils.security import get_current_active_user  # type: ignore
from app.crud import crud_notes
from app.models.user import User as DBUser
from app.schemas.note import NoteDB, NoteSchema

router = APIRouter()
ERROR_NOT_FOUND = "Note not found"


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(
    payload: NoteSchema, current_user: DBUser = Depends(get_current_active_user)
):
    note = await crud_notes.post(payload, owner_id=current_user.id)

    # response_object = {
    #     "id": note_id.id,
    #     "title": payload.title,
    #     "description": payload.description,
    #     # "owner_id":
    # }
    return note
    # return response_object


@router.get("/{id}/", response_model=NoteDB)
async def read_note(id: int = Path(..., gt=0),):
    note = await crud_notes.get(id)
    if not note:
        raise HTTPException(status_code=404, detail=ERROR_NOT_FOUND)
    return note


@router.get("/", response_model=List[NoteDB])
async def read_all_notes():
    return await crud_notes.get_all()


@router.put("/{id}/", response_model=NoteDB)
async def update_note(
    payload: NoteSchema, id: int = Path(..., gt=0),
):
    note = await crud_notes.get(id)
    if not note:
        raise HTTPException(status_code=404, detail=ERROR_NOT_FOUND)

    note_id = await crud_notes.put(id, payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(id: int = Path(..., gt=0)):
    note = await crud_notes.get(id)
    if not note:
        raise HTTPException(status_code=404, detail=ERROR_NOT_FOUND)

    await crud_notes.delete(id)

    return note
