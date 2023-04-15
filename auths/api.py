from auths.auth_token import GlobalAuth
from ninja import Router
from .views import *
from auths import schemas
from typing import List
from .views import User

# API router
api = Router()


@api.post("/add_user", response=schemas.UserSchema)
def add_user(request, userSchema: schemas.CreateUserSchema):
    return User.add_user(request, userSchema)


@api.get("/get_users", response=List[schemas.UserSchema])
def get_users(request):
    return User.get_users(request)


@api.patch("/update-user")
def update_user(request, user_data: schemas.UpdateUserSchema):
    return User.update_user(request, user_data)


@api.delete("/delete_user")
def delete_user(request, id: str):
    return User.delete_user(request, id)
