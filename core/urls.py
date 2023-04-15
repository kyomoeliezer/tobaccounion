from unicodedata import name
from django.urls import path, re_path
from core.api import add_region, add_season

from core.models import Region, Season
from . import web

app_name = "core"
urlpatterns = [
    path("", web.Dashboard.index, name="dashboard"),
    path("seasons", web.Season.get_seasons, name="seasons"),
    path("add-season", web.Season.add_season, name="add-season"),
    path("add-region", web.Region.add_region, name="add-region"),
    path("regions", web.Region.get_regions, name="regions"),
    path("inactive-regions", web.Region.get_inactive_regions, name="inactive_regions"),
    re_path(
        r"^edit-region/(?P<region_id>[\w-]+)/$",
        web.Region.edit_region,
        name="edit-region",
    ),
    re_path(
        r"^delete-region/(?P<region_id>[\w-]+)/$",
        web.Region.delete_region,
        name="delete-region",
    ),
    path(
        "add-constant-code",
        web.ConstantCode.add_constant_code,
        name="add-constant-code",
    ),

    path("ticketprefix", web.ConstantCode.get_codes, name="ticket-prefix"),
    path("grades", web.Grade.get_grades, name="grades"),
    re_path(
        r"^edit-grade/(?P<grade_id>[\w-]+)/$",
        web.Grade.edit_grade,
        name="edit-grade",
    ),
    re_path(
        r"^delete-grade/(?P<grade_id>[\w-]+)/$",
        web.Grade.delete_grade,
        name="delete-grade",
    ),
    path("add-grade", web.Grade.add_grade, name="add-grade"),
    path("add-grade-price", web.GradePrice.price_years, name="add-grade-price"),
    path("grade-years", web.GradePrice.grade_years, name="grade-years"),
    # path("grade-prices", web.GradePrice.get_grade_prices, name="grade-prices"),
    re_path(
        r"^add-price/(?P<year_id>[\w-]+)/$",
        web.GradePrice.add_grade_price,
        name="add-price",
    ),
    re_path(
        r"^grade-prices/(?P<year_id>[\w-]+)/$",
        web.GradePrice.get_grade_prices,
        name="grade-prices",
    ),
    re_path(
        r"^edit-grade-price/(?P<price_id>[\w-]+)/$",
        web.GradePrice.edit_grade_price,
        name="edit-grade-price",
    ),
    re_path(
        r"^delete-grade-price/(?P<grade_price_id>[\w-]+)/$",
        web.GradePrice.delete_grade_price,
        name="delete-grade-price",
    ),
    path(
        "in-house-grades", web.InHouseGrade.get_in_house_grades, name="in-house-grades"
    ),
    re_path(
        r"^edit-in-house-grade/(?P<grade_id>[\w-]+)/$",
        web.InHouseGrade.edit_in_house_grade,
        name="edit-in-house-grade",
    ),
    re_path(
        r"^delete-in-house-grade/(?P<grade_id>[\w-]+)/$",
        web.InHouseGrade.delete_in_house_grade,
        name="delete-in-house-grade",
    ),
    path(
        "add-in-house-grade",
        web.InHouseGrade.add_in_house_grade,
        name="add-in-house-grade",
    ),
    path("product-grades", web.ProductGrade.get_product_grades, name="product-grades"),
    path(
        "add-product-grade",
        web.ProductGrade.add_product_grade,
        name="add-product-grade",
    ),
    re_path(
        r"^edit-product-grade/(?P<grade_id>[\w-]+)/$",
        web.ProductGrade.edit_product_grade,
        name="edit-product-grade",
    ),
    re_path(
        r"^delete-product-grade/(?P<grade_id>[\w-]+)/$",
        web.ProductGrade.delete_product_grade,
        name="delete-product-grade",
    ),
    path("crop-years", web.Season.get_seasons, name="crop-years"),
    path("add-crop-year", web.Season.add_season, name="add-crop-year"),
    re_path(
        r"^edit-crop-year/(?P<year_id>[\w-]+)/$",
        web.Season.edit_season,
        name="edit-crop-year",
    ),
    re_path(
        r"^delete-crop-year/(?P<season_id>[\w-]+)/$",
        web.Season.delete_season,
        name="delete-crop-year",
    ),
]
