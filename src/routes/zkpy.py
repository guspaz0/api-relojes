
from fastapi import APIRouter, Query
from src.services.zkpy import getFichadas, getInfo, setTime, copyTemplates

router = APIRouter()

@router.get('/info')
def getInfoReloj(
    _machine: str = Query(...,alias="machine"),
    _fields: str = Query(...,alias="fields")
    ):
    return getInfo(_machine, _fields)

@router.get('')
def fichadas(
    _machine: str = Query(...,alias="machine"),
    _desde: str = Query(...,alias="desde"),
    _hasta: str = Query(...,alias="hasta")
    ):
    return getFichadas(_machine, _desde, _hasta)

@router.put('/time')
def updateTime(
    _machine: str = Query(...,alias="machine"),
    _origen: str = Query(...,alias="origen")):
    return setTime(_machine, _origen)

@router.put('/template')
def putTemplates(
    _from: str = Query(...,alias="from"),
    _to: str = Query(...,alias="to"),
    _uids: str = Query(...,alias="uids")
    ):
    return copyTemplates(_from, _to, _uids)

