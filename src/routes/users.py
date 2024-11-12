from typing import Annotated
from dotenv import dotenv_values
import psycopg2 
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from src.schemas import TokenData, User

import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

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
cur.execute(f"SET TIME ZONE 'America/Buenos_Aires';")

router = APIRouter()

@router.get("/profile", response_model=User)
async def userProfile(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userId: int = payload.get("id")
        if userId is None:
            raise credentials_exception
        token_data = TokenData(id=userId)
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception
    cur.execute('SELECT * FROM "Users" '+ f"where id = '{token_data.id}';")
    user = cur.fetchone()
    if user is None:
        raise credentials_exception
    userData = User(id=user[0], name=user[1], password=user[2], privileges=user[3], access=True)
    del userData.password
    return userData