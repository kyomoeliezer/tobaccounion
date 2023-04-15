from ninja import Router
from .auth_token import *
from auths import schemas
from typing import List

api = Router()


@api.post("/login", response=schemas.Token)
def login(request, loginSchema: schemas.UserAuthenticate):
    return Auth.authenticate_user(request, loginSchema)


@api.post("/authenticate", response=schemas.UserSchema)
def authenticate(request, token: str):
    return Auth.authenticate_request(request, token)
