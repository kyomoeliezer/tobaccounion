from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required

from association import models
from core.models import Region
from . import forms
from ninja.errors import HttpError
from django.core.paginator import Paginator
from django.contrib import messages


class Farmer:
    def __init__(self):
        pass

    def add_farmer(request):
        """Add farmer by entered farmer details"""
        template_name = "society/add_farmer.html"
        message = ""
        if request.method == "POST":
            form = forms.FarmerForm(request.POST or None)
            if form.is_valid():
                if not models.Farmer.objects.filter(farmer_code__iexact=request.POST.get('farmer_code')).exists():

                    form.cleaned_data["society"] = models.Association.objects.filter(
                        name=form.cleaned_data["society"]
                    ).first()
                    form.cleaned_data["region"] = Region.objects.filter(
                        region_name=form.cleaned_data["region"]
                    ).first()
                    farmer = models.Farmer.objects.create(**form.cleaned_data)
                    farmer.save()
                    return redirect("/farmers")
                else:
                    messages.warning(request,'Farmer code already exists')

            messages.warning(request,'Invalid Input given')
        regions = Region.objects.filter(is_active=True).order_by("region_name")
        primary_societies = models.Association.objects.filter(is_active=True).order_by(
            "name"
        )
        return render(
            request,
            template_name,
            {
                "regions": regions,
                "primary_societies": primary_societies,
                "message": message,
            },
        )

    def edit_farmer(request, farmer_id):
        """edit farmer by entered farmer details"""
        template_name = "society/add_farmer.html"
        message = ""
        if request.method == "POST":
            form = forms.FarmerForm(request.POST or None)
            if form.is_valid():
                form.cleaned_data["society"] = models.Association.objects.get(
                    name=form.cleaned_data["society"]
                )
                form.cleaned_data["region"] = Region.objects.get(
                    region_name=form.cleaned_data["region"]
                )
                farmer = models.Farmer.objects.filter(id=farmer_id).update(
                    **form.cleaned_data
                )
                return redirect("/farmers")
            message = "Invalid Input was given"
        regions = Region.objects.filter(is_active=True).order_by("region_name")
        primary_societies = models.Association.objects.filter(is_active=True).order_by(
            "name"
        )
        form = models.Farmer.objects.get(id=farmer_id)
        return render(
            request,
            template_name,
            {
                "regions": regions,
                "primary_societies": primary_societies,
                "message": message,
                "form": form,
            },
        )
    def get_farmers(request):
        """Get (display) farmers"""
        header='Active Farmers'
        template_name = "society/farmers.html"
        farmers = models.Farmer.objects.filter(is_active=True).order_by("first_name")
        paginated_farmers = Paginator(farmers, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_farmers.get_page(page_number)
        return render(request, template_name, {"page_obj": farmers,'header':header})

    def get_inactive_farmers(request):
        """Get (display) farmers"""
        header = 'Inactive Farmers'
        template_name = "society/farmers.html"
        farmers = models.Farmer.objects.filter(is_active=False).order_by("farmer_code")
        paginated_farmers = Paginator(farmers, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_farmers.get_page(page_number)
        return render(request, template_name, {"page_obj": farmers,'header':header})

    def delete_farmer(request, farmer_id):
        """Delete farmer by farmer id"""
        farmer = models.Farmer.objects.get(id=farmer_id)
        if farmer.is_active:
            farmer.is_active=False
            messages.success(request, 'Farmer deactivated')
        else:
            farmer.is_active = True
            messages.success(request,'Farmer activated')
        farmer.save()

        return redirect("/farmers")


class Society:
    def add_society(request):
        """Add Society by entered Society Details"""
        template_name = "society/add_society.html"
        if request.method == "POST":
            form = forms.SocietyForm(request.POST or None)
            if form.is_valid():
                if not models.Association.objects.filter(name__iexact=request.POST.get('name'),region_id=request.POST.get('region')).exists():

                    form.cleaned_data["region"] = Region.objects.filter(
                        id=request.POST.get('region')
                    ).first()
                    society = models.Association.objects.create(**form.cleaned_data)
                    society.save()
                    return redirect("/societies")
                else:
                    messages.warning(request,'Primary Society exists so we cant create again')
        regions = Region.objects.filter(is_active=True).order_by("region_name")
        return render(request, template_name, {"regions": regions})

    def edit_society(request, society_id):
        """edit Society by entered Society Details"""
        template_name = "society/add_society.html"
        if request.method == "POST":
            form = forms.SocietyForm(request.POST or None)
            if form.is_valid():
                form.cleaned_data["region"] = Region.objects.get(
                    region_name=form.cleaned_data["region"]
                )
                models.Association.objects.filter(id=society_id).update(
                    **form.cleaned_data
                )
                return redirect("/societies")
        form = models.Association.objects.get(id=society_id)
        regions = Region.objects.filter(is_active=True).order_by("region_name")
        return render(request, template_name, {"regions": regions, "form": form})

    def get_societies(request):
        """get (Display) Societies to the web system"""
        header = 'Societies'
        template_name = "society/societies.html"
        societies = models.Association.objects.filter(is_active=True).order_by(
            "-created_on"
        )
        paginated_societies = Paginator(societies, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_societies.get_page(page_number)
        return render(request, template_name, {"page_obj": societies,'header':header})

    def inactiveget_societies(request):
        """get (Display) Societies to the web system"""
        template_name = "society/societies.html"
        header='Inactive Societies'
        societies = models.Association.objects.filter(is_active=False).order_by(
            "-created_on"
        )
        paginated_societies = Paginator(societies, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_societies.get_page(page_number)

        return render(request, template_name, {"page_obj": societies,'header':header})

    def delete_society(request, society_id):
        """delete primary society with society id"""
        society = models.Association.objects.get(id=society_id)
        if society.is_active:
            society.is_active=False
        else:
            society.is_active = True
        society.save()

        return redirect("/societies")


class PrimarySocietyReport:
    def __init__(self):
        pass
