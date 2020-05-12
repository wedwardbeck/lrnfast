from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Response

from app.api.utils.security import get_current_active_user  # type: ignore
from app import crud
from app.crud import crud_notes
from app.models.user import User  # as User
from app.schemas.note import NoteDB, NoteSchema

router = APIRouter()
ERROR_NOT_FOUND = "Note not found"
ERROR_PERMISSIONS = "Not enough permissions"


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(
        payload: NoteSchema,
        current_user: User = Depends(get_current_active_user)
):
    """
    Create a new note.
    :param payload:
    :param current_user:
    :return:
    """
    return await crud_notes.post(payload, owner_id=current_user.id)


@router.get("/{id}/", response_model=NoteDB)
async def read_note(
        id: int = Path(..., gt=0),
        current_user: User = Depends(get_current_active_user)
):
    """
    Get a note by ID
    :param id:
    :param current_user:
    :return:
    """
    owner = await crud_notes.get_owner(id)
    if not owner:
        raise HTTPException(status_code=404, detail=ERROR_NOT_FOUND)
    if not crud.user.is_superuser(current_user) and (owner != current_user.id):
        raise HTTPException(status_code=400, detail=ERROR_PERMISSIONS)
    return  await crud_notes.get(id)


@router.get("/", response_model=List[NoteDB])
async def read_all_notes(
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve notes.
    :param skip:
    :param limit:
    :param current_user:
    :return:
    """
    if crud.user.is_superuser(current_user):
        notes = await crud_notes.get_all(skip=skip, limit=limit)
    else:
        notes = await crud_notes.get_all_by_owner(owner_id=current_user.id, skip=skip, limit=limit)
    return notes


@router.put("/{id}/", response_model=NoteDB)
async def update_note(
        payload: NoteSchema,
        id: int = Path(..., gt=0),
        current_user: User = Depends(get_current_active_user)
):
    """
    Update a note.
    :param payload:
    :param id:
    :param current_user:
    :return:
    """
    owner = await crud_notes.get_owner(id)
    if not owner:
        raise HTTPException(status_code=404, detail=ERROR_NOT_FOUND)
    if not crud.user.is_superuser(current_user) and (owner != current_user.id):
        raise HTTPException(status_code=400, detail=ERROR_PERMISSIONS)
    note = await crud_notes.put(id, payload, current_user)
    return note


@router.delete("/{id}/", response_class=Response, status_code=204)
async def delete_note(
        id: int = Path(..., gt=0),
        current_user: User = Depends(get_current_active_user)
):
    """
    Delete a note.
    :param id:
    :param current_user:
    :return:
    """
    owner = await crud_notes.get_owner(id)
    if not owner:
        raise HTTPException(status_code=404, detail=ERROR_NOT_FOUND)
    if not crud.user.is_superuser(current_user) and (owner != current_user.id):
        raise HTTPException(status_code=400, detail=ERROR_PERMISSIONS)
    return await crud_notes.delete(id)
