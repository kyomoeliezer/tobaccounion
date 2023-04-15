from core.models import Region
from inventory import models
from inventory.forms import RegradingForm,WarehouseForm
from django.shortcuts import render, redirect,HttpResponse
from ninja.errors import HttpError
from django.core.paginator import Paginator
from shipment.forms import TrackForm
from market.models import Buyer ,Bale
from django.contrib import messages
from django.views.generic import CreateView,ListView,UpdateView,View,FormView,DeleteView,DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy


class Warehouse:
    def __init__(self):
        pass

    def create_warehouse(request):
        #try:
        template_name = "inventory/add_warehouse.html"
        if request.method == "POST":
            warehouse_form = WarehouseForm(request.POST or None)
            if not warehouse_form.is_valid():
                print(warehouse_form.errors)
                return render(request, template_name, {"form": warehouse_form})
            else:
                if 'NO' in warehouse_form.cleaned_data["is_for_sold_or_process"]:
                    warehouse_form.cleaned_data["is_for_sold_or_process"]=False
                else:
                    warehouse_form.cleaned_data["is_for_sold_or_process"] = True

                warehouse_form.cleaned_data["region"] = Region.objects.get(
                    region_name=warehouse_form.cleaned_data["region"]
                )
                warehouse = models.Warehouse.objects.create(
                    **warehouse_form.cleaned_data
                )
                warehouse.save()
                return Warehouse.get_warehouses(request)
        regions = Region.objects.filter(is_active=True).order_by("region_name")
        return render(request, template_name, {"regions": regions})
        #except:
        #    raise HttpError(500, "Internal Server Error")

    def edit_warehouse(request, warehouse_id):
        try:
            template_name = "inventory/add_warehouse.html"
            if request.method == "POST":
                warehouse_form = WarehouseForm(request.POST or None)
                if not warehouse_form.is_valid():
                    print(warehouse_form.errors)
                    return render(request, template_name, {"form": warehouse_form})
                else:
                    warehouse_form.cleaned_data["region"] = Region.objects.get(
                        region_name=warehouse_form.cleaned_data["region"]
                    )
                    models.Warehouse.objects.filter(id=warehouse_id).update(
                        **warehouse_form.cleaned_data
                    )
                    return Warehouse.get_warehouses(request)
            form = models.Warehouse.objects.get(id=warehouse_id)
            regions = Region.objects.filter(is_active=True).order_by("region_name")
            return render(request, template_name, {"regions": regions, "form": form})
        except:
            raise HttpError(500, "Internal Server Error")

    def get_warehouses(request):
        try:
            template_name = "inventory/warehouses.html"
            STAT = request.GET.get('status')
            header = 'Warehouse'
            is_ACTV = True
            if STAT:
                if int(STAT) == 0:
                    header = 'Inactive Warehouse'
                    is_ACTV = False

            warehouses = models.Warehouse.objects.filter(is_active=is_ACTV).order_by(
                "-created_on"
            )
            return render(request, template_name, {"page_obj": warehouses,'header':header})
        except:
           raise HttpError(500, "internal Server Error")

    def delete_warehouse(request, warehouse_id):
        try:
            warehouse = models.Warehouse.objects.filter(id=warehouse_id)
            if warehouse:
                warehouse.update(is_active=False)
                return Warehouse.get_warehouses(request)
            return Warehouse.get_warehouses(request)
        except:
            raise HttpError(500, "Internal Server Error")


class InventoryReport:
    def __init__(self):
        pass

class AddWarehouseView(LoginRequiredMixin,CreateView):

    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    form_class=WarehouseForm
    template_name='inventory/add_company.html'
    context_object_name='form'
    success_url=reverse_lazy('inventory:warehouses')

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            if not models.Warehouse.objects.filter(warehouse_name__iexact=request.POST.get('warehouse_name')).exists():
                form=form.save(commit=False)
                form.created_by_id=self.request.user.id
                form.save()
                messages.success(request, 'Succes!, Added')
                return redirect(reverse_lazy('inventory:warehouses'))
            else:
                messages.warning(request,'Name already exists')

        return render(self.request,self.template_name,{'form':form,'header':'Add Warehouse'})



class AddWarehouseView(LoginRequiredMixin,CreateView):

    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    form_class=WarehouseForm
    template_name='inventory/add_warehouse.html'
    context_object_name='form'
    success_url=reverse_lazy('inventory:warehouses')

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            if not models.Warehouse.objects.filter(warehouse_name__iexact=request.POST.get('warehouse_name')).exists():
                form=form.save(commit=False)
                form.created_by_id=self.request.user.id
                form.save()
                messages.success(request, 'Succes!, Added')
                return redirect(reverse_lazy('inventory:warehouses'))
            else:
                messages.warning(request,'Name already exists')

        return render(self.request,self.template_name,{'form':form,'header':'Add Warehouse'})

class UpdateWarehouseView(LoginRequiredMixin,UpdateView):

    login_url = reverse_lazy('login_user')
    redirect_field_name = 'next'
    model=models.Warehouse
    form_class=WarehouseForm
    template_name='inventory/add_warehouse.html'
    context_object_name='form'
    success_url=reverse_lazy('inventory:warehouses')

class RegradingList(LoginRequiredMixin,CreateView):
    login_url = "/login"
    redirect_field_name = 'next'
    form_class=RegradingForm
    template_name='bales/regrading.html'
    context_object_name='form'
    bayers=Buyer.objects.all()
    success_url=reverse_lazy('market:regrading')
    header='REGRADING'

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data()
        context['header']='REGRADING'
        context['bayers'] =self.bayers
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        #return HttpResponse(request.POST.get('buyer_code'))
        if form.is_valid():
            bayer=request.POST.get('buyer_code')
            bayer_code=Buyer.objects.filter(id=bayer).first()

            regrading=Bale.objects.filter(buyer_code=bayer_code.buyer_code).order_by('buyer_code')
            #return HttpResponse(bayer_code)
            #return HttpResponse(regrading)
            header=bayer_code.buyer_code+'  BUYER  '
            return render(request,self.template_name,{'regrading':regrading,'header':header,'form':self.form_class,'bayers':self.bayers})

        return render(request,self.form_class,{'form':form,'header':self.header,'bayers':self.bayers})
