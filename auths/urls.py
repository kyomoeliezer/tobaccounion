from django.urls import path, re_path

from auths.models import Staff
from . import web

app_name = "auths"
urlpatterns = [
    path("login", web.Auths.login, name="login"),
    path("logout", web.Auths.logout, name="logout"),
    path(
        "add-default-password",
        web.Auths.set_default_password,
        name="add-default-password",
    ),
    path("add-staff", web.Staff.create_staff, name="add-staff"),
    path("add-user", web.Staff.create_user, name="add-user"),

    path("staff-members", web.Staff.get_staffs, name="staff-members"),
    path("inactive-staff-members", web.Staff.get_staffs_inactive, name="inactive-staff-members"),
    re_path(r"^(?P<pk>[\w-]+)/user-edit$",web.UpdateUserCvB.as_view(),name="update_user"),
    re_path(
        r"^edit-staff/(?P<staff_id>[\w-]+)/$",
        web.Staff.edit_staff,
        name="edit-staff",
    ),
    re_path(
        r"^delete-staff/(?P<staff_id>[\w-]+)/$",
        web.Staff.delete_staff,
        name="delete-staff",
    ),
    path("roles", web.Role.get_roles, name="roles"),
    path("inactiveroles", web.Role.get_roles_inactive, name="inactiveroles"),
    path("add-role", web.Role.add_role, name="add-role"),
    re_path(
        r"^edit-role/(?P<role_id>[\w-]+)/$",
        web.Role.edit_role,
        name="edit-role",
    ),
    re_path(
        r"^delete-role/(?P<role_id>[\w-]+)/$",
        web.Role.delete_role,
        name="delete-role",
    ),
]
