
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from multiprocessing import process
from django.shortcuts import render, redirect,HttpResponse
from django.urls import reverse,reverse_lazy
from auths.models import Role, Staff
from ninja.errors import HttpError
from payment.models import Payment
from django.contrib.auth.decorators import login_required
from .form import *
from market.models import Bale,MarketTicketRequest
from datetime import datetime
from django.views.generic import CreateView,ListView,UpdateView,View,FormView,DeleteView,DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import IntegerField,FloatField,F,Sum,Value,When,Case,Count,Q,Min,Max


"""
NEW PAYMENTS
"""
class AddNewPaymentView(LoginRequiredMixin,CreateView):

    login_url ="/login"
    redirect_field_name = 'next'
    form_class=PaymentForm
    template_name='payment/new.html'
    context_object_name='form'
    success_url=reverse_lazy('payment:payment_list')

    def get_context_data(self, **kwargs):
        kwargs['header']='Add Payment'
        return super().get_context_data(**kwargs)

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST,request.FILES)
        if form.is_valid():
            form=form.save(commit=False)
            form.created_by_id=request.user.id
            form.amount = (request.POST.get('amount')).replace(',','')
            form.save()
            return redirect(self.success_url)
        return render(self.request,self.template_name,{'form':form})

class UpdatePaymentView(LoginRequiredMixin,UpdateView):

    login_url ="/login"
    redirect_field_name = 'next'
    form_class=PaymentFormEdit
    model=Payment
    template_name='payment/new.html'
    context_object_name='form'
    success_url=reverse_lazy('payment:payment_list')
    def get_context_data(self, **kwargs):
        kwargs['header']='Update Payment'
        return super().get_context_data(**kwargs)


class PaymentLists(LoginRequiredMixin,ListView):
    login_url = "/login"
    redirect_field_name = 'next'
    model=Payment
    template_name='payment/lists.html'
    context_object_name='lists'
    queryset=Payment.objects.filter(is_canceled=False)
    order_by=['-id']
    success_url=reverse_lazy('payment:payment_list')
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data()
        context['header']='PAYMENTS'
        return context

class PaymentListsWithBalance(LoginRequiredMixin,ListView):
    login_url = "/login"
    redirect_field_name = 'next'
    model=Payment
    template_name='payment/lists_with_balance.html'
    context_object_name='lists'
    queryset=Bale.objects.filter(is_mannual=False,value__isnull=False,price__isnull=False).values(
        society_name=F('market_request__society__name'),soc_id=F('market_request__society_id')
    ).annotate(
        total=Sum('value')
    )

    success_url=reverse_lazy('payment:payment_list')
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data()
        context['total']=Bale.objects.filter(is_mannual=False,value__isnull=False,price__isnull=False).aggregate(totav=Sum('value'))
        context['header']='SOCIETY PAYMENT BALANCES'
        return context

class SingleSocietyPaymentDetail(LoginRequiredMixin,ListView):
    login_url = "/login"
    redirect_field_name = 'next'
    model=Association
    template_name='payment/society_detail.html'
    context_object_name='lists'


    success_url=reverse_lazy('payment:payment_list')
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data()
        context['listout'] = Bale.objects.filter(is_mannual=False, value__isnull=False, price__isnull=False,market_request__society_id=self.kwargs['pk']).values(
            market=F('market_request__market__market_name'), saleno=F('market_request__sales_number')
        ).annotate(
            total=Sum('value')
        ).order_by("saleno")
        context['payments']=Payment.objects.filter(is_canceled=False).order_by('dated')
        context['total']=Bale.objects.filter(is_mannual=False,value__isnull=False,price__isnull=False,market_request__society_id=self.kwargs['pk']).aggregate(totav=Sum('value'))
        context['header']=Association.objects.get(id=self.kwargs['pk']).name
        return context


class DeletePayment(LoginRequiredMixin,DeleteView,SuccessMessageMixin):
    """DELETE PAYMENTS"""
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = Payment
    success_message = "Success!  deleted successfully."
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
            messages.success(request,'Success!,Deleted')
        except ProtectedError:
            messages.warning(request,'Faile!,You cannot delete this it is related to others')
            return redirect('payment:payment_list')

    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
    def get_success_url(self):
        return reverse('payment:payment_list')




