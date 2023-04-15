from ninja.orm import create_schema
from processing.models import ProcessingCentre, ProductBale


ProcessingCentreSchema = create_schema(ProcessingCentre)
CreateProcessingCentreSchema = create_schema(
    ProcessingCentre, exclude=["id", "created_on", "updated_on"]
)

ProductBaleSchema = create_schema(ProductBale)
createProductBaleSchema = create_schema(
    ProductBale, exclude=["id", "created_on", "updated_on"]
)
