from fastapi import FastAPI, Request,responses, HTTPException
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.middlewares import checktoken
from src.main import api_router, api_router_public

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")
origins = ["*"]

private = FastAPI(title="fichadas-Auth", root_path="/priv", generate_unique_id_function=custom_generate_unique_id)
public = FastAPI(title="fichadas-Public", root_path="/pub", generate_unique_id_function=custom_generate_unique_id)

private.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
public.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@private.middleware("http")
async def checkToken(request: Request, call_next):
    try:
        checktoken.verify_access_token(request)
        response = await call_next(request)
        return response
    except HTTPException as exc:
        return responses.JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
    except Exception as exc:
        return responses.JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)

private.include_router(api_router)
public.include_router(api_router_public)

app=FastAPI()
app.mount("/priv", private)
app.mount("/pub", public)