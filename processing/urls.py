from django.urls import path, re_path
from . import web

app_name = "processing"
urlpatterns = [
    path(
        "processing-centres/",
        web.Processing.get_processing_centres,
        name="processing-centres",
    ),
    path(
        "add-processing-centre/",
        web.Processing.add_processing_centre,
        name="add-processing-centre",
    ),
    re_path(
        r"^delete-processing-centre/(?P<centre_id>[\w-]+)/$",
        web.Processing.delete_processing_centre,
        name="delete-processing-centre",
    ),
]
