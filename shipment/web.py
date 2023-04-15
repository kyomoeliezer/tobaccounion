
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from multiprocessing import process
from django.shortcuts import render, redirect,HttpResponse
from django.urls import reverse,reverse_lazy
from auths.models import Role, Staff
from inventory.models import Warehouse
from market.models import MarketTicketRequest, MarketTiket,Bale
from ninja.errors import HttpError
from core.models import ConstantCode,GradePrice
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from shipment import models as shipment_model
from processing.models import ProcessingCentre
from .forms import *
from datetime import datetime
from django.views.generic import CreateView,ListView,UpdateView,View,FormView,DeleteView,DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from voedsel.celery import app
from django.contrib import messages

from django.db.models import (
    IntegerField,
    FloatField,
    F,
    Sum,
    Value,
    When,
    Case,
    Count,
    Q,
    Min,
    Max,
)


def create_shipment_number(source, destination):
    shipment_number = (source[:2]).upper() + (destination[:2]).upper()
    shipment_number += str(datetime.now().strftime("%H-%M-%S"))
    return shipment_number

def create_shipment_number_custom():
    shipment_number = 'SHIP'
    shipment_number += str(datetime.now().strftime("%Y%d%m%H%M%S"))
    return shipment_number

def shipment_number(no):
    number = 'SH'
    shipment_number=''
    if int(no) < 10:
        shipment_number=shipment_number+'00'+str(no)
    elif int(no) < 100:
        shipment_number=shipment_number+'0'+str(no)
    elif int(no) >=100:
        shipment_number=shipment_number+''+str(no)

    return number+shipment_number



    return shipment_number


class ListTransportCompany(LoginRequiredMixin,ListView):
    login_url = "/login"
    redirect_field_name = 'next'
    model=shipment_model.TransportCompany
    template_name='shipment/company/companies.html'
    context_object_name='lists'
    order_by='-id'

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data()
        DAT=self.request.GET.get('status')
        isAct = True
        header = 'Transport Companies'
        if DAT:
            if int(DAT) == 0:
                isAct=False
                header='Inactive Companies'
        context['lists']=TransportCompany.objects.filter(is_active=isAct).order_by('-created_on')
        context['header']='ACTIVE COMPANIES'
        return context

class UpdateTransportCompany(LoginRequiredMixin,UpdateView):

    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    model=TransportCompany
    fields=['name','address']
    template_name='shipment/company/add_company.html'
    context_object_name='form'
    success_url=reverse_lazy('shipment:tcompanies')
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data()
        context['header']='UPDATE COMPANY'
        return context

class AddTransportCompany(LoginRequiredMixin,CreateView):

    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    form_class=CompanyForm
    template_name='shipment/company/add_company.html'
    context_object_name='form'
    success_url=reverse_lazy('shipment:tcompanies')

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            if not TransportCompany.objects.filter(name__iexact=request.POST.get('name')).exists():
                form=form.save(commit=False)
                form.created_by_id=self.request.user.id
                form.save()
                messages.success(request, 'Succes!, Added')
                return redirect(self.success_url)
            else:
                messages.warning(request,'Company already exists')

        return render(self.request,self.template_name,{'form':form,'header':'Add Comapny'})

class ActivateDeactivateCompany(LoginRequiredMixin,View):
    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'

    def get(self,*args,**kwargs):
        id=self.kwargs['pk']
        getT=TransportCompany.objects.get(id=id)
        if getT.is_active:
            getT.is_active=False
            messages.success(self.request, 'Deactivated')
        else:
            getT.is_active = True
            messages.success(self.request,'Activated')
        getT.save()
        return redirect(reverse_lazy('shipment:tcompanies'))







class Shipment:
    def __init__(self):
        pass

    def add_market_warehouse_shipment(request):
        """create shipment from market place to warehouse"""
        template_name = "shipment/add_market_warehouse_shipment.html"
        if request.method == "POST":
            form = MarketWarehouseShipmentForm(request.POST or None)
            if form.is_valid():
                shipment_number = create_shipment_number(
                    form.cleaned_data["market"].market_name,
                    form.cleaned_data["warehouse"].warehouse_name,
                )
                print("shipment_number", shipment_number)
                form.cleaned_data["market"] = Market.objects.filter(
                    market_name=form.cleaned_data["market"]
                ).first()
                form.cleaned_data["warehouse"] = Warehouse.objects.filter(
                    warehouse_name=form.cleaned_data["warehouse"]
                ).first()
                form.cleaned_data["driver"] = shipment_model.Driver.objects.filter(
                    full_name=form.cleaned_data["driver"]
                ).first()
                form.cleaned_data["personnel"] = Staff.objects.filter(
                    full_name=form.cleaned_data["personnel"]
                ).first()
                form.cleaned_data["personnel_receiver"] = Staff.objects.filter(
                    full_name=form.cleaned_data["personnel_receiver"]
                ).first()
                form.cleaned_data["track"] = shipment_model.Track.objects.filter(
                    track_name=form.cleaned_data["track"]
                ).first()
                form.cleaned_data["market_request"] = MarketTicketRequest.objects.filter(
                    ticket_request_name=form.cleaned_data["market_request"]
                ).latest('created_on')
                market_warehouse_shipment = MarketWarehouseShipment.objects.create(
                    **form.cleaned_data, shipment_number=shipment_number
                )
                market_warehouse_shipment.save()
                bales=Bale.objects.filter(market_request_id=market_warehouse_shipment.market_request_id,primary_weight__isnull=False).order_by('created_on')
                for bale in bales:
                    if not MarketWarehouseShipmentBale.objects.filter(bale_id=bale.id).exists():
                        MarketWarehouseShipmentBale.objects.create(shipment_id=market_warehouse_shipment.id, bale_id=bale.id)

                return redirect("/shipment/market-warehouse-shipments")
            else:
                error = "Invalid Data was given"
        markets = Market.objects.filter(is_active=True).order_by("market_name")
        warehouses = Warehouse.objects.filter(is_active=True).order_by("warehouse_name")
        drivers = shipment_model.Driver.objects.filter(is_active=True).order_by(
            "full_name"
        )
        tracks = shipment_model.Track.objects.filter(is_active=True).order_by(
            "track_name"
        )
        donemrequests_list=list(MarketWarehouseShipment.objects.values_list('market_request_id',flat=True))
        market_requests = MarketTicketRequest.objects.filter(Q(on_buying=False)&~Q(id__in=donemrequests_list)).order_by("created_on")
    
        staffs = Staff.objects.filter(
            role__role_name__in=[
                role.role_name for role in Role.objects.filter(is_active=True)
            ],
            is_active=True,
        ).order_by("full_name")
        return render(
            request,
            template_name,
            {
                "drivers": drivers,
                "tracks": tracks,
                "warehouses": warehouses,
                "markets": markets,
                "market_requests": market_requests,
                "staffs": staffs,
            },
        )

    def edit_market_warehouse_shipment(request, shipment_id):
        """edit shipment from market place to warehouse"""
        template_name = "shipment/add_market_warehouse_shipment.html"
        if request.method == "POST":
            form = MarketWarehouseShipmentForm(request.POST or None)
            if form.is_valid():
                form.cleaned_data["market"] = Market.objects.filter(
                    market_name=form.cleaned_data["market"]
                ).first()
                form.cleaned_data["warehouse"] = Warehouse.objects.filter(
                    warehouse_name=form.cleaned_data["warehouse"]
                ).first()
                form.cleaned_data["driver"] = shipment_model.Driver.objects.filter(
                    full_name=form.cleaned_data["driver"]
                ).first()
                form.cleaned_data["personnel"] = Staff.objects.filter(
                    full_name=form.cleaned_data["personnel"]
                ).first()
                form.cleaned_data["personnel_receiver"] = Staff.objects.filter(
                    full_name=form.cleaned_data["personnel_receiver"]
                ).first()
                form.cleaned_data["track"] = shipment_model.Track.objects.filter(
                    track_name=form.cleaned_data["track"]
                ).first()
                form.cleaned_data.pop("market_request")
                MarketWarehouseShipment.objects.filter(id=shipment_id).update(
                    **form.cleaned_data
                )
                return redirect("/shipment/market-warehouse-shipments")
            else:
                error = "Invalid Data was given"
        markets = Market.objects.filter(is_active=True).order_by("market_name")
        warehouses = Warehouse.objects.filter(is_active=True).order_by("warehouse_name")
        drivers = shipment_model.Driver.objects.filter(is_active=True).order_by(
            "full_name"
        )
        tracks = shipment_model.Track.objects.filter(is_active=True).order_by(
            "track_name"
        )
        staffs = Staff.objects.filter(
            role__role_name__in=[
                role.role_name for role in Role.objects.filter(is_active=True)
            ],
            is_active=True,
        ).order_by("full_name")
        form = MarketWarehouseShipment.objects.get(id=shipment_id)
        return render(
            request,
            template_name,
            {
                "drivers": drivers,
                "tracks": tracks,
                "warehouses": warehouses,
                "markets": markets,
                "staffs": staffs,
                "form": form,
            },
        )

    def get_market_warehouse_shipments(request):
        """get market warehouse shipments"""
        try:
            template_name = "shipment/market_warehouse_shipments.html"
            market_warehouse_shipments = MarketWarehouseShipment.objects.filter(
                is_active=True
            ).order_by("-created_on")
            paginated_market_warehouse_shipments = Paginator(
                market_warehouse_shipments, 10
            )
            page_number = request.GET.get("page")
            page_obj = paginated_market_warehouse_shipments.get_page(page_number)
            return render(request, template_name, {"page_obj": market_warehouse_shipments})
        except:
            raise HttpError(500, "Internal Server Error")

    def delete_market_warehouse_shipment(request, shipment_id):
        """delete market warehouse shipmets"""
        template_name = "shipment/market_warehouse_shipment.html"
        shipment = MarketWarehouseShipment.objects.filter(id=shipment_id)
        baleszipo=MarketWarehouseShipmentBale.objects.filter(Q(shipment_id=shipment_id)&Q(Q(transport_weight__isnull=False)|Q(received_weight__isnull=False))).exists()
        
        if not baleszipo:
            shipment_bales = MarketWarehouseShipmentBale.objects.filter(shipment_id=shipment[0].id)
            shipment_bales.delete()
            shipment.delete()
            return redirect("/shipment/market-warehouse-shipments")

        else:
            message = "Shipment was already deleted or does not exists"
            shipments = MarketWarehouseShipment.objects.filter(is_active=True).order_by(
                "-created_on"
            )
            paginated_shipments = Paginator(shipments, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_shipments.get_page(page_number)
            return render(
                request, template_name, {"page_obj": shipments, "message": message}
            )

    def market_warehouse_shipment_refresh(request,shipment_id):
        ship=MarketWarehouseShipment.objects.get(id=shipment_id)
        bales=Bale.objects.filter(market_request_id=ship.market_request_id,primary_weight__isnull=False).order_by('created_on')
        for bale in bales:
            if not MarketWarehouseShipmentBale.objects.filter(bale_id=bale.id).exists():
                MarketWarehouseShipmentBale.objects.create(shipment=ship, bale_id=bale.id)
        return redirect(reverse('shipment:market-warehouse-shipments'))




    def get_market_warehouse_details(request, shipment_id):
        template_name = "shipment/market_warehouse_details.html"
        shipmet_bales = MarketWarehouseShipmentBale.objects.filter(
            shipment_id=shipment_id
        )
        CAPTURING = MarketWarehouseShipmentBale.objects.filter(shipment_id=shipment_id).values('shipment_id').annotate(
            tickets=Count('id'),
            transported=Sum(
                    Case(
                        When(Q(transport_weight__isnull=False) & ~Q(transport_weight = 0), then=Value(1)),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),

            rcvd=Sum(
                    Case(
                        When(Q(received_weight__isnull=False) & ~Q(received_weight = 0), then=Value(1)),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
            rcvd_weightT=Sum(
                    Case(
                        When(Q(received_weight__isnull=False) & ~Q(received_weight = 0), then='received_weight'),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
            transport_weightT=Sum(
                    Case(
                        When(Q(transport_weight__isnull=False) & ~Q(transport_weight = 0), then='transport_weight'),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
        )

        paginated_shipments = Paginator(shipmet_bales, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_shipments.get_page(page_number)
        shipments=MarketWarehouseShipmentBale.objects.filter(shipment_id=shipment_id).order_by('created_on')
        shipment = MarketWarehouseShipment.objects.get(id=shipment_id)
        return render(
            request, template_name, {"page_obj": page_obj, "shipment": shipment,'CAPTURING':CAPTURING,'shipments':shipments}
        )

    def add_market_processing_shipment(request):
        template_name = "shipment/add_market_processing_shipment.html"
        if request.method == "POST":
            form = MarketProcessingShipmentForm(request.POST or None)
            if form.is_valid():
                shipment_number = create_shipment_number(
                    form.cleaned_data["market"].market_name,
                    form.cleaned_data["processing_centre"].centre_name,
                )
                form.cleaned_data["market"] = Market.objects.get(
                    market_name=form.cleaned_data["market"]
                )
                form.cleaned_data["processing_centre"] = ProcessingCentre.objects.get(
                    centre_name=form.cleaned_data["processing_centre"]
                )
                form.cleaned_data["driver"] = shipment_model.Driver.objects.get(
                    full_name=form.cleaned_data["driver"]
                )
                form.cleaned_data["personnel"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel"]
                )
                form.cleaned_data["personnel_receiver"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel_receiver"]
                )
                form.cleaned_data["track"] = shipment_model.Track.objects.get(
                    track_name=form.cleaned_data["track"]
                )
                form.cleaned_data["market_request"] = MarketTicketRequest.objects.get(
                    ticket_request_name=form.cleaned_data["market_request"]
                )
                market_processing_shipment = MarketProcessingShipment.objects.create(
                    **form.cleaned_data, shipment_number=shipment_number
                )
                market_processing_shipment.save()
                for ticket_ in [
                    market_ticket.ticket
                    for market_ticket in MarketTiket.objects.filter(
                        market_ticket_request=request.POST.get("market_request")
                    )
                ]:
                    bale = Bale.objects.filter(ticket_id=ticket_.id)[0]
                    shipment_bale = MarketProcessingShipmentBale.objects.create(
                        shipment=market_processing_shipment, bale=bale
                    )
                    shipment_bale.save()
                return redirect("/shipment/market-processing-shipments")
            error = "Invalid Input was given"
        markets = Market.objects.filter(is_active=True).order_by("market_name")
        processing_centres = ProcessingCentre.objects.filter(is_active=True).order_by(
            "centre_name"
        )
        drivers = shipment_model.Driver.objects.filter(is_active=True).order_by(
            "full_name"
        )
        tracks = shipment_model.Track.objects.filter(is_active=True).order_by(
            "track_name"
        )
        market_requests = (
            MarketTicketRequest.objects.filter(on_buying=False)
            .exclude(
                Q(
                    id__in=[
                        shipment.market_request.id
                        for shipment in MarketProcessingShipment.objects.filter(
                            is_active=True
                        )
                    ]
                )
                | Q(
                    id__in=[
                        shipment.market_request.id
                        for shipment in MarketWarehouseShipment.objects.filter(
                            is_active=True
                        )
                    ]
                )
            )
            .order_by("ticket_request_name")
        )
        staffs = Staff.objects.filter(
            role__role_name__in=[
                role.role_name for role in Role.objects.filter(is_active=True)
            ]
        ).order_by("full_name")
        return render(
            request,
            template_name,
            {
                "drivers": drivers,
                "tracks": tracks,
                "processing_centres": processing_centres,
                "markets": markets,
                "market_requests": market_requests,
                "staffs": staffs,
            },
        )

    def edit_market_processing_shipment(request, shipment_id):
        template_name = "shipment/add_market_processing_shipment.html"
        if request.method == "POST":
            form = MarketProcessingShipmentForm(request.POST or None)
            if form.is_valid():
                form.cleaned_data["market"] = Market.objects.get(
                    market_name=form.cleaned_data["market"]
                )
                form.cleaned_data["processing_centre"] = ProcessingCentre.objects.get(
                    centre_name=form.cleaned_data["processing_centre"]
                )
                form.cleaned_data["driver"] = shipment_model.Driver.objects.get(
                    full_name=form.cleaned_data["driver"]
                )
                form.cleaned_data["personnel"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel"]
                )
                form.cleaned_data["personnel_receiver"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel_receiver"]
                )
                form.cleaned_data["track"] = shipment_model.Track.objects.get(
                    track_name=form.cleaned_data["track"]
                )
                MarketProcessingShipment.objects.filter(id=shipment_id).update(
                    **form.cleaned_data
                )
                return redirect("/shipment/market-processing-shipments")
            error = "Invalid Input was given"
        markets = Market.objects.filter(is_active=True).order_by("market_name")
        processing_centres = ProcessingCentre.objects.filter(is_active=True).order_by(
            "centre_name"
        )
        drivers = shipment_model.Driver.objects.filter(is_active=True).order_by(
            "full_name"
        )
        tracks = shipment_model.Track.objects.filter(is_active=True).order_by(
            "track_name"
        )
        staffs = Staff.objects.filter(
            role__role_name__in=[
                role.role_name for role in Role.objects.filter(is_active=True)
            ]
        ).order_by("full_name")
        form = MarketProcessingShipment.objects.get(id=shipment_id)
        return render(
            request,
            template_name,
            {
                "drivers": drivers,
                "tracks": tracks,
                "processing_centres": processing_centres,
                "markets": markets,
                "staffs": staffs,
                "form": form,
            },
        )

    def get_market_processing_shipments(request):
        try:
            template_name = "shipment/market_processing_shipments.html"
            market_processing_shipments = MarketProcessingShipment.objects.filter(
                is_active=True
            ).order_by("-created_on")
            paginated_market_processing_shipments = Paginator(
                market_processing_shipments, 10
            )
            page_number = request.GET.get("page")
            page_obj = paginated_market_processing_shipments.get_page(page_number)
            return render(request, template_name, {"page_obj": page_obj})
        except:
            raise HttpError(500, "Internal Server Error")

    def delete_market_processing_shipment(request, shipment_id):
        template_name = "shipment/market_processing_shipment.html"
        shipment = MarketProcessingShipment.objects.filter(id=shipment_id)
        if not shipment.exists():
            message = "Shipment was already deleted"
            shipments = MarketProcessingShipment.objects.filter(
                is_active=True
            ).order_by("-created_on")
            paginated_shipments = Paginator(shipments, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_shipments.get_page(page_number)
            return render(
                request, template_name, {"page_obj": page_obj, "message": message}
            )
        shipment.delete()
        return redirect("/shipment/market-processing-shipments")

    def get_market_processing_details(request, shipment_id):
        template_name = "shipment/market_processing_details.html"
        shipmet_bales = MarketProcessingShipmentBale.objects.filter(
            shipment_id=shipment_id
        )
        paginated_shipments = Paginator(shipmet_bales, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_shipments.get_page(page_number)
        shipment = MarketProcessingShipment.objects.get(id=shipment_id)
        return render(
            request, template_name, {"page_obj": page_obj, "shipment": shipment}
        )

    def add_warehouse_shipment(request):
        template_name = "shipment/add_warehouse_shipment.html"
        if request.method == "POST":
            form = WarehouseShipmentForm(request.POST or None)
            if form.is_valid():
                shipment_number = create_shipment_number(
                    form.cleaned_data["from_warehouse"].warehouse_name,
                    form.cleaned_data["to_warehouse"].warehouse_name,
                )
                form.cleaned_data["from_warehouse"] = Warehouse.objects.get(
                    warehouse_name=form.cleaned_data["from_warehouse"]
                )
                form.cleaned_data["to_warehouse"] = Warehouse.objects.get(
                    warehouse_name=form.cleaned_data["to_warehouse"]
                )
                form.cleaned_data["driver"] = shipment_model.Driver.objects.get(
                    full_name=form.cleaned_data["driver"]
                )
                form.cleaned_data["personnel"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel"]
                )
                form.cleaned_data["personnel_receiver"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel_receiver"]
                )
                form.cleaned_data["track"] = shipment_model.Track.objects.get(
                    track_name=form.cleaned_data["track"]
                )
                warehouse_shipment = WarehouseShipment.objects.create(
                    **form.cleaned_data, shipment_number=shipment_number
                )
                warehouse_shipment.save()
                initial_ticket = request.POST.get("start_ticket")
                final_ticket = request.POST.get("end_ticket")
                for bale in range(int(initial_ticket), int(final_ticket) + 1):
                    bale_ = Bale.objects.filter(ticket__ticket_number=str(bale))
                    if (
                        not bale_
                        or form.cleaned_data["from_warehouse"]
                        == form.cleaned_data["to_warehouse"]
                    ):
                        WarehouseShipment.objects.filter(
                            id=warehouse_shipment.id
                        ).delete()
                        if not bale_:
                            message = f"There is no bale with ticket {initial_ticket} in the stock"
                        if (
                            form.cleaned_data["from_warehouse"]
                            == form.cleaned_data["to_warehouse"]
                        ):
                            message = f"warehouse can`t be the same, you cant ship within the same warehouse"
                        warehouses = Warehouse.objects.filter(is_active=True).order_by(
                            "warehouse_name"
                        )
                        drivers = shipment_model.Driver.objects.filter(
                            is_active=True
                        ).order_by("full_name")
                        tracks = shipment_model.Track.objects.filter(
                            is_active=True
                        ).order_by("track_name")
                        return render(
                            request,
                            template_name,
                            {
                                "drivers": drivers,
                                "tracks": tracks,
                                "warehouses": warehouses,
                                "message": message,
                            },
                        )
                    bale_ = bale_[0]
                    warehouse_bale = WarehouseShipmentBale.objects.create(
                        shipment=warehouse_shipment, bale=bale_
                    )
                warehouse_bale.save()
                return redirect("/shipment/warehouse-shipments")
            error = "Invalid Inputs ware given"
        warehouses = Warehouse.objects.filter(is_active=True).order_by("warehouse_name")
        drivers = shipment_model.Driver.objects.filter(is_active=True).order_by(
            "full_name"
        )
        tracks = shipment_model.Track.objects.filter(is_active=True).order_by(
            "track_name"
        )
        staffs = Staff.objects.filter(
            role__role_name__in=[
                role.role_name for role in Role.objects.filter(is_active=True)
            ]
        ).order_by("full_name")
        return render(
            request,
            template_name,
            {
                "drivers": drivers,
                "tracks": tracks,
                "warehouses": warehouses,
                "staffs": staffs,
            },
        )

    def edit_warehouse_shipment(request, shipment_id):
        template_name = "shipment/add_warehouse_shipment.html"
        if request.method == "POST":
            form = WarehouseShipmentForm(request.POST or None)
            if form.is_valid():
                form.cleaned_data["from_warehouse"] = Warehouse.objects.get(
                    warehouse_name=form.cleaned_data["from_warehouse"]
                )
                form.cleaned_data["to_warehouse"] = Warehouse.objects.get(
                    warehouse_name=form.cleaned_data["to_warehouse"]
                )
                form.cleaned_data["driver"] = shipment_model.Driver.objects.get(
                    full_name=form.cleaned_data["driver"]
                )
                form.cleaned_data["personnel"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel"]
                )
                form.cleaned_data["personnel_receiver"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel_receiver"]
                )
                form.cleaned_data["track"] = shipment_model.Track.objects.get(
                    track_name=form.cleaned_data["track"]
                )
                WarehouseShipment.objects.filter(id=shipment_id).update(
                    **form.cleaned_data
                )
                return redirect("/shipment/warehouse-shipments")
            error = "Invalid Inputs ware given"
        warehouses = Warehouse.objects.filter(is_active=True).order_by("warehouse_name")
        drivers = shipment_model.Driver.objects.filter(is_active=True).order_by(
            "full_name"
        )
        tracks = shipment_model.Track.objects.filter(is_active=True).order_by(
            "track_name"
        )
        staffs = Staff.objects.filter(
            role__role_name__in=[
                role.role_name for role in Role.objects.filter(is_active=True)
            ]
        ).order_by("full_name")
        form = WarehouseShipment.objects.get(id=shipment_id)
        return render(
            request,
            template_name,
            {
                "drivers": drivers,
                "tracks": tracks,
                "warehouses": warehouses,
                "staffs": staffs,
                "form": form,
            },
        )

    def get_warehouse_shipments(request):
        template_name = "shipment/warehouse_shipments.html"
        shipments = WarehouseShipment.objects.filter(is_active=True).order_by(
            "-created_on"
        )
        paginated_shipments = Paginator(shipments, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_shipments.get_page(page_number)
        return render(request, template_name, {"page_obj": page_obj})

    def delete_warehouse_shipment(request, shipment_id):
        template_name = "shipment/warehouse_shipments.html"
        shipment = WarehouseShipment.objects.filter(id=shipment_id)
        if not shipment.exists():
            message = "Shipment was already deleted"
            shipments = WarehouseShipment.objects.filter(is_active=True).order_by(
                "-created_on"
            )
            paginated_shipments = Paginator(shipments, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_shipments.get_page(page_number)
            return render(
                request, template_name, {"page_obj": page_obj, "message": message}
            )
        shipment.delete()
        return redirect("/shipment/warehouse-shipments")

    def get_warehouse_details(request, shipment_id):
        template_name = "shipment/warehouse_details.html"
        shipmet_bales = WarehouseShipmentBale.objects.filter(shipment_id=shipment_id)
        paginated_shipments = Paginator(shipmet_bales, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_shipments.get_page(page_number)
        shipment = WarehouseShipment.objects.get(id=shipment_id)
        return render(
            request, template_name, {"page_obj": page_obj, "shipment": shipment}
        )

    def add_warehouse_processing_shipment(request):
        template_name = "shipment/add_warehouse_processing_shipment.html"
        if request.method == "POST":
            form = WarehouseProcessingShipmentForm(request.POST or None)
            if form.is_valid():
                shipment_number = create_shipment_number(
                    form.cleaned_data["warehouse"].warehouse_name,
                    form.cleaned_data["processing_centre"].centre_name,
                )
                form.cleaned_data["warehouse"] = Warehouse.objects.get(
                    warehouse_name=form.cleaned_data["warehouse"]
                )
                form.cleaned_data["processing_centre"] = ProcessingCentre.objects.get(
                    centre_name=form.cleaned_data["processing_centre"]
                )
                form.cleaned_data["driver"] = shipment_model.Driver.objects.get(
                    full_name=form.cleaned_data["driver"]
                )
                form.cleaned_data["personnel"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel"]
                )
                form.cleaned_data["personnel_receiver"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel_receiver"]
                )
                form.cleaned_data["track"] = shipment_model.Track.objects.get(
                    track_name=form.cleaned_data["track"]
                )
                warehouse_shipment = WarehouseProcessingShipment.objects.create(
                    **form.cleaned_data, shipment_number=shipment_number
                )
                warehouse_shipment.save()
                initial_ticket = request.POST.get("start_ticket")
                final_ticket = request.POST.get("end_ticket")
                for bale in range(int(initial_ticket), int(final_ticket) + 1):
                    bale_ = Bale.objects.filter(ticket__ticket_number=str(bale))
                    if not bale_:
                        WarehouseShipment.objects.filter(
                            id=warehouse_shipment.id
                        ).delete()
                        message = f"There is no bale with ticket {initial_ticket} in the stock"
                        warehouses = Warehouse.objects.filter(is_active=True).order_by(
                            "warehouse_name"
                        )
                        drivers = shipment_model.Driver.objects.filter(
                            is_active=True
                        ).order_by("full_name")
                        tracks = shipment_model.Track.objects.filter(
                            is_active=True
                        ).order_by("track_name")
                        return render(
                            request,
                            template_name,
                            {
                                "drivers": drivers,
                                "tracks": tracks,
                                "warehouses": warehouses,
                                "message": message,
                            },
                        )
                    bale_ = bale_[0]
                    warehouse_bale = WarehouseProcessingShipmentBale.objects.create(
                        shipment=warehouse_shipment, bale=bale_
                    )
                    warehouse_bale.save()
                return redirect("/shipment/warehouse-processing-shipments")
            error = "Invalid Input was given"
            return render(request, template_name, {"message": error})
        warehouses = Warehouse.objects.filter(is_active=True).order_by("warehouse_name")
        processing_centres = ProcessingCentre.objects.filter(is_active=True).order_by(
            "centre_name"
        )
        drivers = shipment_model.Driver.objects.filter(is_active=True).order_by(
            "full_name"
        )
        tracks = shipment_model.Track.objects.filter(is_active=True).order_by(
            "track_name"
        )
        staffs = Staff.objects.filter(
            role__role_name__in=[
                role.role_name for role in Role.objects.filter(is_active=True)
            ]
        ).order_by("full_name")
        return render(
            request,
            template_name,
            {
                "drivers": drivers,
                "tracks": tracks,
                "warehouses": warehouses,
                "processing_centres": processing_centres,
                "staffs": staffs,
            },
        )

    def edit_warehouse_processing_shipment(request, shipment_id):
        template_name = "shipment/add_warehouse_processing_shipment.html"
        if request.method == "POST":
            form = WarehouseProcessingShipmentForm(request.POST or None)
            if form.is_valid():
                form.cleaned_data["warehouse"] = Warehouse.objects.get(
                    warehouse_name=form.cleaned_data["warehouse"]
                )
                form.cleaned_data["processing_centre"] = ProcessingCentre.objects.get(
                    centre_name=form.cleaned_data["processing_centre"]
                )
                form.cleaned_data["driver"] = shipment_model.Driver.objects.get(
                    full_name=form.cleaned_data["driver"]
                )
                form.cleaned_data["personnel"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel"]
                )
                form.cleaned_data["personnel_receiver"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel_receiver"]
                )
                form.cleaned_data["track"] = shipment_model.Track.objects.get(
                    track_name=form.cleaned_data["track"]
                )
                WarehouseProcessingShipment.objects.filter(id=shipment_id).update(
                    **form.cleaned_data
                )
                return redirect("/shipment/warehouse-processing-shipments")
            error = "Invalid Input was given"
            return render(request, template_name, {"message": error})
        warehouses = Warehouse.objects.filter(is_active=True).order_by("warehouse_name")
        processing_centres = ProcessingCentre.objects.filter(is_active=True).order_by(
            "centre_name"
        )
        drivers = shipment_model.Driver.objects.filter(is_active=True).order_by(
            "full_name"
        )
        tracks = shipment_model.Track.objects.filter(is_active=True).order_by(
            "track_name"
        )
        staffs = Staff.objects.filter(
            role__role_name__in=[
                role.role_name for role in Role.objects.filter(is_active=True)
            ]
        ).order_by("full_name")
        form = WarehouseProcessingShipment.objects.get(id=shipment_id)
        return render(
            request,
            template_name,
            {
                "drivers": drivers,
                "tracks": tracks,
                "warehouses": warehouses,
                "processing_centres": processing_centres,
                "staffs": staffs,
                "form": form,
            },
        )

    def get_warehouse_processing_shipments(request):
        template_name = "shipment/warehouse_processing_shipments.html"
        shipments = WarehouseProcessingShipment.objects.filter(is_active=True).order_by(
            "-created_on"
        )
        paginated_shipments = Paginator(shipments, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_shipments.get_page(page_number)
        return render(request, template_name, {"page_obj": page_obj})

    def delete_warehouse_processing_shipment(request, shipment_id):
        template_name = "shipment/warehouse_processing_shipments.html"
        shipment = WarehouseProcessingShipment.objects.filter(id=shipment_id)
        if not shipment.exists():
            message = "Shipment was already deleted"
            shipments = WarehouseProcessingShipment.objects.filter(
                is_active=True
            ).order_by("-created_on")
            paginated_shipments = Paginator(shipments, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_shipments.get_page(page_number)
            return render(
                request, template_name, {"page_obj": page_obj, "message": message}
            )
        shipment.delete()
        return redirect("/shipment/warehouse-processing-shipments")

    def get_warehouse_processing_details(request, shipment_id):
        template_name = "shipment/warehouse_processing_details.html"
        shipmet_bales = WarehouseProcessingShipmentBale.objects.filter(
            shipment_id=shipment_id
        )
        paginated_shipments = Paginator(shipmet_bales, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_shipments.get_page(page_number)
        shipment = WarehouseProcessingShipment.objects.get(id=shipment_id)
        return render(
            request, template_name, {"page_obj": page_obj, "shipment": shipment}
        )

    def add_sales_shipment(request):
        template_name = "shipment/add_sales_shipment.html"
        processing_centres = ProcessingCentre.objects.filter(is_active=True).order_by(
            "centre_name"
        )
        if request.method == "POST":
            form = SalesShipmentForm(request.POST or None)
            if form.is_valid():
                shipment_number = create_shipment_number(
                    form.cleaned_data["processing_centre"].centre_name,
                    form.cleaned_data["sales_location"],
                )
                form.cleaned_data["personnel"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel"]
                )
                form.cleaned_data["processing_centre"] = ProcessingCentre.objects.get(
                    centre_name=form.cleaned_data["processing_centre"]
                )
                shipment = SalesShipment.objects.create(
                    **form.cleaned_data, shipment_number=shipment_number
                )
                shipment.save()
                return redirect("/shipment/sales-shipments")
            error = "Invalid Input was given"
            return render(
                request,
                template_name,
                {"message": error, "processing_centres": processing_centres},
            )
        staffs = Staff.objects.filter(
            role__role_name__in=[
                role.role_name for role in Role.objects.filter(is_active=True)
            ]
        ).order_by("full_name")
        return render(
            request,
            template_name,
            {
                "processing_centres": processing_centres,
                "staffs": staffs,
            },
        )

    def edit_sales_shipment(request, shipment_id):
        template_name = "shipment/add_sales_shipment.html"
        processing_centres = ProcessingCentre.objects.filter(is_active=True).order_by(
            "centre_name"
        )
        if request.method == "POST":
            form = SalesShipmentForm(request.POST or None)
            if form.is_valid():
                form.cleaned_data["personnel"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel"]
                )
                form.cleaned_data["processing_centre"] = ProcessingCentre.objects.get(
                    centre_name=form.cleaned_data["processing_centre"]
                )
                SalesShipment.objects.filter(id=shipment_id).update(**form.cleaned_data)
                return redirect("/shipment/sales-shipments")
            error = "Invalid Input was given"
            return render(
                request,
                template_name,
                {"message": error, "processing_centres": processing_centres},
            )
        staffs = Staff.objects.filter(
            role__role_name__in=[
                role.role_name for role in Role.objects.filter(is_active=True)
            ]
        ).order_by("full_name")
        form = SalesShipment.objects.get(id=shipment_id)
        return render(
            request,
            template_name,
            {"processing_centres": processing_centres, "staffs": staffs, "form": form},
        )

    def get_sales_shipments(request):
        template_name = "shipment/sales_shipments.html"
        shipments = SalesShipment.objects.filter(is_active=True).order_by("-created_on")
        paginated_shipments = Paginator(shipments, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_shipments.get_page(page_number)
        return render(request, template_name, {"page_obj": page_obj})

    def delete_sales_shipment(request, shipment_id):
        template_name = "shipment/sales_shipments.html"
        shipment = SalesShipment.objects.filter(id=shipment_id)
        if not shipment.exists():
            message = "Shipment was already deleted"
            shipments = SalesShipment.objects.filter(is_active=True).order_by(
                "-created_on"
            )
            paginated_shipments = Paginator(shipments, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_shipments.get_page(page_number)
            return render(
                request, template_name, {"page_obj": page_obj, "message": message}
            )
        shipment.delete()
        return redirect("/shipment/sales-shipments")

    def get_sales_details(request, shipment_id):
        template_name = "shipment/sales_details.html"
        shipmet_bales = SalesShipmentBale.objects.filter(sales_shipment_id=shipment_id)
        paginated_shipments = Paginator(shipmet_bales, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_shipments.get_page(page_number)
        shipment = SalesShipment.objects.get(id=shipment_id)
        return render(
            request, template_name, {"page_obj": page_obj, "shipment": shipment}
        )


class Track:
    def __init__(self):
        pass

    def add_track(request):
        template_name = "shipment/track/add_track.html"
        if request.method == "POST":
            form = TrackForm(request.POST or None)
            if form.is_valid():
                if shipment_model.Track.objects.filter(
                    Q(reg_number=form.cleaned_data["reg_number"])|Q(document_number=form.cleaned_data["reg_number"])
                ).exists():
                    document_number = form.cleaned_data["document_number"]
                    reg_number = form.cleaned_data["reg_number"]
                    message = f"Track with reg_number {reg_number} or document {document_number} already exists"
                    return render(request, template_name, {"message": message})
                track = shipment_model.Track.objects.create(**form.cleaned_data)
                track.save()
                if track:
                    return redirect("/shipment/tracks")
        campanies = TransportCompany.objects.filter(is_active=True).order_by('-created_on')
        return render(request, template_name,{'companies':campanies,'header':''})

    def edit_track(request, track_id):
        template_name = "shipment/track/add_track.html"
        if request.method == "POST":
            form = TrackForm(request.POST or None)
            if form.is_valid():
                shipment_model.Track.objects.filter(id=track_id).update(
                    **form.cleaned_data
                )
                return redirect("/shipment/tracks")
        form = shipment_model.Track.objects.get(id=track_id)
        campanies = TransportCompany.objects.filter(is_active=True).order_by('-created_on')
        return render(request, template_name, {"form": form,'companies':campanies})

    def get_tracks(request):
        template_name = "shipment/track/tracks.html"
        STAT = request.GET.get('status')
        header = 'Active Tracks'
        is_ACTV = True
        if STAT:
            if int(STAT) == 0:
                header = 'Inactive Tracks'
                is_ACTV = False

        tracks = shipment_model.Track.objects.filter(is_active=is_ACTV).order_by(
            "track_name"
        )

        return render(request, template_name, {"page_obj": tracks,'header':header})

    def delete_track(request, track_id):
        template_name = "shipment/track/tracks.html"
        track = shipment_model.Track.objects.filter(id=track_id)
        trunckf = track.first()
        if trunckf.is_active:
            trunckf.is_active = False
            messages.success(request, 'Deactivated ')
        else:
            trunckf.is_active = True
            messages.success(request, 'Deactivated ')
        trunckf.save()
        return redirect("/shipment/tracks")


class Driver:
    def __init__(self):
        pass

    def add_driver(request):
        template_name = "shipment/driver/add_driver.html"
        if request.method == "POST":
            form = DriverForm(request.POST or None)
            if form.is_valid():
                return HttpResponse(request.POST)
                if shipment_model.Driver.objects.filter(
                   Q(license=form.cleaned_data["license"])|Q(phone_number=form.cleaned_data["phone_number"])
                ).exists():
                    license = form.cleaned_data["license"]
                    phone_number = form.cleaned_data["phone_number"]
                    message = f"Driver with license {license}  or phone number {phone_number} already exists"
                    return render(request, template_name, {"message": message})
                driver = shipment_model.Driver.objects.create(**form.cleaned_data)

                driver.save()
                return redirect("/shipment/drivers")
        campanies=TransportCompany.objects.filter(is_active=True).order_by('-created_on')
        return render(request, template_name,{'companies':campanies})

    def edit_driver(request, driver_id):
        template_name = "shipment/driver/add_driver.html"
        if request.method == "POST":
            form = DriverForm(request.POST or None)

            if form.is_valid():
                shipment_model.Driver.objects.filter(id=driver_id).update(
                    **form.cleaned_data
                )
                return redirect("/shipment/drivers")
        form = shipment_model.Driver.objects.get(id=driver_id)
        companies = TransportCompany.objects.filter(is_active=True).order_by('-created_on')
        return render(request, template_name, {"form": form,'companies':companies})

    def get_drivers(request):
        template_name = "shipment/driver/drivers.html"
        STAT=request.GET.get('status')
        header='Active Drivers'
        is_ACTV = True
        if STAT:
            if int(STAT) == 0:
                header = 'Inactive Drivers'
                is_ACTV=False
        #return HttpResponse(is_ACTV)

        drivers = shipment_model.Driver.objects.filter(is_active=is_ACTV).order_by(
            "full_name"
        )


        return render(request, template_name, {"page_obj": drivers,'header':header})

    def delete_driver(request, driver_id):
        template_name = "shipment/driver/drivers.html"
        driver = shipment_model.Driver.objects.filter(id=driver_id)
        driverf=driver.first()
        if driverf.is_active:
            driverf.is_active=False
            messages.success(request,'Deactivated ')
        else:
            driverf.is_active = True
            messages.success(request, 'Deactivated ')
        driverf.save()

        return redirect("/shipment/drivers")


class ShipmentReport:
    def __init__(self):
        pass

"""
GENERAL SHIPMENT
"""
class AddGeneralShipmentView(LoginRequiredMixin,CreateView):

    login_url ="/login"
    redirect_field_name = 'next'
    form_class=GeneralShipmentForm
    template_name='shipment/custom/add_general_shipment.html'
    context_object_name='form'
    success_url=reverse_lazy('shipment:list-custom-shipment')

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            maxno=shipment_model.GeneralShipment.objects.aggregate(no=Max('shipmentno'))
            no=0
            if maxno['no']:
                no=int(maxno['no'])
            form.shipmentno = no+1
            form.shipment_number = shipment_number(no+1)
            form.save()
            return redirect(self.success_url)
        return render(self.request,self.template_name,{'form':form})

class AddEmailReceiverView(LoginRequiredMixin,CreateView):

    login_url ="/login"
    redirect_field_name = 'next'
    form_class=GeneralEmailForm
    template_name='shipment/custom/add_email.html'
    context_object_name='form'
    success_url=reverse_lazy('shipment:list-email-receivers')


class ListEmailReceiversView(LoginRequiredMixin,ListView):
    login_url = "/login"
    redirect_field_name = 'next'
    model=shipment_model.SendingShipmentEmail
    template_name='shipment/custom/list_email_receivers.html'
    context_object_name='lists'
    order_by='-id'

class DeleteEmailReceiversView(LoginRequiredMixin,View):
    login_url = "/login"
    redirect_field_name = 'next'
    
    model=shipment_model.SendingShipmentEmail
    success_url=reverse_lazy('shipment:list-email-receivers')
    def get(self,*args,**kwargs):
        shipment_model.SendingShipmentEmail.objects.filter(id=self.kwargs['pk']).delete()
        return redirect(self.success_url)


class ListGeneralShipmentView(LoginRequiredMixin,ListView):
    login_url = "/login"
    redirect_field_name = 'next'
    model=shipment_model.GeneralShipment
    template_name='shipment/custom/general_shipment.html'
    context_object_name='lists'
    order_by='-id'
    success_url=reverse_lazy('shipment:list-custom-shipment')
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data()
        context['constn']=ConstantCode.objects.first().code_number
        context['header']='CURRENT SHIPMENTS'
        context['lists']=GeneralShipment.objects.filter(Q(is_closed_transporting=False)|Q(is_closed_transporting__isnull=True)).order_by('shipmentno')
        context['totals']=GeneralShipmentBale.objects.filter(general_shipment__is_closed_transporting=False).aggregate(bls=Count('id'),summ=Sum('transport_weight'))
        context['summaries']=GeneralShipmentBale.objects.filter(general_shipment__is_closed_transporting=False).values(fromw=F('general_shipment__from_warehouse'),tow=F('general_shipment__to_warehouse'),shipmentno=F('general_shipment__shipment_number'),gid=F('general_shipment_id'),is_closed=F('general_shipment__is_closed_transporting')).annotate(bls=Count('id'),summ=Sum('transport_weight')).order_by('general_shipment__created_on')
        return context


class ListGeneralShipmentDoneView(LoginRequiredMixin,ListView):
    login_url = "/login"
    redirect_field_name = 'next'
    model=shipment_model.GeneralShipment
    template_name='shipment/custom/general_shipment.html'
    context_object_name='lists'
    order_by='-id'
    success_url=reverse_lazy('shipment:list-custom-shipment')
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data()
        context['constn']=ConstantCode.objects.first().code_number
        context['header']='COMPLETED SHIPMENTS'
        context['lists']=GeneralShipment.objects.filter(is_closed_transporting=True).order_by('shipmentno')
        context['totals']=GeneralShipmentBale.objects.filter(general_shipment__is_closed_transporting=True).aggregate(
            bls=Count('id'),summ=Sum('transport_weight')
                )
        context['summaries']=GeneralShipmentBale.objects.filter(general_shipment__is_closed_transporting=True).values(fromw=F('general_shipment__from_warehouse'),tow=F('general_shipment__to_warehouse'),shipmentno=F('general_shipment__shipment_number'),gid=F('general_shipment_id'),is_closed=F('general_shipment__is_closed_transporting')).annotate(bls=Count('id'),summ=Sum('transport_weight')).order_by('general_shipment__created_on')
        return context
class UpdateGeneralShipmentView(LoginRequiredMixin,UpdateView):
    login_url = "/login"
    redirect_field_name = 'next'
    model=shipment_model.GeneralShipment
    form_class=GeneralShipmentForm
    template_name='shipment/custom/add_general_shipment.html'
    context_object_name='form'
    success_url=reverse_lazy('shipment:list-custom-shipment')

class DeleteGeneralShipmentView(LoginRequiredMixin,View):
    login_url = "/login"
    redirect_field_name = 'next'
    
    model=shipment_model.GeneralShipment
    success_url=reverse_lazy('shipment:list-custom-shipment')
    def get(self,*args,**kwargs):
        shipment_model.GeneralShipment.objects.filter(id=self.kwargs['pk']).delete()
        return redirect(self.success_url)

class RemoveBaleonGeneralShipmentBaleView(LoginRequiredMixin,View):
    login_url = "/login"
    redirect_field_name = 'next'
    
    model=shipment_model.GeneralShipmentBale
    success_url=reverse_lazy('shipment:list-custom-shipment')
    def get(self,*args,**kwargs):
        shp_id=shipment_model.GeneralShipmentBale.objects.get(id=self.kwargs['pk']).general_shipment_id
        shipment_model.GeneralShipmentBale.objects.filter(id=self.kwargs['pk']).delete()
        return redirect(reverse('market-warehouse-details',kwargs={'shipment_id':shp_id}))

class DetailGeneralShipmentView(LoginRequiredMixin,DetailView):
    login_url = "/login"
    redirect_field_name = 'next'
   
    model=shipment_model.GeneralShipment
    form_class=GeneralShipmentForm
    template_name='shipment/custom/general_shipment_detail.html'
    context_object_name='shipment'
    success_url=reverse_lazy('shipment:list-custom-shipment')
    order_by=('-id')

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data()
        context['header']='MAGEFA-'+GeneralShipment.objects.get(id=self.kwargs['pk']).shipment_number
        context['constn']=ConstantCode.objects.first().code_number
        context['bales']=GeneralShipmentBale.objects.filter(general_shipment_id=self.kwargs['pk']).order_by('bale__ticket__created_on')
        context['total']=GeneralShipmentBale.objects.filter(general_shipment_id=self.kwargs['pk']).aggregate(total=Count('id'),kg=Sum('transport_weight'))
        return context


class ChangeGeneralShipmentNoView(LoginRequiredMixin,View):
    login_url = "/login"
    redirect_field_name = 'next'
    
    model=shipment_model.GeneralShipment
    success_url=reverse_lazy('shipment:list-custom-shipment')
    def get(self,*args,**kwargs):
        maxno=shipment_model.GeneralShipment.objects.aggregate(no=Max('shipmentno'))
        no=0
        if maxno['no']:
            no=maxno['no']

        shipments=shipment_model.GeneralShipment.objects.all().order_by('created_on')
        no=0
        for ship in shipments:
            no=no+1
            ship.shipment_number=shipment_number(no)
            ship.save()

        return HttpResponse(no)


"""
END OF GENERAL SHIPMENTS
"""
class FileSendEmailToProcessing(LoginRequiredMixin,View):
    login_url = "/login"
    redirect_field_name = 'next'

    def get(self,request,*args,**kwargs):
        import mimetypes
        import random
        ship=GeneralShipment.objects.get(id=self.kwargs['pk'])

        filename=''+str(ship.shipment_number)+'.txt'
        filepath = 'files/'+filename
        bales=GeneralShipmentBale.objects.filter(general_shipment_id=self.kwargs['pk']).order_by('bale__ticket__no')
        #with open(filename, 'a') as f:
        constn=ConstantCode.objects.first().code_number
        import random
        #f= open(filepath,'w')
        
        line=''
        #return HttpResponse(bales.count())
        for bl in bales:
            line += (bl.bale.market_request.sales_date).strftime("%m/%d/%Y")+';'+ship.track.reg_number+';'+str(constn)+str(bl.bale.ticket.ticket_number)+';'+bl.bale.verified_grade.grade_name+';'+''+bl.bale.in_house_grade.grade+';'+str(bl.transport_weight)+';'+str(ship.shipment_number)+'\n'
            
        with  open(filepath, "w") as file:
            #content = "Hello, Welcome to Python Tutorial !! \n"
            file.write(line)
            file.close()
        ######SEND EMAIL#####

        from django.core.mail import EmailMessage, get_connection
        from django.conf import settings
        frp=None
        #if request.method == "POST":
        emails=list(shipment_model.SendingShipmentEmail.objects.values_list('email',flat=True)) 
        with get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, username=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD, use_tls=settings.EMAIL_USE_TLS  ) as connection:  
           subject = ship.shipment_number+' Shipment as per  '+str(datetime.today())
           email_from = settings.EMAIL_HOST_USER  
           recipient_list = emails 
           message = 'Dear Team \n'
           message +=' Attached shippment number '+str(ship.shipment_number)+'. On any case please reply to this email'
           message +='\n \n Best Regards '
           message +='\n Capture Software(automatic)'
           reply_to=['esterghuliku@gmail.com','kyomo89elieza@gmail.com']
           headers={'Message-ID': str(ship.shipment_number)},
           email=EmailMessage(subject, message, email_from, recipient_list,reply_to=reply_to, connection=connection)
           email.attach_file(filepath)
           email.send()
        ship.is_sent_email=True
        ship.save()
        GeneralShipment.objects.filter(id=self.kwargs['pk']).update(is_sent_email=True)
        messages.success(request,'Sent to all recipents')
        return redirect(reverse('shipment:detail-custom-shipment',kwargs={'pk':ship.id}))
        

class FileForImporting(LoginRequiredMixin,View):
    login_url = "/login"
    redirect_field_name = 'next'

    def get(self,request,*args,**kwargs):
        import mimetypes
        import random
        ship=GeneralShipment.objects.get(id=self.kwargs['pk'])

        filename=''+str(ship.shipment_number)+'.txt'
        filepath = 'files/'+filename
        bales=GeneralShipmentBale.objects.filter(general_shipment_id=self.kwargs['pk']).order_by('bale__ticket__no')
        #with open(filename, 'a') as f:
        constn=ConstantCode.objects.first().code_number
        import random
        #f= open(filepath,'w')
        
        line=''
        #return HttpResponse(bales.count())
        for bl in bales:
            line += (bl.bale.market_request.sales_date).strftime("%m/%d/%Y")+';'+ship.track.reg_number+';'+str(constn)+str(bl.bale.ticket.ticket_number)+';'+bl.bale.verified_grade.grade_name+';'+''+bl.bale.in_house_grade.grade+';'+str(bl.transport_weight)+';'+str(ship.shipment_number)+'\n'
            
        with  open(filepath, "w") as file:
            #content = "Hello, Welcome to Python Tutorial !! \n"
            file.write(line)
            file.close()
     
      
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as fh:
                response = HttpResponse(fh.read(), content_type="application/text")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
                os.remove(filepath)
                return response
        raise Http404


class EndShipments(LoginRequiredMixin,View):
    login_url = "/login"
    redirect_field_name = 'next'

    def get(self,request,*args,**kwargs):
        import mimetypes
        import random
        ship=GeneralShipment.objects.filter(id=self.kwargs['pk']).update(is_closed_transporting=True)
        bales=GeneralShipmentBale.objects.filter(general_shipment_id=self.kwargs['pk'],transport_weight__isnull=False,bale__shipmentvalue__isnull=True)
        cont=0
        #Bale.objects.update(shipmentvalue=None)
        for bal in bales:

            priceob=GradePrice.objects.filter(grade_id=bal.bale.verified_grade.id).first()
            if priceob:
                val=round(priceob.price*bal.transport_weight,2)
                Bale.objects.filter(id=bal.bale_id).update(shipmentvalue=val)
                cont +=1

        return redirect(reverse('shipment:list-custom-shipment'))

class OpenShipments(LoginRequiredMixin,View):
    login_url = "/login"
    redirect_field_name = 'next'

    def get(self,request,*args,**kwargs):
        import mimetypes
        import random
        ship=GeneralShipment.objects.filter(id=self.kwargs['pk']).update(is_closed_transporting=False)
        bales=GeneralShipmentBale.objects.filter(general_shipment_id=self.kwargs['pk'],transport_weight__isnull=False,bale__shipmentvalue__isnull=True)
        cont=0
        #Bale.objects.update(shipmentvalue=None)
        for bal in bales:

            priceob=GradePrice.objects.filter(grade_id=bal.bale.verified_grade.id).first()
            if priceob:
                val=round(priceob.price*bal.transport_weight,2)
                Bale.objects.filter(id=bal.bale_id).update(shipmentvalue=val)
                cont +=1

        return redirect(reverse('shipment:list-custom-shipment'))

class RefreshshiingValue(LoginRequiredMixin,View):


    def get(self,request,*args,**kwargs):
        bales=GeneralShipmentBale.objects.filter(transport_weight__isnull=False,bale__shipmentvalue__isnull=True,general_shipment__is_closed_transporting=True)[:5000]
        cont=0
        #Bale.objects.update(shipmentvalue=None)
        for bal in bales:

            priceob=GradePrice.objects.filter(grade_id=bal.bale.verified_grade.id).first()
            if priceob:
                val=round(priceob.price*bal.transport_weight,2)
                Bale.objects.filter(id=bal.bale_id).update(shipmentvalue=val)
                cont +=1
        return redirect(reverse('report:shipped_value_report'))

class DeleteshiingTicket(LoginRequiredMixin,View):


    def get(self,request,*args,**kwargs):
        datfld=GeneralShipmentBale.objects.filter(id=self.kwargs['pk']).first()
        general_id=datfld.general_shipment_id
        GeneralShipmentBale.objects.filter(id=self.kwargs['pk']).delete()
        
        return redirect(reverse('shipment:detail-custom-shipment',kwargs={'pk':general_id}))






@app.task()
def process_uploaded_file(filepath='media/shipment/CSV-AUG-01.csv'):
    import csv
    html = ''
    filepath='media/shipment/JULY-ONLY-GOOD.csv'
    # Open a file with access mode 'a'
    file_object = open('background_import.txt', 'a')
    file_object.writelines(['nimeingia now'+str(datetime.now()),])
    file_object.close()
    file_object = open('background_import.txt', 'a')
    try:

        count=countE =countNwR=countNOt=countRE=countNotFound= 0
        bales = []
        with open(filepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            
            file_object.write(str(filepath)+'\n',)
            for row in reader:
                if (row['Bale Status']).strip() == 'Received':

                    ticket=(row['Barcode']).replace('22222','')
                    file_object.writelines(['nimeingia now'+str(ticket)+'\n',])
                    if  GeneralShipmentReceivedBales.objects.filter(bale__ticket__ticket_number=ticket).exists():
                        file_object.writelines(['IPO  '+str(countNotFound)+'\n',])
                        """
                        if ticket and row['Receiving Wt'] and row['Bale Status'] == 'Received':
                            GeneralShipmentReceivedBales.objects.filter(bale__ticket__ticket_number=ticket).update(receiving_weight=row['Receiving Wt'],receiving_grade=row['Receiving Grade'])
                            countRE +=1
                        else:
                            countNOt  +=1
                        """
                        countRE +=1

                    elif Bale.objects.filter(ticket__ticket_number=ticket).exists() and (row['Bale Status']).strip() == 'Received':

                        ship = GeneralShipment.objects.get(shipment_number=(row['Load Number']).strip())

                        bl=Bale.objects.filter(ticket__ticket_number=ticket).first()
                        inhouse=InHouseGrade.objects.filter(grade=(row['Receiving Grade']).strip()).first()
                        if row['Receiving Wt'] and ship:
                            file_object.writelines(['IPO-NEW-'+str(countNwR)+'\n',])
                            countNwR = +1
                            GeneralShipmentReceivedBales.objects.create(bale_id=bl.id,general_shipment_id=ship.id,receiving_grade=row['Receiving Grade'],receiving_weight=row['Receiving Wt'],is_received=True)
                    else:
                        file_object.writelines(['HAIPO KABISA'+str(countNotFound)+'\n',])
                        countNotFound +=1
                    #html += str(count) + ' - ' + row['Load Number'] + ' - ' + row['Dated'] + '   '+ row['Truck Number'] + '   '+ row['Barcode'] + '   '+ row['Receiving Wt']+'<br/>'
            # if bales:
            #    GeneralShipmentReceivedBales.objects.bulk_create(bales,10000)
            # Append 'hello' at the end of file
            wrdata=str(datetime.now())+' - UPDATED-'+str(countE)+' UPDATED-NEW- '+ str(countNwR)+' NOT-UPDATED- '+ str(countNOt)+' HAIPO KOKOTE-'+str(countNotFound)
            file_object.write(wrdata)
            # Close the file
            file_object.close()
            #return HttpResponse()

        return HttpResponse('TEST NOW')
    except Exception as e:
        wrdata=str(datetime.now())
        file_object.write(wrdata)
        #file_object.write(e)
        # Close the file
        file_object.close()
        return e



class IMPORT:
    def process_uploaded_file_now(request):
        data=process_uploaded_file(filepath='media/shipment/CSV-AUG-01.csv')
        return HttpResponse(data)

@app.task()
def process_csv(request):
    import csv
    import time
    GBist = []
    counter1 = 0
    #csv_file=open('D:/PROJECTS/tobacco/media/shipment/2022MGLReceivingReport.csv')
    csv_file = open('media/shipment/SEP152022.csv')

    data = csv.reader(csv_file)

    next(data)
    st = time.time()
    GeneralShipmentReceivedBales.objects.all().delete()
    for row in data:
        ship = None
        bl = None

        if row[0]:
            #counter1 += 1
            # print(row)

            ticket = (row[3]).replace('22222', '')
            try:
                bl = None  # Bale.objects.filter(ticket__ticket_number=ticket)[:1].get()
            except:
                bl = None

            try:
                ship = None  # GeneralShipment.objects.get(shipment_number=(row[2]).strip())
            except:
                ship = None

            if row[6] and row[3] and ticket:
                if (row[6]).strip() =='Received':

                    counter1 += 1
                    GBist.append(GeneralShipmentReceivedBales(baleno=(ticket).strip(),
                                                              truckno=(row[2]).strip(),
                                                              status=(row[6]).strip(),
                                                              general_shipmentno=(row[1]).strip(),
                                                              receiving_grade=(row[4]).strip(),
                                                              receiving_weight=(row[5]).strip(), is_received=True))

                    # GBist.append(GeneralShipmentReceivedBales(bale_id=bl.id, general_shipment_id=ship.id,receiving_grade=row[5],receiving_weight=row[6], is_received=True))
                    if len(GBist) > 2000:
                        GeneralShipmentReceivedBales.objects.bulk_create(GBist)
                        GBist = []
    if len(GBist) > 0:
        GeneralShipmentReceivedBales.objects.bulk_create(GBist)
        


    et = time.time()

    return HttpResponse(str(counter1) + ' executed in ' + str((et - st) / 60))


