
from fastapi import APIRouter, Query
from src.schemas import zkCreateUser, enrollUserZk
from src.services.zkUser import ( createUser, fingerUser, deleteUser, enrollUser )

router = APIRouter()

@router.delete('')
def fichadas(
    _machine: str = Query(...,alias="machine"),
    _uid: str = Query(...,alias="uid"),
    _legajo: str = Query(...,alias="legajo")
    ):
    return deleteUser(_machine, _uid, _legajo)

@router.post('')
def postUser(body: zkCreateUser):
    return createUser(body)

@router.get('')
def getFinger(
    _machine: str = Query(...,alias="machine"),
    _uid: str = Query(...,alias="uid")):
    return fingerUser(_machine, _uid)

@router.put('/template')
def putTemplates(body: enrollUserZk):
    return enrollUser(body)
