from auths.models import LoginLog, Staff, User
from ninja.orm import create_schema
from ninja import Schema

UserSchema = create_schema(User)
CreateUserSchema = create_schema(
    User, exclude=["id", "date_joined", "last_login", "groups", "user_permissions"]
)

UpdateUserSchema = create_schema(
    User, exclude=["date_joined", "last_login", "groups", "user_permissions"]
)

StaffSchema = create_schema(Staff)
CreateStaffSchema = create_schema(Staff, exclude=["id", "created_on", "updated_on"])

LoginLogSchema = create_schema(LoginLog)
CreateLoginLogSchema = create_schema(
    LoginLog, exclude=["id", "created_on", "updated_on"]
)


class Token(Schema):
    access_token: str
    token_type: str
    user_details: object


class AuthToken(Schema):
    access_token: str


class TokenData(Schema):
    username: str = None


class UserAuthenticate(Schema):
    username: str
    password: str
