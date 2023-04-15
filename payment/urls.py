from django.urls import path, re_path
from . import web

app_name = "payment"
urlpatterns = [
    path("", web.PaymentLists.as_view(), name="payment_list"),
    path("new", web.AddNewPaymentView.as_view(), name="new_payment"),
    path("balances", web.PaymentListsWithBalance.as_view(), name="payment_balance"),


    re_path(r"^(?P<pk>[\w-]+)/update$", web.UpdatePaymentView.as_view(), name="update_payment", ),
    re_path(r"^(?P<pk>[\w-]+)/delete", web.DeletePayment.as_view(), name="delete_payment", ),
    re_path(r"^(?P<pk>[\w-]+)/society", web.SingleSocietyPaymentDetail.as_view(), name="society_payment", ),


]
