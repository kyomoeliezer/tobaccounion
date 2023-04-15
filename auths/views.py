from http.client import HTTPException

from django.contrib import messages
from auths import models
import bcrypt




class User:
    def __init__(self):
        pass

    def add_user(request, user_schema):
        try:
            if type(user_schema) != "dict":
                user_schema = user_schema.dict()
            hash_password = bcrypt.hashpw(
                user_schema["password"].encode("utf-8"), bcrypt.gensalt()
            )
            hashed_password = hash_password.decode("utf8")
            print("Schema", user_schema)
            user_schema["password"] = hashed_password
            user = models.User.objects.create(**user_schema)
            user.save()
            return user
        except:
            raise "Internal server Error"

    def get_users(request):
        try:
            users = models.User.objects.filter(is_active=True)
            return users
        except:
            pass

    def update_user(request, user_data):
        if type(user_data) != "dict":
            user_data = dict(user_data)
        user = models.User.objects.filter(id=user_data["id"])
        user_data.pop("id")
        user.update(**user_data)
        return "user updated successfully"

    def get_user_by_username(request, username: str):
        try:
            user = models.User.objects.filter(username=username)
            if user:
                return user[0]
            return None
        except:
            raise HTTPException(
                data={"status_code": 500, "detail": "Internal Server Error"}
            )

    def change_password(request, password_schema):
        try:
            if type(password_schema) != "dict":
                user = user.objects.get(**password_schema)
                user.save()
                return user

        except:
            pass

    def delete_user(request, id: str):
        try:
            user = models.User.objects.filter(id=id)[0]
            if user:
                user.delete()
                return "User has been deleted"
            return "user not found"

        except:
            raise "Internal Server Error"
