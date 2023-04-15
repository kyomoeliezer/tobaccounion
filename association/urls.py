from django.urls import path, re_path
from . import web

app_name = "association"
urlpatterns = [
    path("add-farmer", web.Farmer.add_farmer, name="add-farmer"),
    path("farmers", web.Farmer.get_farmers, name="farmers"),
    path("inactive-farmers", web.Farmer.get_inactive_farmers, name="inactive_farmers"),
    path("societies", web.Society.get_societies, name="societies"),
    path("inactive-societies", web.Society.inactiveget_societies, name="inactive_societies"),

    re_path(
        r"^delete-farmer/(?P<farmer_id>[\w-]+)/$",
        web.Farmer.delete_farmer,
        name="delete-farmer",
    ),
    re_path(
        r"^edit-farmer/(?P<farmer_id>[\w-]+)/$",
        web.Farmer.edit_farmer,
        name="edit-farmer",
    ),
    path("add-society", web.Society.add_society, name="add-society"),
    re_path(
        r"^delete-society/(?P<society_id>[\w-]+)/$",
        web.Society.delete_society,
        name="delete-society",
    ),
    re_path(
        r"^edit-society/(?P<society_id>[\w-]+)/$",
        web.Society.edit_society,
        name="edit-society",
    ),
]
