from venv import create
from core.models import (
    ConstantCode,
    CropGrade,
    CropSeed,
    GradePrice,
    InHouseGrade,
    ProductGrade,
    Region,
    Season,
)
from ninja.orm import create_schema


RegionSchema = create_schema(Region)
CreateRegionSchema = create_schema(Region, exclude=["id"])

ProductGradeSchema = create_schema(ProductGrade)
CreateProductGradeSchema = create_schema(
    ProductGrade, exclude=["id", "created_on", "updated_on"]
)

ConstantCodeSchema = create_schema(ConstantCode, exclude=["id"])


CropGradeSchema = create_schema(CropGrade)
CreateCropGradeSchema = create_schema(
    CropGrade, exclude=["id", "created_on", "updated_on", "created_by", "is_active"]
)

CropSeedSchema = create_schema(CropSeed)
CreateCropSeedSchema = create_schema(CropSeed, exclude=["id"])


SeasonSchema = create_schema(Season)
CreateSeasonSchema = create_schema(Season, exclude=["id", "created_on", "updated_on"])


GradePriceSchema = create_schema(GradePrice)
CreateGradePriceSchema = create_schema(
    GradePrice, exclude=["id", "created_on", "updated_on"]
)


InHouseGradeSchema = create_schema(InHouseGrade)
CreateInHouseGradeSchema = create_schema(
    InHouseGrade, exclude=["id", "created_on", "updated_on"]
)
