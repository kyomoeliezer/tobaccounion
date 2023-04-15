from association.models import Association, Farmer
from ninja.orm import create_schema


AssociationSchema = create_schema(Association)
CreateAssociationSchema = create_schema(
    Association, exclude=["id", "created_on", "updated_on", "created_by"]
)

FarmerSchema = create_schema(Farmer)
CreateFarmerSchema = create_schema(
    Farmer, exclude=["id", "created_on", "updated_on", "created_by"]
)
