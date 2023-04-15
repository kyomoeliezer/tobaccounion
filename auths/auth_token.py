from datetime import timedelta, datetime
from http.client import HTTPException
from ninja.errors import HttpError
from auths import schemas
from auths.views import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from ninja.security import HttpBearer
import jwt
import bcrypt
from auths import models
from voedsel.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    RESET_PASSWORD_TOKEN_TIME,
    SECRET_KEY as secret_key,
    ALGORITHM as algorithm,
)
from auths import models
from ninja.security import HttpBearer
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import json


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        return Auth.authenticate_request(request, token)


class Auth:
    def __init__(self):
        pass

    def get_user_by_token(request):
        return Auth.authenticate_request(
            request, request.headers.get("Authorization")[7:]
        )

    def create_access_token(request, data: dict, expires_delta: timedelta = None):
        try:
            to_encode = data.copy()
            # if expires_delta:
            #     expire = datetime.utcnow() + expires_delta
            # else:
            #     expire = datetime.utcnow() + timedelta(minutes=60)
            # to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
            return encoded_jwt
        except:
            raise HttpError(500, "Internal server Error")

    def create_token_from_email(email: str):
        """
        Create a token that can be used to verify a reset password.

        Expires in 15 minutes.
        """
        try:
            to_encode = {
                "email": email,
            }
            expire = datetime.utcnow() + timedelta(
                minutes=int(RESET_PASSWORD_TOKEN_TIME)
            )
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
            return encoded_jwt
        except:
            raise HttpError(500, "Internal Server Error")

    def decode_access_token(request, data: str):
        try:
            return jwt.decode(data, secret_key, algorithm)
        except:
            raise HttpError(400, "Invalid Token was given")

    def check_username_password(request, user: schemas.UserAuthenticate):
        db_user = User.get_user_by_username(request, username=user.username)
        return bcrypt.checkpw(
            user.password.encode("utf-8"), db_user.password.encode("utf-8")
        )

    def get_account(request, id: int, DB_table):
        return DB_table.objects.filter("id" == id).first()

    def authenticate_user(request, user: schemas.UserAuthenticate):
        # try:
        db_user = User.get_user_by_username(request, username=user.username)
        if db_user is None:
            raise HttpError(
                400,
                "Incorrect Credentials ware given.",
            )
        elif db_user.is_active == False:
            raise HttpError(
                400,
                "Sorry the user Account is not active please communicate with your adminstartor to activate your account !!!",
            )
        else:
            is_password_correct = Auth.check_username_password(request, user)
            if is_password_correct is False:
                raise HttpError(400, "Incorrect Credentials ware given.")
            else:
                access_token_expires = timedelta(
                    minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
                )

                access_token = Auth.create_access_token(
                    request,
                    data={"sub": user.username},
                    expires_delta=access_token_expires,
                )
                current_user = Auth.authenticate_request(request, access_token)
                request.user = current_user
                auth_user = authenticate(username=user.username, password=user.password)
                auth_login(request, auth_user)
                login_log = models.LoginLog.objects.create(created_by=request.user)
                login_log.save()
                user_data = model_to_dict(current_user)
                user_data["id"] = current_user.id
                return {
                    "access_token": access_token,
                    "token_type": "Bearer",
                    "user_details": user_data,
                }

    # except:
    #     raise HttpError(500, "Internal Server Error")

    def authenticate_request(request, authorization: str):
        credentials_exception = HttpError(401, "Could not validate credentials")
        # try:
        payload = Auth.decode_access_token(request, data=authorization)
        try:
            token_data = models.User.objects.get(username=payload.get("sub"))
            return token_data
        except:
            raise credentials_exception
        # except jwt.PyJWTError:
        #     raise credentials_exception

    def logout(request, token):
        auth_logout(request)
        jwt.destroy(token)
        return "User has been logged out"
