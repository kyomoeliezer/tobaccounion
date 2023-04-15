from urllib import response
from auths.auth_token import GlobalAuth
from ninja import Router
from .views import *
from market import schemas
from typing import List

# API router
api = Router(auth=GlobalAuth())


# @api.post("/create-ticket", response=schemas.TicketSchema)
# def add_ticket(request):
#     return Ticket.create_ticket(request)


@api.get("/get-tickects", response=List[schemas.TicketSchema])
def get_tickets(request):
    return Ticket.get_tickets(request)


@api.delete("/delete-tickect")
def delete_ticket(request, id: str):
    return Ticket.delete_ticket(request, id)


@api.delete("/delete-tickects")
def delete_tickets(request):
    return Ticket.delete_tickets(request)


@api.post("/add-bale", response=schemas.BaleSchema)
def add_bale(request, bale: schemas.CreateBaleSchema):
    return Bale.add_bale(request, bale)


@api.patch("/edit-bale")
def edit_bale(request, bale: schemas.EditBaleSchema):
    return Bale.edit_bale(request, bale)


@api.patch("/edit-bales")
def edit_bales(request, bales: List[schemas.EditBaleSchema]):
    return Bale.edit_bales(request, bales)


@api.get("/get-buyers", response=List[schemas.BuyerSchema])
def get_buyers(request):
    return Market.get_buyers(request)

@api.get("/get-verifiers", response=List[schemas.VerifierSchema])
def get_verifiers(request):
    return Market.get_verifiers(request)


@api.get("/get-bales", response=List[schemas.BaleSchema])
def get_bales(request):
    return Bale.get_bales(request)


@api.get("/get-bale-by-ticket", response=schemas.GetBaleSchema)
def get_bale_by_ticket(request, ticket_number: str):
    return Bale.get_bale_by_ticket(request, ticket_number)

@api.patch("/single-bale-update-status")
def update_bale_status_(request, edit_bale_schema:schemas.GetBaleSchema):
    return Bale.update_bale_status(request, edit_bale_schema)

@api.patch("/mannual-save-ticket-or-update")
def save_ticket_or_update(request, edit_bale_schema:schemas.SaveBaleSchema):
    return Bale.save_ticket_or_update(request, edit_bale_schema)




@api.get("/load-market-data", response=schemas.MarketDataSchema)
def load_market_bales(request):
    return Bale.load_market_data(request)


@api.patch("/end-pre-buying")
def end_pre_buying(request):
    return PrintRequest.end_pre_buying(request)


@api.patch("/end-buying")
def end_buying(request):
    return PrintRequest.end_buying(request)


@api.delete("/delete-bale")
def delete_bale(request, id: str):
    return Bale.delete_bale(request, id)


@api.post("/add-market", response=schemas.MarketSchema)
def add_market(request, market: schemas.CreateMarketSchema):
    return Market.create_market(request, market)


@api.get("/get-markets", response=List[schemas.MarketSchema])
def get_markets(request):
    return Market.get_markets(request)


class PrintRequestApi:
    def __init__(self):
        pass

    api = Router(auth=GlobalAuth())

    @api.post("/create-print-request", response=schemas.PrintRequestSchema)
    def add_print_request(request, print_request: schemas.CreatePrintRequestSchema):
        return PrintRequest.create_print_request(request, print_request)

    @api.get("/get-print-request", response=List[schemas.PrintRequestSchema])
    def get_print_requests(request):
        return PrintRequest.get_print_requests(request)

    @api.get(
        "/get-print-request-tickets", response=List[schemas.PrintRequestTicketSchema]
    )
    def get_print_request_tickets(request, print_request_id):
        return PrintRequest.get_print_request_tickets(request, print_request_id)

    @api.delete("delete-print-request")
    def delete_print_request(request, id: str):
        return PrintRequest.delete_print_request(request, id)

    @api.post("/generate-request-tickets")
    def generate_request_tickets(request, id: str):
        return PrintRequest.genarate_request_tickets(request, id)
