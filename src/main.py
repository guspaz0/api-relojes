from fastapi import APIRouter

from src.routes import auth, users, zkpy, zkUser
#, novedades

api_router_public = APIRouter()
api_router_public.include_router(auth.router, prefix="/auth", tags=["auth"])


api_router = APIRouter()
api_router.include_router(users.router, prefix="/user", tags=["user"])
api_router.include_router(zkpy.router, prefix="/zk", tags=["zk"])
api_router.include_router(zkUser.router, prefix="/zk/user", tags=["zk/user"])


