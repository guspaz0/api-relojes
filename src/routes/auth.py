from datetime import datetime, timedelta, timezone
from typing import Annotated
from dotenv import dotenv_values
import psycopg2 
import hashlib
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.schemas import Token, User, Login
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")

configEnv = dotenv_values(".env")

SECRET_KEY = configEnv["JWT_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SALT=configEnv["SALT"]

config = {
    'host':configEnv["DB_HOST"],
    'database':configEnv["DB_NAME"],
    'user':configEnv["DB_USER"],
    'password':configEnv["DB_PASS"]
}

conn = psycopg2.connect(**config) 

cur = conn.cursor()

router = APIRouter()

@router.post("/access-token")
async def handleLogin(body: Login):
    return login_access_token(body)

def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    cur.execute('SELECT * FROM "Users" '+ f"where name = '{form_data.username}';")
    user = cur.fetchone()
    if (user):
        userData = User(id=user[0], name=user[1], password=user[2], privileges=user[3])
        dk = hashlib.pbkdf2_hmac("sha256", form_data.password.encode('utf-8'), SALT.encode('utf-8'), 36000, 64)
        hash_result = dk.hex()
        if hash_result == userData.password:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token({'id': userData.id}, access_token_expires)
            return Token(access_token=access_token, token_type="bearer" )
        else:
            raise credentialsException
    else:
        raise credentialsException


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
