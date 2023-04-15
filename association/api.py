from auths.auth_token import GlobalAuth
from ninja import Router
from .views import *
from association import schemas
from typing import List

# API router
api = Router(auth=GlobalAuth())


@api.post("/add-society", response=schemas.AssociationSchema)
def add_society(request, society: schemas.CreateAssociationSchema):
    return Society.create_society(request, society)


@api.get("/get-societies", response=List[schemas.AssociationSchema])
def get_societies(request):
    return Society.get_societies(request)


@api.delete("/delete-society")
def delete_society(request, id: str):
    return Society.delete_society(request, id)


@api.post("/add-farmer", response=schemas.FarmerSchema)
def add_farmer(request, farmer: schemas.CreateFarmerSchema):
    return Farmer.create_farmer(request, farmer)


@api.get("/get-farmers", response=List[schemas.FarmerSchema])
def get_farmers(request):
    return Farmer.get_farmers(request)


@api.delete("/delete-farmer")
def delete_farmer(request, id: str):
    return Farmer.delete_farmer(request, id)
