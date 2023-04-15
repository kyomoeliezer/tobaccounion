from genericpath import exists
from math import prod
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from auths.models import Staff
from core import models
from django.contrib import messages
from market.models import Bale, Market, MarketTicketRequest, MarketTiket, Ticket
from processing.models import ProductCategory
from shipment.models import (
    MarketProcessingShipmentBale,
    MarketWarehouseShipmentBale,
    WarehouseProcessingShipmentBale,
    WarehouseShipmentBale,
)
from . import forms
from ninja.errors import HttpError
from django.core.paginator import Paginator

from django.http import Http404, HttpResponseRedirect
from django.db.models import ProtectedError,Count,F,Q,Case,When,Value,FloatField,Sum


class Dashboard:
    def __init__(self):
        pass

    @login_required(login_url="/login")
    def index(request):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        template_name = "core/dashboard/index.html"
        tickets = Ticket.objects.filter(is_active=True).count()
        used_tickets = Bale.objects.filter(is_active=True).count()
        ticketsids=list(Bale.objects.values_list('ticket_id',flat=True))
        available_tickets = Ticket.objects.filter(~Q(id__in=ticketsids)&Q(is_used=False)).count()
        market_requests = MarketTicketRequest.objects.filter(is_active=True).count()
        
        product_categories = ProductCategory.objects.filter(is_active=True).count()
        shipments = [
            MarketWarehouseShipmentBale.objects.filter(is_active=True).count(),
            MarketProcessingShipmentBale.objects.filter(is_active=True).count(),
            WarehouseShipmentBale.objects.filter(is_active=True).count(),
            WarehouseProcessingShipmentBale.objects.filter(is_active=True).count(),
        ]
        return render(
            request,
            template_name,
            {
                "tickets": tickets,
                "used_tickets": used_tickets,
                "available_tickets": available_tickets,
                "market_requests": market_requests,
                "shipments": shipments,
            },
        )


class Grade:
    def __init__(self):
        pass

    def add_grade(request):
        template_name = "core/grade/add_grade.html"
        if request.method == "POST":
            form = forms.GradeForm(request.POST or None)
            if form.is_valid():
                if models.CropGrade.objects.filter(**form.cleaned_data).exists():
                    grade_name = form.cleaned_data["grade_name"]
                    message = f"Grade Name {grade_name} Already Exists"
                    return render(request, template_name, {"message": message})
                crop_grade = models.CropGrade.objects.create(**form.cleaned_data)
                crop_grade.save()
                return redirect("/grades")
        return render(request, template_name)

    def edit_grade(request, grade_id):
        template_name = "core/grade/add_grade.html"
        if request.method == "POST":
            form = forms.GradeForm(request.POST or None)
            if form.is_valid():
                models.CropGrade.objects.filter(id=grade_id).update(**form.cleaned_data)
                return redirect("/grades")
        form = models.CropGrade.objects.get(id=grade_id)
        return render(request, template_name, {"form": form})

    def get_grades(request):
        template_name = "core/grade/grades.html"
        STAT=request.GET.get('status')
        isActive = True
        header='Grades'
        if STAT:
            if int(STAT) ==0:
                isActive=False
                header = 'Inactive Grades'

        grades = models.CropGrade.objects.filter(is_active=isActive).order_by("grade_name")
        paginated_grades = Paginator(grades, 100)
        page_number = request.GET.get("page")
        page_obj = paginated_grades.get_page(page_number)
        return render(request, template_name, {"page_obj": grades,'header':header})

    def delete_grade(request, grade_id):
        grade = models.CropGrade.objects.filter(id=grade_id).first()

        if grade.is_active:
            grade.is_active=False
            messages.success(request,'Deactivated')
        else:
            grade.is_active=True
            messages.success(request,'Activated')
        grade.save()
        return redirect("/grades")


class Region:
    def add_region(request):
        """ "Add region"""
        template_name = "core/region/add_region.html"
        if request.method == "POST":
            form = forms.Region(request.POST or None)
            if form.is_valid():
                #return HttpResponse(request.POST.get('region_name'))
                if not models.Region.objects.filter(region_name__iexact=request.POST.get('region_name')).exists():

                    region = models.Region.objects.create(**form.cleaned_data)
                    region.save()
                    messages.warning(request, 'Region name already exists')
                    return redirect("/regions")
                else:
                    messages.warning(request,'Region name already exists')

        return render(request, template_name)

    def edit_region(request, region_id):
        """ "edit region"""
        template_name = "core/region/add_region.html"
        if request.method == "POST":
            form = forms.Region(request.POST or None)
            if form.is_valid():
                models.Region.objects.filter(id=region_id).update(**form.cleaned_data)
                return redirect("/regions")
        form = models.Region.objects.get(id=region_id)
        return render(request, template_name, {"form": form})

    def get_regions(request):
        header = ' Regions'
        template_name = "core/region/regions.html"
        regions = models.Region.objects.filter(is_active=True).order_by("region_name")
        paginated_regions = Paginator(regions, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_regions.get_page(page_number)
        return render(request, template_name, {"page_obj": regions,'header':header})

    def get_inactive_regions(request):
        header='Inactive Regions'
        template_name = "core/region/regions.html"
        regions = models.Region.objects.filter(is_active=False).order_by("region_name")
        paginated_regions = Paginator(regions, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_regions.get_page(page_number)
        return render(request, template_name, {"page_obj": regions,'header':header})

    def delete_region(request, region_id):
        """Delete Region by region id"""
        region = models.Region.objects.get(id=region_id)
        if region.is_active:
            region.is_active=False
        else:
            region.is_active = True
        region.save()
        return redirect("/regions")


class ConstantCode:
    def __init__(self):
        pass

    def add_constant_code(request):
        """Add constant code to be used as prefix in ticket_number"""

        template_name = "core/add_constant_code.html"
        seasons = models.Season.objects.filter(is_active=True).order_by('-created_on')
        if request.method == "POST":
            form = forms.ConstantCodeForm(request.POST or None)
            if form.is_valid():
                constant_code = models.ConstantCode.objects.create(**form.cleaned_data)
                constant_code.save()
                constant_code_now = models.ConstantCode.objects.filter(
                    is_active=True
                ).order_by("-created_on")
                if constant_code_now:
                    constant_code_now = constant_code_now[0]
                else:
                    constant_code_now = "No constant Code"

                return render(
                    request, template_name, {"constant_code": constant_code_now,'seasons':seasons}
                )

        constant_code_now = models.ConstantCode.objects.filter(is_active=True).order_by(
            "-created_on"
        )
        if constant_code_now:
            constant_code_now = constant_code_now[0]
        else:
            constant_code_now = "22222"

        return render(request, template_name, {"constant_code": constant_code_now,'seasons':seasons})
    def get_codes(request):
        template='core/constant_code.html'
        ST=request.POST.get('status')
        header='Ticket Prifix'
        ACtv = True
        if ST:
            if int(ST) == 0:
                header='Inactive Prifix'
                ACtv=False
        codes=models.ConstantCode.objects.all().order_by('-created_on')
        #return HttpResponse(codes.count())
        return render(request,template,{'header':header,'codes':codes})

class Season:
    def add_season(request):
        """Add season (Crop year) price of crops depend on crop year"""
        template_name = "core/season/add_season.html"
        if request.method == "POST":
            form = forms.SeasonForm(request.POST or None)
            if form.is_valid():
                if not models.Season.objects.filter(Q(season_name__iexact=request.POST.get('season_name'))).exists():
                    season = models.Season.objects.create(**form.cleaned_data)
                    season.save()
                    messages.success(request,'Created the season')
                    return redirect("/seasons")
                messages.warning(request, 'did not create, another season have same name')
        return render(request, template_name)

    def edit_season(request, year_id):
        """Edit season (Crop year) price of crops depend on crop year"""
        template_name = "core/season/add_season.html"
        if request.method == "POST":
            form = forms.SeasonForm(request.POST or None)
            if form.is_valid():
                models.Season.objects.filter(id=year_id).update(**form.cleaned_data)
                return redirect("/seasons")
        form = models.Season.objects.get(id=year_id)
        return render(request, template_name, {"form": form})

    def get_seasons(request):
        """Get all seasons (crop years)"""
        template_name = "core/season/seasons.html"
        ST=request.GET.get('status')
        ISACTV = True
        header='Season'
        if ST:
            if int(ST) == 0:
                ISACTV=False
                header = 'Inactive Season'
        seasons = models.Season.objects.filter(is_active=ISACTV).order_by("-created_on")
        paginated_seasons = Paginator(seasons, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_seasons.get_page(page_number)
        return render(request, template_name, {"page_obj": page_obj,'header':header})

    def delete_season(request, season_id):
        """delete season (crop year) by season id"""

        season = models.Season.objects.filter(id=season_id)
        if season.first().is_active:
            season.update(is_active=False)
            messages.success(request,'Deactivated the seasoan')
        else:
            season.update(is_active=True)
            messages.success(request, 'Activated the seasoan')
        return redirect("/seasons")


class GradePrice:
    def grade_years(request):
        """get (display) all grade years"""
        template_name = "core/grade/grade_years.html"
        seasons = models.Season.objects.filter(
            id__in=[
                price.season.id
                for price in models.GradePrice.objects.filter(is_active=True)
            ],
            is_active=True,
        ).order_by("-created_on")
        paginated_seasons = Paginator(seasons, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_seasons.get_page(page_number)
        return render(request, template_name, {"page_obj": page_obj})

    def price_years(request):
        """display years to view Grade prices (grade prices of particular crop year)"""
        template_name = "core/grade/add_grade_price_years.html"
        seasons = (
            models.Season.objects.filter(is_active=True)
            .exclude(
                id__in=[
                    price.season.id
                    for price in models.GradePrice.objects.filter(is_active=True)
                ]
            )
            .order_by("-created_on")
        )
        paginated_seasons = Paginator(seasons, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_seasons.get_page(page_number)
        return render(request, template_name, {"page_obj": page_obj})

    def add_grade_price(request, year_id):
        """Add grade price of particular crop year"""
        template_name = "core/grade/add_grade_price.html"
        if request.method == "POST":
            grades = request.POST.getlist("grade")
            prices = request.POST.getlist("price")
            list_data = dict(zip(grades, prices))
            for grade, price in list_data.items():
                grade_ = models.CropGrade.objects.get(grade_name=grade)
                season = models.Season.objects.get(id=year_id)
                if models.GradePrice.objects.filter(
                    grade=grade_, price=price, season=season
                ).exists():
                    season = models.Season.objects.get(id=year_id)
                    grades = (
                        models.CropGrade.objects.filter(is_active=True)
                        .exclude(
                            id__in=[
                                price.grade.id
                                for price in models.GradePrice.objects.filter(
                                    season_id=year_id
                                )
                            ]
                        )
                        .order_by("grade_name")
                    )
                    message = f"{grade} with price {price} on {season.season_name} already exists"
                    return render(
                        request,
                        template_name,
                        {
                            "grades": grades,
                            "year_id": year_id,
                            "season": season.season_name,
                            "message": message,
                        },
                    )
                grade_price = models.GradePrice.objects.create(
                    grade=grade_, price=price, season=season
                )
                grade_price.save()
            return GradePrice.get_grade_prices(request, year_id)
        season = models.Season.objects.get(id=year_id)
        grades = (
            models.CropGrade.objects.filter(is_active=True)
            .exclude(
                id__in=[
                    price.grade.id
                    for price in models.GradePrice.objects.filter(season_id=year_id)
                ]
            )
            .order_by("grade_name")
        )
        return render(
            request,
            template_name,
            {"grades": grades, "year_id": year_id, "season": season.season_name},
        )

    def edit_grade_price(request, price_id):
        """Edit grade price of particular crop year"""
        template_name = "core/grade/add_grade_price.html"
        grades = models.GradePrice.objects.filter(id=price_id)
        season = grades[0].season
        if request.method == "POST":
            grades = request.POST.getlist("grade")
            prices = request.POST.getlist("price")
            list_data = dict(zip(grades, prices))
            for grade, price in list_data.items():
                models.GradePrice.objects.filter(id=price_id).update(price=price)
            return GradePrice.get_grade_prices(request, season.id)
        form = models.GradePrice.objects.get(id=price_id)
        return render(
            request,
            template_name,
            {
                "grades": grades,
                "year_id": season.id,
                "season": season.season_name,
                "form": form,
            },
        )

    def get_grade_prices(request, year_id):
        """Get grade prices of the particular year (crop year -season)"""
        template_name = "core/grade/grade_prices.html"
        grade_prices = models.GradePrice.objects.filter(
            season__id=year_id, is_active=True
        ).order_by("grade__grade_name")
        paginated_grade_prices = Paginator(grade_prices, 100)
        page_number = request.GET.get("page")
        page_obj = paginated_grade_prices.get_page(page_number)
        season = models.Season.objects.get(id=year_id)
        return render(request, template_name, {"page_obj": grade_prices, "season": season})

    def delete_grade_price(request, grade_price_id):
        """delete grade price viewed in particular year"""
        if not models.GradePrice.objects.filter(id=grade_price_id).exists():
            return redirect("/grade-years")
        grade_price = models.GradePrice.objects.filter(id=grade_price_id)
        year_id = grade_price[0].season.id
        grade_price.update(is_active=False)
        return GradePrice.get_grade_prices(request, year_id)


class InHouseGrade:
    def add_in_house_grade(request):
        """add in house grades"""
        template_name = "core/grade/add_in_house_grade.html"
        if request.method == "POST":
            form = forms.InHouseGradeForm(request.POST or None)
            if form.is_valid():
                if not  models.InHouseGrade.objects.filter(grade__iexact=request.POST.get('grade')).exists():
                    in_house_grade = models.InHouseGrade.objects.create(**form.cleaned_data)
                    in_house_grade.save()
                    messages.success(request, request.POST.get('grade') + ' added')
                    return redirect("/in-house-grades")
                else:
                    messages.warning(request,request.POST.get('grade')+' Already exists')

        return render(request, template_name)

    def edit_in_house_grade(request, grade_id):
        """edit in house grades"""
        template_name = "core/grade/add_in_house_grade.html"
        if request.method == "POST":
            form = forms.InHouseGradeForm(request.POST or None)
            if form.is_valid():
                models.InHouseGrade.objects.filter(id=grade_id).update(
                    **form.cleaned_data
                )
                return redirect("/in-house-grades")
        form = models.InHouseGrade.objects.get(id=grade_id)
        return render(request, template_name, {"form": form})

    def get_in_house_grades(request):
        """get all in house grades"""

        template_name = "core/grade/in_house_grades.html"
        STAT = request.GET.get('status')
        isActive = True
        header = 'Inhouse Grades'
        if STAT:
            if int(STAT) == 0:
                isActive = False
                header = 'Inactive Inhouse Grades'
        in_house_grades = models.InHouseGrade.objects.filter(is_active=isActive).order_by(
            "-created_on"
        )
        paginated_in_house_grades = Paginator(in_house_grades, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_in_house_grades.get_page(page_number)
        return render(request, template_name, {"page_obj": in_house_grades,'header':header})

    def delete_in_house_grade(request, grade_id):
        """delete in house grade by grade id"""
        grade = models.InHouseGrade.objects.filter(id=grade_id)
        grade=grade.first()
        if grade.is_active:
            grade.is_active = False
            messages.success(request, 'Deactivated')
        else:
            grade.is_active = True
            messages.success(request, 'Activated')
        grade.save()
        return redirect(reverse("core:in-house-grades"))


class ProductGrade:
    def add_product_grade(request):
        """Add grade to be used for processed crops (product)"""
        template_name = "core/grade/add_product_grade.html"
        if request.method == "POST":
            form = forms.ProductGradeForm(request.POST or None)
            if form.is_valid():
                product_grade = models.ProductGrade.objects.create(**form.cleaned_data)
                product_grade.save()
                return redirect("/product-grades")
        return render(request, template_name)

    def edit_product_grade(request, grade_id):
        """Edit grade to be used for processed crops (product)"""
        template_name = "core/grade/add_product_grade.html"
        if request.method == "POST":
            form = forms.ProductGradeForm(request.POST or None)
            if form.is_valid():
                models.ProductGrade.objects.filter(id=grade_id).update(
                    **form.cleaned_data
                )
                return redirect("/product-grades")
        form = models.ProductGrade.objects.get(id=grade_id)
        return render(request, template_name, {"form": form})

    def get_product_grades(request):
        """Get (display) all product grades"""
        template_name = "core/grade/product_grades.html"
        product_grades = models.ProductGrade.objects.filter(is_active=True).order_by(
            "grade_name"
        )
        paginated_product_grades = Paginator(product_grades, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_product_grades.get_page(page_number)
        return render(request, template_name, {"page_obj": page_obj})

    def delete_product_grade(request, grade_id):
        """Delete product grade by product grade id"""
        grade = models.ProductGrade.objects.filter(id=grade_id)
        grade.update(is_active=False)
        return redirect("/in-house-grades")

    


class GeneralReport:
    def __init__(self):
        pass
