from django.shortcuts import render
from association import models
from core.models import Region
from ninja.errors import HttpError

# Create your views here.


class Society:
    def __init__(self):
        pass

    def create_society(request, society_schema):
        try:
            if type(society_schema) != "dict":
                society_schema = society_schema.dict()
            society_schema["region"] = Region.objects.get(id=society_schema["region"])
            society = models.Association.objects.create(
                **society_schema, created_by=request.user
            )
            society.save()
            return society
        except:
            raise HttpError(500, "Internal Server Error")

    def get_societies(request):
        try:
            societies = models.Association.objects.filter(is_active=True)
            return societies
        except:
            raise HttpError(500, "Internal Server Error")

    def delete_society(request, society_id: str):
        try:
            society = models.Association.objects.filter(id=society_id)
            if society:
                society[0].delete()
                return "Society was successful Deleted"
            raise HttpError(404, "Society was not found may be was already deleted")
        except:
            raise HttpError(500, "Internal Server Error")


class Farmer:
    def __init__(self):
        pass

    def create_farmer(request, farmer_schema):
        # try:
        if type(farmer_schema) != "dict":
            farmer_schema = farmer_schema.dict()
        farmer_schema["association"] = models.Association.objects.get(
            id=farmer_schema["association"]
        )
        farmer_schema["region"] = Region.objects.get(id=farmer_schema["region"])
        farmer = models.Farmer.objects.create(**farmer_schema, created_by=request.user)
        farmer.save()
        return farmer

    # except:
    #     raise HttpError(500, "Internal Server Error")

    def get_farmers(request):
        try:
            farmers = models.Farmer.objects.filter(is_active=True)
            return farmers
        except:
            raise HttpError(500, "Internal Server Error")

    def delete_farmer(request, id: str):
        try:
            farmer = models.Farmer.objects.filter(id=id)
            if farmer:
                farmer[0].delete()
                return "Farmer has been deleted successful"
            raise HttpError(404, "Farmer was not found, may be was already Deleted")
        except:
            raise HttpError(500, "Internal Server Error")
