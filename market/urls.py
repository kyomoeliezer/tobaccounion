from unicodedata import name
from django.urls import path, re_path
from . import views
from . import web
from . import web as market_web

app_name = "market"
urlpatterns = [
    path("chekcorrect",views.check_tickets,name='refresh_available'),
    
    path("available_lists",views.available_lists,name='available_lists'),
    path("market-list/", market_web.Market.get_markets, name="market-list"),
    path("inactive-market-list/", market_web.Market.get_inactivemarkets, name="inactive-market-list"),

    path("verifyall", market_web.Market.old_pcn_verify),
    path("mannual-verify", market_web.UpdateSaveMannualTicketView.as_view(),name='mannual_verify'),
    path("mannual-bales", market_web.LatestBales.as_view(),name='m_bales'),
    
    
    path("print_request_change", market_web.Market.print_request_change),
    
    #path("old_problem_128522", market_web.Market.old_problem_128522),
    
    path("changeb4grading", market_web.Market.change_something_old,name='changeb4grading'),
    
     re_path(r"^sync-shipments-for-analysis/(?P<shipment_id>[\w-]+)/$",
        web.Market.sync_shipments_for_analysis,
        name="sync-shipments-for-analysis",
    ),
    path("verifiedvalue", market_web.Market.calculate_verified_value,name='verifiedvalue'),
    
    re_path(r"^unlink-tickets-from-pcn/(?P<pcn_id>[\w-]+)$",
        web.PCN.unlink_tickets_from_pcn,
        name="unlink_tickets_from_pcn",
    ),
    re_path(r"^refresh-pcn-and-tickets/(?P<request_id>[\w-]+)/$",
        web.PCN.refresh_pcn_and_tickets,
        name="refresh_pcn_and_tickets",
    ),
    path("unlink-tickets-from-pcn", market_web.PCN.unlink_tickets_from_pcn),
    
    
    re_path(
        r"^edit-market/(?P<market_id>[\w-]+)/$",
        web.Market.edit_market,
        name="edit-market",
    ),
    re_path(
        r"^delete-market/(?P<market_id>[\w-]+)/$",
        web.Market.delete_market,
        name="delete-market",
    ),
    path("add-market/", market_web.Market.add_market, name="add-market"),
    path("add-buyer/", market_web.Buyer.add_buyer, name="add-buyer"),
    re_path(
        r"^edit-buyer/(?P<buyer_id>[\w-]+)/$",
        web.Buyer.edit_buyer,
        name="edit-buyer",
    ),
    re_path(
        r"^delete-buyer/(?P<buyer_id>[\w-]+)/$",
        web.Buyer.delete_buyer,
        name="delete-buyer",
    ),

    ##VERIFIER
    path("add-verifier/", market_web.Verifier.add_verifier, name="add-verifier"),
    path("get_buyers-verifier/", market_web.Verifier.get_verifiers, name="verifiers"),
     re_path(
        r"^edit-verifier/(?P<verifier_id>[\w-]+)/$",
        web.Verifier.edit_verifier,
        name="edit-verifier",
    ),
     re_path(
        r"^delete-verifier/(?P<verifier_id>[\w-]+)/$",
        web.Verifier.delete_verifier,
        name="delete-verifier",
    ),
    re_path(
        r"^request-details/(?P<request_id>[\w-]+)/$",
        web.Market.get_bales_by_request_id,
        name="request-details",
    ),
    re_path(
        r"^request-details-tickets/(?P<request_id>[\w-]+)/$",
        web.Market.market_ticket_list,
        name="request-detail-tickets",
    ),
    re_path(
        r"^refresh_prices_on_2023/(?P<request_id>[\w-]+)/$",
        web.Verifier.refresh_prices_on_2023,
        name="refresh_prices_on_2023",
    ),
    
    path("buyers", market_web.Buyer.get_buyers, name="buyers"),
    path(
        "add-print-request/",
        market_web.Market.add_print_request_v02,
        name="add-print-request",
    ),
    path(
        "add-print-requestold/",
        market_web.Market.add_print_request,
        name="add-print-requestold",
    ),

    
    path(
        "add-market-ticket-request/",
        market_web.Market.add_market_ticket_request,
        name="add-market-ticket-request",
    ),
    re_path(
        r"^ticket/(?P<request_id>[\w-]+)/release-ticket-from-request/",
        market_web.Market.release_ticket_from_request,
        name="release-ticket-from-request",
    ),
    re_path(
        r"^ticket/(?P<request_id>[\w-]+)/aditional-ticket-from-request/",
        market_web.Market.aditional_ticket_from_request,
        name="aditional-ticket-from-request",
    ),
    
    path(
        "market-ticket-requests/",
        market_web.Market.get_market_ticket_requests,
        name="market-ticket-requests",
    ),
    path(
        "done-market-ticket-requests/",
        market_web.Market.get_market_ticket_requests_completed,
        name="market-ticket-requests-done",
    ),
    
    path(
        "print-requests/", market_web.Market.get_print_requests, name="print-requests"
    ),
    path(
        "add-market-personnel",
        market_web.Market.assign_personnel,
        name="add-market-personnel",
    ),
    path(
        "market-personnels",
        market_web.Market.market_assignments,
        name="market-personnels",
    ),
    path(
        "available-tickets/",
        market_web.Market.get_available_tickets,
        name="available-tickets",
    ),
     path(
        "test-email/",
        market_web.Market.test_email
    ),

    
    path(
        "change_to_used/",
        market_web.Market.change_to_used,
        name="change_to_used",
    ),

    path(
        "used-tickets/",
        market_web.Market.get_used_tickets,
        name="used-tickets",
    ),
    re_path(
        r"^delete-print-request/(?P<print_request_id>[\w-]+)/$",
        views.PrintRequest.delete_print_request,
        name="delete-print-request",
    ),
    re_path(
        r"^close-request-buying/(?P<data_id>[\w-]+)/$",
        views.MarketRequest2.end_buying_admin,
        name="admin-close-request-buying",
    ),
    re_path(
        r"^open-request-buying/(?P<data_id>[\w-]+)/$",
        views.MarketRequest2.open_buying_admin,
        name="admin-open-request-buying",
    ),
    re_path(
        r"^edit-market-ticket-request/(?P<request_id>[\w-]+)/$",
        web.Market.edit_market_ticket_request,
        name="edit-market-ticket-request",
    ),
    re_path(
        r"^delete-market-ticket-request/(?P<market_ticket_request_id>[\w-]+)/$",
        web.Market.delete_market_ticket_request,
        name="delete-market-ticket-request",
    ),
    re_path(
        r"^pcn-detail/(?P<pcn_id>[\w-]+)/$",
        web.PCN.get_pcn_detail,
        name="pcn-detail",
    ),
    re_path(
        r"^pcn-update-detail/(?P<pcn_id>[\w-]+)/$",
        web.PCN.get_pcn_detail_for_update,
        name="pcn-detail-update",
    ),
    re_path(
        r"^singe-bale-update/(?P<request_id>[\w-]+)/$",
        web.PCN.single_bale_update,
        name="singe-bale-update",
    ),
    re_path(
        r"^pcn-get-grade-price/(?P<season_id>[\w-]+)/$",
        web.PCN.get_grade_price,
        name="single-grade-price",
    ),
    re_path(
        r"^pcn-verify/(?P<pcn_id>[\w-]+)/$",
        web.PCN.verify_pcn,
        name="verify-pcn",
    ),
    re_path(
        r"^deverify-pcn/(?P<pcn_id>[\w-]+)/$",
        web.PCN.deverify_pcn,
        name="deverify-pcn",
    ),
    re_path(
        r"^emptysingle-pcn/(?P<pcn_id>[\w-]+)/$",
        web.PCN.pcn_single_pdf,
        name="pdf-single-pcn",
    ),
    re_path(
        r"^pcn/all-pcn-pdf/(?P<request_id>[\w-]+)/$",
        web.PCN.pcn_all_pdf,
        name="pcn-all-pdf",
    ),
    ##BALE
    path(
        "get-bale-info/",
        market_web.BaleView.get_bale_info,
        name="get_bale_info",
    ),
    path(
        "excess-weight-bales/",
        market_web.BaleView.beyond_the_weight,
        name="beyond_the_weight",
    ),
    re_path(
        r"^edit-bale-now/(?P<bale_id>[\w-]+)/$",
        web.BaleView.edit_bale,
        name="edit_bale",
    ),
    re_path(
        r"^edit-marketShipment-bale/(?P<trans_id>[\w-]+)/$",
        web.BaleView.edit_marketShipment_bale,
        name="edit_marketShipment_bale",
    ),
    re_path(
        r"^edit-processShipment-bale/(?P<transb_id>[\w-]+)/$",
        web.BaleView.edit_GeneralShipment_bale,
        name="edit_GeneralShipment_bale",
    ),
   
    
    
    

]
