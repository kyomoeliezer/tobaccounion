from dataclasses import fields
from sqlite3 import Date
from xml.etree.ElementInclude import include
from market.models import Bale, Buyer, Market, PrintRequest, PrintRequestTicket, Ticket,GradeVerifier
from ninja.orm import create_schema
from ninja import Schema
import uuid
from typing import List


MarketSchema = create_schema(Market)
CreateMarketSchema = create_schema(
    Market, exclude=["id", "created_on", "updated_on", "created_by"]
)

TicketSchema = create_schema(Ticket)
CreateTicketSchema = create_schema(
    Ticket,
    exclude=[
        "id",
        "qr_code",
        "bar_code",
        "ticket_number",
        "created_by",
        "created_on",
        "updated_on",
    ],
)

PrintRequestSchema = create_schema(PrintRequest)
CreatePrintRequestSchema = create_schema(
    PrintRequest, exclude=["id", "created_on", "updated_on", "created_by"]
)


BaleSchema = create_schema(Bale)
CreateBaleSchema = create_schema(Bale, exclude=["id", "created_on", "updated_on"])
PrintRequestTicketSchema = create_schema(PrintRequestTicket)

BuyerSchema = create_schema(Buyer)
VerifierSchema = create_schema(GradeVerifier)


class EditBaleSchema(Schema):
    id: uuid.UUID = "" or None
    ticket: uuid.UUID = "" or None
    farmer: uuid.UUID = "" or None
    primary_weight: float = 0.0 or None
    grade: str = "" or None
    buyer_code: str = "" or None
    status: str = "" or None


class SingleBaleSchema(Schema):
    id: uuid.UUID = "" or None
    ticket: uuid.UUID = "" or None
    farmer: uuid.UUID = "" or None
    primary_weight: float = 0.0 or None
    grade: uuid.UUID = "" or None
    buyer_code: str = "" or None


class GetBaleSchema(Schema):
    id: uuid.UUID = "" or None
    ticket: uuid.UUID = "" or None
    ticket_number: str = "" or None
    farmer: uuid.UUID = "" or None
    primary_weight: float = 0.0 or None
    grade: uuid.UUID = "" or None
    buyer_code: str = "" or None
    warehouse: uuid.UUID = "" or None
    current_grade: uuid.UUID = "" or None
    verifier: uuid.UUID = "" or None
    verified_grade: uuid.UUID = "" or None
    in_house_grade: uuid.UUID = "" or None
    current_weight: float = 0.0 or None
    role: str = "" or None

class SaveBaleSchema(Schema):
    
    ticket_number: str = "" or None
    primary_weight: float = 0.0 or None
    grade: uuid.UUID = "" or None
    buyer_code: str = "" or None
    warehouse: uuid.UUID = "" or None
    current_grade: uuid.UUID = "" or None
    verifier: uuid.UUID = "" or None
    verified_grade: uuid.UUID = "" or None
    in_house_grade: uuid.UUID = "" or None
    current_weight: float = 0.0 or None


class MarketDataSchema(Schema):
    market: object
    sales_date: Date
    sales_number: int = 0 or None
    primary_society: str
    ticket_request_bales: List


# EditBaleSchema = create_schema(
#     Bale, exclude=["created_by", "created_on", "updated_on", "is_active"]
# )
