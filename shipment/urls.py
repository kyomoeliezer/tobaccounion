from django.urls import path, re_path
from . import web

app_name = "shipment"
urlpatterns = [

    path("tcomapanies", web.ListTransportCompany.as_view(), name="tcompanies"),
    path("add-tcomapny", web.AddTransportCompany.as_view(), name="add_tcompany"),
    re_path(r"(?P<pk>[\w-]+)/Atcomapny", web.ActivateDeactivateCompany.as_view(), name="active_tcompanies"),

    re_path(r"(?P<pk>[\w-]+)/tcomapny", web.UpdateTransportCompany.as_view(), name="update_tcompanies"),
    path("drivers", web.Driver.get_drivers, name="drivers"),
    path("add-driver", web.Driver.add_driver, name="add-driver"),
    re_path(
        r"^edit-driver/(?P<driver_id>[\w-]+)/$",
        web.Driver.edit_driver,
        name="edit-driver",
    ),
    re_path(
        r"^delete-driver/(?P<driver_id>[\w-]+)/$",
        web.Driver.delete_driver,
        name="delete-driver",
    ),
    path("tracks", web.Track.get_tracks, name="tracks"),
    path("add-tracks", web.Track.add_track, name="add-track"),
    re_path(
        r"^edit-track/(?P<track_id>[\w-]+)/$",
        web.Track.edit_track,
        name="edit-track",
    ),
    re_path(
        r"^delete-track/(?P<track_id>[\w-]+)/$",
        web.Track.delete_track,
        name="delete-track",
    ),
    path(
        "add-warehouse-shipment",
        web.Shipment.add_warehouse_shipment,
        name="add-warehouse-shipment",
    ),
    path(
        "warehouse-shipments",
        web.Shipment.get_warehouse_shipments,
        name="warehouse-shipments",
    ),
    re_path(
        r"^edit-warehouse-shipment/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.edit_warehouse_shipment,
        name="delete-warehouse-shipment",
    ),
    re_path(
        r"^delete-warehouse-shipment/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.edit_warehouse_shipment,
        name="delete-warehouse-shipment",
    ),
    path(
        "add-warehouse-processing-shipment",
        web.Shipment.add_warehouse_processing_shipment,
        name="add-warehouse-processing-shipment",
    ),
    path(
        "warehouse-processing-shipments",
        web.Shipment.get_warehouse_processing_shipments,
        name="warehouse-processing-shipments",
    ),
    re_path(
        r"^delete-warehouse-processing-shipment/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.delete_warehouse_processing_shipment,
        name="delete-warehouse-processing-shipment",
    ),
    re_path(
        r"^edite-warehouse-processing-shipment/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.edit_warehouse_processing_shipment,
        name="edit-warehouse-processing-shipment",
    ),
    path(
        "add-market-warehouse-shipment",
        web.Shipment.add_market_warehouse_shipment,
        name="add-market-warehouse-shipment",
    ),
    path(
        "market-warehouse-shipments",
        web.Shipment.get_market_warehouse_shipments,
        name="market-warehouse-shipments",
    ),
    re_path(
        r"^edit-market-warehouse-shipment/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.edit_market_warehouse_shipment,
        name="edit-market-warehouse-shipment",
    ),

    ####SHIPMENT REFRESH
    re_path(
        r"^refmarket_warehouse_shipment_refresh/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.market_warehouse_shipment_refresh,
        name="market_warehouse_shipment_refresh",
    ),

    re_path(
        r"^delete-market-warehouse-shipment/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.delete_market_warehouse_shipment,
        name="delete-market-warehouse-shipment",
    ),
    path(
        "add-market-processing-shipment",
        web.Shipment.add_market_processing_shipment,
        name="add-market-processing-shipment",
    ),
    path(
        "market-processing-shipments",
        web.Shipment.get_market_processing_shipments,
        name="market-processing-shipments",
    ),
    re_path(
        r"^edit-market-processing-shipment/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.edit_market_processing_shipment,
        name="edit-market-processing-shipment",
    ),
    re_path(
        r"^delete-market-processing-shipment/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.delete_market_processing_shipment,
        name="delete-market-processing-shipment",
    ),
    path(
        "add-sales-shipment", web.Shipment.add_sales_shipment, name="add-sales-shipment"
    ),
    path("sales-shipments", web.Shipment.get_sales_shipments, name="sales-shipments"),
    re_path(
        r"^edit-sales-shipment/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.edit_sales_shipment,
        name="edit-sales-shipment",
    ),
    re_path(
        r"^delete-sales-shipment/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.delete_sales_shipment,
        name="delete-sales-shipment",
    ),
    re_path(
        r"^warehouse-details/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.get_warehouse_details,
        name="warehouse-details",
    ),
    re_path(
        r"^warehouse-pricessing-details/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.get_warehouse_processing_details,
        name="warehouse-processing-details",
    ),
    re_path(
        r"^market-warehouse-details/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.get_market_warehouse_details,
        name="market-warehouse-details",
    ),
    re_path(
        r"^market-processing-details/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.get_market_processing_details,
        name="market-processing-details",
    ),
    re_path(
        r"^sales-details/(?P<shipment_id>[\w-]+)/$",
        web.Shipment.get_sales_details,
        name="sales-details",
    ),
    re_path(r"^new-custom-shipment$",web.AddGeneralShipmentView.as_view(),name="new-custom-shipment",),
    
    
    re_path(r"^(?P<pk>[\w-]+)/update-custom-shipment$",web.UpdateGeneralShipmentView.as_view(),name="edit-custom-shipment",),
    re_path(r"^(?P<pk>[\w-]+)/delete-custom-shipment$",web.DeleteGeneralShipmentView.as_view(),name="delete-custom-shipment",),
    re_path(r"^(?P<pk>[\w-]+)/detail-custom-shipment$",web.DetailGeneralShipmentView.as_view(),name="detail-custom-shipment",),
    re_path(r"^(?P<pk>[\w-]+)/send-email$",web.FileSendEmailToProcessing.as_view(),name="send_shipment_email",),

    ####EMAIL RECEIVERS
    re_path(r"^(?P<pk>[\w-]+)/delemaireceiver$",web.DeleteEmailReceiversView.as_view(),name="delete-receiver",),
    re_path(r"^addemaireceiver$",web.AddEmailReceiverView.as_view(),name="add-receiver",),
    re_path(r"^emailfilereceivers$",web.ListEmailReceiversView.as_view(),name="list-email-receivers",),
    
    
    re_path(r"^(?P<pk>[\w-]+)/remove-bale-custom-shipment$",web.RemoveBaleonGeneralShipmentBaleView.as_view(),name="remove-bale-shipment",),
    
    re_path(r"^assignno$",web.ChangeGeneralShipmentNoView.as_view(),name="asignno",),

    re_path(r"^list-g-shipment$",web.ListGeneralShipmentView.as_view(),name="list-custom-shipment",),
    re_path(r"^done-list-g-shipment$",web.ListGeneralShipmentDoneView.as_view(),name="done-list-custom-shipment",),
    
    re_path(r"^(?P<pk>[\w-]+)/file-kiwandani$",web.FileForImporting.as_view(),name="file-kiwandani",),
    re_path(r"^(?P<pk>[\w-]+)/end-shipment$",web.EndShipments.as_view(),name="end_tshipment",),
    re_path(r"^(?P<pk>[\w-]+)/open-shipment$",web.OpenShipments.as_view(),name="open_tshipment",),
    
    re_path(r"^(?P<pk>[\w-]+)/delete-line$",web.DeleteshiingTicket.as_view(),name="delete_line",),
    re_path(r"^shipmentvalue$",web.RefreshshiingValue.as_view(),name="refresh_shipvalue",),
    #IMPORT NOW
    re_path(r"^sync-processing-receing-report",web.IMPORT.process_uploaded_file_now,name="sync-processing",),
    re_path(r"^large-csv-import",web.process_csv,name="large_csv",),

    
    



]
