import glob
import os
from http.client import HTTPException
from PIL import Image
from django.shortcuts import render
from core import models
from market.models import Ticket
from ninja.errors import HttpError
import qrcode
from barcode.writer import ImageWriter
from barcode import EAN13, ISBN10, Code128
from ninja.errors import HttpError
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from voedsel.settings import BASE_DIR
from xhtml2pdf import pisa
from django.conf import settings


# Create your views here.


def generate_qr_code(ticket_number):
    """_generate qr codes with ticket number_

    Args:
        ticket_number (_string_): _description_

    Returns:
        _type_: _description_
    """
    img = qrcode.make(ticket_number)
    location = "static/assets/qr_code/" + ticket_number + ".png"
    img.save(location)
    return location


def generate_bar_code(ticket_number):
    """Generate Bar codes

    Args:
        ticket_number str: string

    Raises:
        HttpError: Internal server error or other errors

    Returns:
        _type_: _description_
    """
    const_number = models.ConstantCode.objects.filter(is_active=True)
    if const_number.count() == 0:
        raise HttpError(
            404, "There is no Constant Number, please Add Constant Number for Barcode"
        )
    number = models.ConstantCode.objects.all()[0].code_number + ticket_number
    bar_code = Code128(number, writer=ImageWriter())
    location = "static/assets/bar_code/" + number
    bar_code.save(
        location,
        options={
            "text_distance": 1,
            "quiet_zone": 2.5,
            "module_height": 6,
            "font_size": 16,
        },
    )
    return location + ".png"


def rotate_bar_code(ticket):
    """Rotate barcode to fit horizontal on tickets"""
    im = Image.open(ticket.bar_code)
    im = im.rotate(90, expand=True)
    location = "static/assets/bar_code/rotated" + ticket.ticket_number + ".png"
    im.save(location)
    Ticket.objects.filter(id=ticket.id).update(rotated_bar_code=location)


def fetch_resources(uri, rel):
    """Fetch settings data"""
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri
    if not os.path.isfile(path):
        raise Exception("media URI must start with %s or %s" % (sUrl, mUrl))
    return path


def render_to_pdf(path: str, params, filename):
    """Render data to pdf"""
    template_path = path
    context = params
    filename = "media/tickets/" + str(params["tickets"][0].print_request.id) + ".pdf"
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="' + filename + '"'
    template = get_template(template_path)
    html = template.render(context)
    open_file = open(filename, "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=open_file, link_callback=fetch_resources)
    if pisaStatus.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    open_file.close()
    return filename


def genera_render_to_pdf(path: str, params, filename):
    """Render data to pdf"""
    template_path = path
    context = params
    filename = "media/tickets/" + str(params["tickets"][0].print_request.id) + ".pdf"
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="' + filename + '"'
    template = get_template(template_path)
    html = template.render(context)
    open_file = open(filename, "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=open_file, link_callback=fetch_resources)
    if pisaStatus.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    open_file.close()
    return filename


def delete_files_in_dir(path):
    """delete all files in particular directory"""
    dir = os.path.join(BASE_DIR, path)
    filelist = glob.glob(os.path.join(dir, "*"))
    for file in filelist:
        os.remove(file)


class Region:
    def __init__(self):
        pass

    def add_region(request, create_region_schema):
        try:
            """Add region with region schema"""
            if type(create_region_schema) != "dict":
                create_region_schema = create_region_schema.dict()

            region = models.Region.objects.create(**create_region_schema)
            region.save()
            return region
        except:
            raise HttpError(503, "Service Unavailable. Please retry later.")

    def get_regions(request):
        """get all regions"""
        try:
            regions = models.Region.objects.filter(is_active=True)
            return regions
        except:
            raise HTTPException(
                data={"status_code": 500, "detail": "Internal Server Error"}
            )

    def delete_region(request, id: str):
        """delete region by region id"""
        try:
            region = models.Region.objects.filter(id=id)
            if region:
                region[0].delete()
                return "Region has successful Deleted"
            raise HTTPException(
                data={
                    "status_code": 404,
                    "detail": "Region Not Found may be was already deleted",
                }
            )

        except:
            raise HTTPException(
                data={"status_code": 500, "detail": "Internal Server Error"}
            )


class CropGrade:
    def __init__(self):
        pass

    def add_crop_grade(request, create_crop_grade_schema):
        try:
            if type(create_crop_grade_schema) != "dict":
                create_crop_grade_schema = create_crop_grade_schema.dict()

            crop_grade = models.CropGrade.objects.create(
                **create_crop_grade_schema, created_by=request.user
            )
            crop_grade.save()
            return crop_grade
        except:
            raise

    def get_crop_grades(request):
        try:
            crop_grades = models.CropGrade.objects.filter(is_active=True)
            return crop_grades
        except:
            raise

    def delete_crop_grade(request, id):
        try:
            crop_grade = models.CropGrade.objects.filter(id=id)
            if crop_grade:
                crop_grade[0].delete()
                return "Crop Grade Successful deleted"
            return "Crop Grade not found may be was already deleted"
        except:
            raise


class CropType:
    def __init__(self):
        pass

    def add_crop_type(request, create_crop_type_schema: None):
        try:
            if type(create_crop_type_schema) != "dict":
                create_crop_type_schema = create_crop_type_schema.dict()
            create_crop_type_schema["crop_seed"] = models.CropSeed.objects.get(
                id=create_crop_type_schema["crop_seed"]
            )
            crop_type = models.CropType.objects.create(**create_crop_type_schema)
            crop_type.save()
            return crop_type
        except:
            raise

    def get_crop_types(request):
        try:
            crop_types = models.CropType.objects.filter(is_active=True)
            return crop_types
        except:
            raise

    def delete_crop_type(request, id: str):
        try:
            crop_type = models.CropType.objects.filter(id=id)
            if crop_type:
                crop_type[0].delete()
                return "Crop Type successful deleted"
            return "Crop Type not found, may be was already deleted"
        except:
            raise


class CropSeed:
    def __init__(self):
        pass

    def add_crop_seed(request, create_crop_seed_schema):
        try:
            if type(create_crop_seed_schema) != "dict":
                create_crop_seed_schema = create_crop_seed_schema.dict()

            crop_seed = models.CropSeed.objects.create(**create_crop_seed_schema)
            crop_seed.save()
            return crop_seed
        except:
            raise

    def get_crop_seeds(request):
        try:
            crop_seeds = models.CropSeed.objects.filter(is_active=True)
            return crop_seeds
        except:
            raise "Internal Server Error"

    def delete_crop_seed(request, id: str):
        try:
            crop_seed = models.CropSeed.objects.filter(id=id)
            if crop_seed:
                crop_seed[0].delete()
                return "Crop Seed successful Deleted"
            return "Crop seed Not found, may be was already Deleted"
        except:
            raise


class Season:
    def __init__(self):
        pass

    def create_season(request, create_season_schema):
        try:
            if type(create_season_schema) != "dict":
                create_season_schema = create_season_schema.dict()

            season = models.Season.objects.create(**create_season_schema)
            season.save()
            return season
        except:
            raise

    def get_seasons(request):
        try:
            seasons = models.Season.objects.filter(is_active=True)
            return seasons
        except:
            raise "Internal Server Error"

    def delete_season(request, id: str):
        try:
            season = models.Season.objects.filter(id=id)
            if season:
                season[0].delete()
                return "Season was successful Deleted"
            return "No season Found, may be was already deleted"
        except:
            raise "Internal Server Error"


class InHouseGrade:
    def __init__(self):
        pass

    def create_in_house_grade(request, create_in_house_grade__schema):
        try:
            if type(create_in_house_grade__schema) != "dict":
                create_in_house_grade__schema = create_in_house_grade__schema.dict()

            in_house_grade = models.InHouseGrade.objects.create(
                **create_in_house_grade__schema
            )
            in_house_grade.save()
            return in_house_grade
        except:
            raise "Internal Server Error"

    def get_in_house_grades(request):
        try:
            in_house_grades = models.InHouseGrade.objects.filter(is_active=True)
            return in_house_grades
        except:
            raise "Intrnal Server Error"

    def delete_in_house_grade(request, id: str):
        try:
            in_house_grade = models.InHouseGrade.objects.filter(id=id)
            if in_house_grade:
                in_house_grade[0].delete()
                return "InHouse Grade was successful Deleted"
            return "Inhouse Grade was not found, may be was deleted"
        except:
            raise "Internal Server Error"


def check_weight(request, percent_loss):
    weight_loss = models.WeightLoss.objects.all()[0].weight_loss
    if percent_loss > weight_loss:
        return {
            "loss": "The weight Loss is too high allowable loss is bellow "
            + weight_loss
        }
    return {"normal": "The weight Loss in on range"}


class ConstantCode:
    def __init__(self):
        pass

    def create_code(request, code):
        try:
            if type(code) != "dict":
                code = code.dict()
            constant_code = models.ConstantCode.objects.create(**code)
            constant_code.save()
            return constant_code
        except:
            raise HttpError(500, "Internal Server Error")

    def get_code(request):
        return models.ConstantCode.objects.all()[0]

    def delete_code(request, id: str):
        try:
            code = models.ConstantCode.objects.filter(id=id)
            if code:
                code[0].delete()
                return "code has been deleted successful"
            raise HttpError(404, "Constant code was not found")
        except:
            raise HttpError(500, "Internal Server Error")
