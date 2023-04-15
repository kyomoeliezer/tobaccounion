from auths.auth_token import GlobalAuth
from .views import *
from ninja import Router
from core import schemas
from typing import List


api = Router(auth=GlobalAuth())


@api.post("/add_region", response=schemas.RegionSchema)
def add_region(request, region: schemas.CreateRegionSchema):
    return Region.add_region(request, region)


@api.get("/get-regions", response=List[schemas.RegionSchema])
def get_regions(request):
    return Region.get_regions(request)


@api.post("/add-constant-code", response=schemas.ConstantCodeSchema)
def add_constant_code(request, code: schemas.ConstantCodeSchema):
    return ConstantCode.create_code(request, code)


@api.delete("/delete-constant-code")
def delete_constant_code(request, id: str):
    return ConstantCode.delete_code(request, id)


@api.post("/add-crop-seed", response=schemas.CropSeedSchema)
def add_crop_seed(request, crop_seed: schemas.CreateCropSeedSchema):
    return CropSeed.add_crop_seed(request, crop_seed)


@api.get("/get-crop-seeds", response=List[schemas.CropSeedSchema])
def get_crop_seeds(request):
    return CropSeed.get_crop_seeds(request)


@api.delete("/delete-crop-seed")
def delete_crop_seed(request, id: str):
    return CropSeed.delete_crop_seed(request, id)


@api.post("/add-crop-grade", response=schemas.CropGradeSchema)
def add_crop_grade(request, crop_grade: schemas.CreateCropGradeSchema):
    return CropGrade.add_crop_grade(request, crop_grade)


@api.get("/get-crop-grades", response=List[schemas.CropGradeSchema])
def get_crop_grades(request):
    return CropGrade.get_crop_grades(request)


@api.delete("/delete-crop-grade")
def delete_crop_grade(request, id: str):
    return CropGrade.delete_crop_grade(request, id)


@api.post("/add-in-house-grade", response=schemas.InHouseGradeSchema)
def add_in_house_grade(request, in_house_grade: schemas.CreateInHouseGradeSchema):
    return InHouseGrade.create_in_house_grade(request, in_house_grade)


@api.get("/get-in-house-grades", response=List[schemas.InHouseGradeSchema])
def get_in_house_grades(request):
    return InHouseGrade.get_in_house_grades(request)


@api.delete("/delete-in-house-grade")
def delete_in_house_grade(request, id: str):
    return InHouseGrade.delete_in_house_grade(request, id)


@api.post("/add-season", response=schemas.SeasonSchema)
def add_season(request, season: schemas.CreateSeasonSchema):
    return Season.create_season(request, season)


@api.get("/get-seasons", response=List[schemas.SeasonSchema])
def get_seasons(request):
    return Season.get_seasons(request)


@api.delete("/delete-season")
def delete_season(request, id: str):
    return Season.delete_season(request, id)
