from dotenv import dotenv_values, load_dotenv
from fastapi import HTTPException, responses
from starlette.middleware.base import BaseHTTPMiddleware

import jwt


configEnv = dotenv_values(".env")

SECRET_KEY = configEnv["JWT_KEY"]
ALGORITHM = "HS256"

def verify_access_token(request):
    token = request
    if request.headers["authorization"]:
        token = request.headers["authorization"].split(" ")
        if len(token) == 2:
            token = token[1]
        else:
            token = token[0]
    else:
        raise HTTPException(status_code=401, detail="unauthorized")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            verify_access_token(request)
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return responses.JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            return responses.JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
