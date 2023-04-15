from email.policy import default
from django.db import models
from core.models import BaseDB
from model_utils import Choices
from django.core.validators import MaxLengthValidator,MinLengthValidator


# Create your models here.
USE_STATUS_CHOICES = Choices(("INITIAL_MARKET", "Initial Market"))

PRINTING_STATUS_CHOICES = Choices(
    ("PRINTED", "Printed"), ("NOT_PRINTED", "Not Printed")
)


class Buyer(BaseDB):
    full_name = models.CharField(max_length=50, null=True, blank=True)
    buyer_code = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Buyer"
        verbose_name_plural = "Buyers"
        db_table = "buyer"

    def __str__(self):
        return self.full_name +'('+ self.buyer_code+')'

class GradeVerifier(BaseDB):
    full_name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "GradeVerifier"
        verbose_name_plural = "GradeVerifiers"
        

    def __str__(self):
        return self.full_name+'['+self.code+']'


class Ticket(BaseDB):
    ticket_number = models.CharField(max_length=50, null=True, blank=True)
    qr_code = models.CharField(max_length=500, null=True, blank=True)
    bar_code = models.CharField(max_length=500, null=True, blank=True)
    rotated_bar_code = models.CharField(max_length=500, null=True, blank=True)
    is_printed = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False,null=True)
    print_request = models.ForeignKey(
        "market.PrintRequest", null=True, blank=True, on_delete=models.CASCADE
    )
    no = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="This is just a Ticket no but in interger format,used for ticket release",
    )
    Use_status = models.CharField(
        max_length=200,
        choices=USE_STATUS_CHOICES,
        default=USE_STATUS_CHOICES.INITIAL_MARKET,
    )

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        db_table = "ticket"

    def __str__(self):
        return self.ticket_number


class MarketTicketRequestPersonnel(BaseDB):
    personnel = models.ForeignKey("auths.Staff", on_delete=models.CASCADE)
    market_ticket_request = models.ForeignKey(
        "MarketTicketRequest", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Buyer Market"
        verbose_name_plural = "Buyer Markets"
        db_table = "market_ticket_request_personnel"

    def __str__(self):
        return f"{self.personnel__full_name} {self.market_ticket_request__ticket_request_name}"


class Market(BaseDB):
    market_name = models.CharField(max_length=500, null=True, blank=True)
    market_code = models.CharField(max_length=500, null=True, blank=True)
    region = models.ForeignKey(
        "core.Region", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Market"
        verbose_name_plural = "Markets"
        db_table = "market"

    def __str__(self):
        return self.market_name


class PrintRequest(BaseDB):
    request_name = models.CharField(max_length=500, null=True, blank=True)
    number_of_tickets = models.IntegerField(null=True, blank=True)
    ticket_file = models.CharField(max_length=500, null=True, blank=True)
    initial_ticket=models.IntegerField(null=True, blank=True,)
    last_ticket = models.IntegerField(null=True, blank=True)
    is_mannual=models.BooleanField(default=False)
    print_request_status = models.CharField(
        max_length=500,
        choices=PRINTING_STATUS_CHOICES,
        default=PRINTING_STATUS_CHOICES.NOT_PRINTED,
    )

    class Meta:
        verbose_name = "PrintRequest"
        verbose_name_plural = "PrintRequests"
        db_table = "print_request"

    def __str__(self):
        return self.request_name


class MarketTicketRequest(BaseDB):
    ticket_request_name = models.CharField(max_length=500, null=True, blank=True)
    market = models.ForeignKey(
        "Market", on_delete=models.CASCADE, null=True, blank=True
    )

    number_of_tickets = models.IntegerField(null=True, blank=True)
    sales_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    society = models.ForeignKey(
        "association.Association", on_delete=models.CASCADE, null=True, blank=True
    )
    season = models.ForeignKey(
        "core.Season", on_delete=models.CASCADE, null=True, blank=True
    )
    personnel = models.ForeignKey(
        "auths.Staff", on_delete=models.CASCADE, null=True, blank=True
    )
    print_request_status = models.CharField(
        max_length=500, choices=PRINTING_STATUS_CHOICES, default="Not Allocated"
    )
    on_pre_buying = models.BooleanField(default=True)
    on_buying = models.BooleanField(default=True)
    sales_number = models.IntegerField(null=True, blank=True)
    is_mannual=models.BooleanField(default=False)
    # transporter = models.CharField(null=True, blank=True,max_length=40,verbose_name="Transporter Just kwa ajili ya kuprint PCN,anatakiwa ajazwe automatically")
    mobile_clerk = models.CharField(
        null=True, blank=True, max_length=40, verbose_name="Mobile Clerk for PDF only "
    )

    class Meta:
        verbose_name = "MarketTicketRequest"
        verbose_name_plural = "MarketTicketRequests"
        db_table = "market_ticket_request"

    def __str__(self):
        return self.ticket_request_name


class MarketTiket(BaseDB):
    market_ticket_request = models.ForeignKey(
        "MarketTicketRequest", on_delete=models.CASCADE, null=True, blank=True
    )
    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "MarketTiket"
        verbose_name_plural = "MarketTikets"
        db_table = "market_ticket"

    def __str__(self):
        return self.ticket.ticket_number


class PrintRequestTicket(BaseDB):
    print_request = models.ForeignKey("PrintRequest", on_delete=models.CASCADE)
    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "PrintRequestTicket"
        verbose_name_plural = "PrintRequestTickets"
        db_table = "print_request_ticket"

    def __str__(self):
        return self.print_request.request_name


class Pcn(BaseDB):
    """Table for PCN to for grouping bales"""

    request = models.ForeignKey(MarketTicketRequest, on_delete=models.PROTECT)
    no = models.IntegerField()
    pcn_no = models.CharField(max_length=20, verbose_name="Pcn no")
    is_data_verified = models.BooleanField(
        verbose_name="The farmer have verified the data?,1-YES,0-Not yet", default=False
    )
    data_verification_by = models.ForeignKey(
        "auths.User", on_delete=models.PROTECT, null=True, related_name="Verified_by"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    nill = models.CharField(max_length=30, null=True)

    class Meta:
        verbose_name = "PCN"
        verbose_name_plural = "PCNs"
        db_table = "pcn"

    def __str__(self):
        return self.pcn_no


class Bale(BaseDB):
    ticket = models.ForeignKey(
        "Ticket", verbose_name="ticket", null=True, blank=True, on_delete=models.CASCADE
    )

    primary_weight = models.FloatField(null=True, blank=True)
    grade = models.ForeignKey(
        "core.CropGrade",
        related_name="crop_grade",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    market_request = models.ForeignKey(
        "market.MarketTicketRequest", null=True, blank=True, on_delete=models.CASCADE
    )
    pcn = models.ForeignKey(Pcn, on_delete=models.DO_NOTHING, null=True)
    in_house_grade = models.ForeignKey(
        "core.InHouseGrade", on_delete=models.CASCADE, null=True, blank=True
    )
    current_grade = models.ForeignKey(
        "core.CropGrade",
        related_name="current_grade",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    verified_grade = models.ForeignKey(
        "core.CropGrade",
        related_name="verified_grade",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    verifier=models.ForeignKey(GradeVerifier, on_delete=models.CASCADE, null=True, blank=True)
    
    current_weight = models.FloatField(null=True, blank=True)
    warehouse = models.ForeignKey(
        "inventory.Warehouse",
        verbose_name="warehouse",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    farmer = models.ForeignKey(
        "association.Farmer", on_delete=models.CASCADE, null=True, blank=True
    )
    buyer_code = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(null=True, max_length=50)
    remarks = models.CharField(
        null=True, max_length=50, verbose_name="Remarks / comments "
    )
    price = models.FloatField(verbose_name="Price", null=True)
    value = models.FloatField(verbose_name="Value", null=True)
    shipmentvalue= models.FloatField(verbose_name="shipmentvalue  Value, mzigo unatoka, transport weight mara grade price", null=True)
    verifiedvalue= models.FloatField(verbose_name="verified Value", null=True)
    verification_date=models.DateTimeField(null=True)
    verification_by=models.ForeignKey("auths.Staff",on_delete=models.DO_NOTHING,null=True,related_name="verify")
    is_mannual=models.BooleanField(default=False,null=True)
    mn_society=models.ForeignKey(
        "association.Association", on_delete=models.CASCADE, null=True, blank=True
    )
    mn_market=models.ForeignKey(
        "Market", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Bale"
        verbose_name_plural = "Bales"
        db_table = "bale"

    def __str__(self):
        return self.ticket.ticket_number
