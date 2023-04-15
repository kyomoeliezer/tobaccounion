from django.db import models
from core.models import BaseDB,CropGrade,InHouseGrade
from model_utils import Choices
from market.models import Bale, Market

# Create your models here.

SHIPMENT_STATUS_CHOICES = Choices(
    ("NOT_STARTED", "Not Started"),
    ("PENDING", "Pending"),
    ("LOADING", "Loading"),
    ("ON_SHIPPING", "On Shipping"),
    ("DELIVERED", "Delivered"),
)

DELIVERY_STATUS_CHOICES = Choices(("NORMAL", "Normal"), ("DESTUCTED", "DESTRUCTED"))

class SendingShipmentEmail(BaseDB):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)


    def __str__(self):
        return self.email


class TransportCompany(BaseDB):
    name = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.name+' '+self.address

class Track(BaseDB):
    track_name = models.CharField(max_length=50, null=True, blank=True)
    reg_number = models.CharField(max_length=50, null=True, blank=True)
    document_number = models.CharField(max_length=50, null=True, blank=True)
    company = models.ForeignKey(TransportCompany, on_delete=models.DO_NOTHING, null=True)


    class Meta:
        verbose_name = "Track"
        verbose_name_plural = "Tracks"
        db_table = "track"

    def __str__(self):
        return self.company.name+'('+self.reg_number+')'


class Driver(models.Model):
    full_name = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    license = models.CharField(max_length=500, null=True, blank=True)
    nida = models.CharField(max_length=40, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    company=models.ForeignKey(TransportCompany,on_delete=models.DO_NOTHING,null=True)
    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"
        db_table = "driver"

    def __str__(self):
        return self.full_name+'('+self.license+')'


class BaseShipment(BaseDB):
    shipment_number = models.CharField(max_length=50, null=True, blank=True)
    track = models.ForeignKey(
        "shipment.Track", on_delete=models.CASCADE, null=True, blank=True
    )
    driver = models.ForeignKey(
        "shipment.Driver", on_delete=models.CASCADE, null=True, blank=True
    )
    on_loading = models.BooleanField(default=True)
    on_receiving = models.BooleanField(default=True)
    shipment_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    delivery_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    shipmet_status = models.CharField(
        choices=SHIPMENT_STATUS_CHOICES, max_length=40, null=True, blank=True
    )

    class Meta:
        abstract = True


class BaseShipmentBale(BaseDB):
    transport_weight = models.FloatField(blank=True, null=True)
    received_weight = models.FloatField(blank=True, null=True)
    delivery_status = models.CharField(
        null=True,
        blank=True,
        choices=DELIVERY_STATUS_CHOICES,
        default="",
        max_length=40,
    )

    class Meta:
        abstract = True


class WarehouseShipment(BaseShipment):
    from_warehouse = models.ForeignKey(
        "inventory.Warehouse", related_name="warehouse_bale", on_delete=models.CASCADE
    )
    to_warehouse = models.ForeignKey("inventory.Warehouse", on_delete=models.CASCADE)

    personnel = models.ForeignKey(
        "auths.Staff",
        on_delete=models.CASCADE,
        related_name="transpoter",
        null=True,
        blank=True,
    )
    personnel_receiver = models.ForeignKey(
        "auths.Staff",
        on_delete=models.CASCADE,
        related_name="receiver",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "WareHouse Shipment"
        verbose_name_plural = "Warehouse Shipments"
        db_table = "warehouse_shipment"

    def __str__(self):
        return self.shipment_number


class WarehouseShipmentBale(BaseShipmentBale):
    bale = models.ForeignKey(
        "market.Bale", verbose_name="warehouse_bale", on_delete=models.CASCADE
    )
    shipment = models.ForeignKey(
        "WarehouseShipment", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "WarehouseShipmentBale"
        verbose_name_plural = "WarehouseShipmentBales"
        db_table = "warehouse_shipment_bale"

    def __str__(self):
        return self.bale.ticket.ticket_number


class MarketProcessingShipment(BaseShipment):
    """ "Shipment from market to processing Centres"""

    market = models.ForeignKey("market.Market", on_delete=models.CASCADE)
    market_request = models.ForeignKey(
        "market.MarketTicketRequest", null=True, blank=True, on_delete=models.CASCADE
    )
    processing_centre = models.ForeignKey(
        "processing.ProcessingCentre", on_delete=models.CASCADE
    )
    personnel = models.ForeignKey(
        "auths.Staff",
        on_delete=models.CASCADE,
        related_name="processing_transpoter",
        null=True,
        blank=True,
    )
    personnel_receiver = models.ForeignKey(
        "auths.Staff",
        on_delete=models.CASCADE,
        related_name="processing_receiver",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "processing Shipment"
        verbose_name_plural = "Processing Shipments"
        db_table = "market_processing_shipment"

    def __str__(self):
        return self.shipment_number


class MarketProcessingShipmentBale(BaseShipmentBale):
    bale = models.ForeignKey(
        "market.Bale", verbose_name="warehouse_bale", on_delete=models.CASCADE
    )
    shipment = models.ForeignKey(
        "MarketProcessingShipment", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Market Processing Shipment bale"
        verbose_name_plural = "Market Processing Shipment bales"
        db_table = "market_processing_shipment_bale"

    def __str__(self):
        return self.bale.ticket.ticket_number


class WarehouseProcessingShipment(BaseShipment):
    """ "Shipment from warehouse to processing Centres"""

    warehouse = models.ForeignKey("inventory.Warehouse", on_delete=models.CASCADE)
    processing_centre = models.ForeignKey(
        "processing.ProcessingCentre", on_delete=models.CASCADE
    )

    personnel = models.ForeignKey(
        "auths.Staff",
        on_delete=models.CASCADE,
        related_name="warehouse_processing_transpoter",
        null=True,
        blank=True,
    )
    personnel_receiver = models.ForeignKey(
        "auths.Staff",
        on_delete=models.CASCADE,
        related_name="warehouse_receiver",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "processing Shipment"
        verbose_name_plural = "Processing Shipments"
        db_table = "warehouse_processing_shipment"

    def __str__(self):
        return self.shipment_number


class WarehouseProcessingShipmentBale(BaseShipmentBale):
    shipment = models.ForeignKey(
        "WarehouseProcessingShipment", on_delete=models.CASCADE
    )
    bale = models.ForeignKey("market.Bale", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "WarehoseProcessingShipmentBale"
        verbose_name_plural = "WarehoseProcessingShipmentBales"
        db_table = "warehouse_processing_shipment_bale"

    def __str__(self):
        return self.bale.ticket.ticket_number


class MarketWarehouseShipment(BaseShipment):
    """ "Shipment from markets to warehouses"""

    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True,)
    warehouse = models.ForeignKey("inventory.Warehouse", on_delete=models.CASCADE, null=True,)
    market_request = models.ForeignKey(
        "market.MarketTicketRequest", null=True, blank=True, on_delete=models.CASCADE
    )
    personnel = models.ForeignKey(
        "auths.Staff",
        on_delete=models.CASCADE,
        related_name="market_warehousetranspoter",
        null=True,
        blank=True,
    )
    personnel_receiver = models.ForeignKey(
        "auths.Staff",
        on_delete=models.CASCADE,
        related_name="market_warehouse_receiver",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Market Shipment"
        verbose_name_plural = "Market Shipments"
        db_table = "market_warehouse_shipment"

    def __str__(self):
        return self.shipment_number


class MarketWarehouseShipmentBale(BaseShipmentBale):
    bale = models.ForeignKey("market.Bale", on_delete=models.CASCADE)
    shipment = models.ForeignKey(
        "MarketWarehouseShipment", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "MarketWarehouseShipmentBale"
        verbose_name_plural = "MarketWarehouseShipmentBales"
        db_table = "market_warehouse_shipment_bale"

    def __str__(self):
        return self.bale.ticket.ticket_number


class SalesShipment(BaseShipment):
    """ "Shipment from Processing Centre to sales places"""

    processing_centre = models.ForeignKey(
        "processing.ProcessingCentre", on_delete=models.CASCADE
    )
    sales_location = models.CharField(max_length=500, null=True, blank=True)

    personnel = models.ForeignKey(
        "auths.Staff",
        on_delete=models.CASCADE,
        related_name="on_sales",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Sales Shipment"
        verbose_name_plural = "Sales Shipments"
        db_table = "sales_shipment"

    def __str__(self):
        return self.shipment_number


class SalesShipmentBale(BaseDB):
    product_bale = models.ForeignKey(
        "processing.ProductBale",
        verbose_name="processing_bale",
        on_delete=models.CASCADE,
    )
    sales_shipment = models.ForeignKey(
        "SalesShipment", null=True, blank=True, on_delete=models.CASCADE
    )
    shipment_bale_weight = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "SalesShipmentBale"
        verbose_name_plural = "SalesShipmentBales"
        db_table = "sales_shipment_bale"

    def __str__(self):
        return self.Product_bale.bale_number

class GeneralShipment(BaseShipment):
    """Shipment any to any, but uses internet"""
    from_warehouse=models.ForeignKey("inventory.Warehouse", on_delete=models.CASCADE,related_name="general_from",null=True)
    to_warehouse = models.ForeignKey("inventory.Warehouse", on_delete=models.CASCADE,related_name="general_to",null=True)
    transporter = models.ForeignKey( "auths.Staff",on_delete=models.CASCADE,related_name="general_transpoter",null=True,blank=True,)
    receiver = models.ForeignKey("auths.Staff",on_delete=models.CASCADE,related_name="general_receiver",null=True,blank=True,)
    shipmentno=models.IntegerField(null=True,blank=True)
    is_closed_transporting = models.BooleanField(null=True,default=False,)
    is_closed_receiving = models.BooleanField(null=True,default=False)
    is_sent_email=models.BooleanField(default=False,null=True)

    class Meta:
        verbose_name = "General Shipment"
        verbose_name_plural = "General Shipments"


class  GeneralShipmentBale(BaseDB):
    bale=models.ForeignKey(Bale,on_delete=models.CASCADE)
    general_shipment = models.ForeignKey(GeneralShipment,on_delete=models.CASCADE)
    transport_weight = models.FloatField(blank=True, null=True)
    receiving_weight = models.FloatField(blank=True, null=True)
    shipment_grade = models.ForeignKey(CropGrade,on_delete=models.CASCADE,blank=True, null=True)
    in_house_grade = models.ForeignKey(InHouseGrade,on_delete=models.CASCADE,blank=True, null=True)
    #testfield = models.FloatField(blank=True, null=True)
    class Meta:
        verbose_name = "GeneralShipmentBale"
        verbose_name_plural = "GeneralShipmentBales"
        db_table = "general_shipment_bale"

    def __str__(self):
        return self.transport_weight


class  GeneralShipmentReceivedBales(BaseDB):
    dispatch_date=models.DateField(null=True,blank=True)
    bale=models.ForeignKey(Bale,on_delete=models.CASCADE,null=True)
    baleno = models.CharField(null=True, verbose_name='Bale no',max_length=300)
    general_shipment = models.ForeignKey(GeneralShipment,on_delete=models.CASCADE,null=True)
    general_shipmentno = models.CharField(null=True, verbose_name='general_shipment no',max_length=300)
    receiving_weight = models.FloatField(blank=True, null=True)
    shipment_grade = models.ForeignKey(CropGrade,on_delete=models.CASCADE,blank=True, null=True)
    in_house_grade = models.ForeignKey(InHouseGrade,on_delete=models.CASCADE,blank=True, null=True)
    in_house_gradeno = models.CharField(null=True, verbose_name='in_house_grade name',max_length=300)
    is_received=models.BooleanField(default=False)
    receiving_grade = models.CharField(blank=True, null=True,max_length=20)
    truckno=models.CharField(blank=True, null=True,max_length=200)
    status=models.CharField(blank=True, null=True,max_length=200)

    #testfield = models.FloatField(blank=True, null=True)
    class Meta:
        verbose_name = "GeneralShipmentReceivedBales"
        verbose_name_plural = "GeneralShipmentReceivedBales"
        db_table = "general_shipment_received_bales"

    def __str__(self):
        if self.receiving_weight:
            return str(self.receiving_weight)
        else:
            return self.general_shipment.shipment_number+' '+self.bale.ticket.ticket_number
