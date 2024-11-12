from pydantic import BaseModel
from datetime import datetime

class FormData(BaseModel):
    desde: str
    hasta: str | None = None
    reloj: str

class enrollUserZk(BaseModel):
    machine: int
    uid: int
    temp_id: int
    user_id: str

class Checkinout(BaseModel):
    badgenumber: str
    checktime: datetime
    sensorid: int
    verifycode: str
    checktype: str

class resp_reloj(BaseModel):
    results: list[Checkinout] = []

class formNovedad(BaseModel):
    fecha_i: str
    fecha_f: str
    legajo: int
    feriados: str | None

class formDivision(BaseModel):
    id: int
    legajo: int
    fecha: str
    novedad: str
    cantidad: int
    valor: int

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class User(BaseModel):
    id: int
    name: str
    password: str
    privileges: str
    access: bool | None = None

class Machine(BaseModel):
    sensorid: int
    serialnumber: str
    sensorname: str
    ip: str | None = None
    ddns: str | None = None

class zkUser(BaseModel):
    uid: int
    name: str | None = None
    user_id: str | None = None
    group_id: str | None = None
    privilege: int | None = None
    password: str | None = None

class zkCreateUser(BaseModel):
    uid: int | int = 0
    name: str
    privilege: int
    password: str | str = ''
    group_id: str | str = ''
    user_id: str
    card: int | int = 0
    machine: int

class zkSizes(BaseModel):
    users: int | None = None
    fingers: int | None = None
    records: int | None = None
    users_cap: int | None = None
    fingers_cap: int | None = None

class zkFinger(BaseModel):
    uid: int | None = None
    fid: int
    size: int | None = None
    valid: int | None = None
    template: bytes | None = None

class zkUserTemplate(BaseModel):
    user: zkUser
    templates: list[zkFinger]

class MachineInfo(BaseModel):
    firmware_version: str | None = None
    serialnumber: str | None = None
    platform: str | None = None
    device_name: str | None = None
    face_version: int | None = None
    fp_version: int | None = None
    extend_fmt: int | None = None
    user_extend_fmt: int | None = None
    face_fun_on: int | None = None
    compat_old_firmware: int | None = None
    network_params: dict | None = None
    mac: str | None = None
    pin_width: int | None = None
    usage_space: zkSizes | None = None
    users: list[zkUser] | None = None
    time: datetime | None = None

