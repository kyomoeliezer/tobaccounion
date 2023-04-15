from django.shortcuts import render, redirect
from django.shortcuts import redirect, reverse, resolve_url, render, HttpResponse
from association.models import Association, Farmer
import auths
from django.contrib import messages
from auths.auth_token import Auth
from auths.models import Staff, User
from inventory.models import Warehouse
from market import models, schemas
from core.models import CropGrade, CropType, Region, GradePrice
from core.views import (
    delete_files_in_dir,
    generate_bar_code,
    generate_qr_code,
    render_to_pdf,
    rotate_bar_code,
)
from ninja.errors import HttpError
from django.http import HttpResponse
from django.forms.models import model_to_dict
from voedsel.celery import app
from django.db.models import Q
from market.pcn import create_pcn, create_pcn_for_additional
from datetime import datetime


# Create your views here.


class Ticket:
    def __init__(self):
        pass

    def create_ticket(user_id, print_request):
        # try:
        last_ticket = models.Ticket.objects.filter(is_active=True).order_by(
            "-created_on"
        )
        if last_ticket.count() == 0:
            last_ticket = 100001
            ticket_number = last_ticket
        else:
            ticket_number = int(last_ticket[0].ticket_number) + 1
        qr_code = generate_qr_code(str(ticket_number))
        bar_code = generate_bar_code(str(ticket_number))
        ticket = models.Ticket.objects.create(
            print_request=print_request,
            created_by=User.objects.get(id=user_id),
            ticket_number=str(ticket_number),
            no=int(ticket_number),
            qr_code=qr_code,
            bar_code=bar_code,
        )
        ticket.save()

        return ticket

    def create_ticket_v02(user_id, print_request, ticketno):

        # qr_code = generate_qr_code(str(ticket_number))
        # bar_code = generate_bar_code(str(ticket_number))
        ticket = models.Ticket.objects.create(
            print_request=print_request,
            created_by=User.objects.get(id=user_id),
            ticket_number=str(ticketno),
            no=int(ticketno),

        )
        ticket.save()

        return ticket

    # except:
    #     raise HttpError(500, "Internal Server Error")

    def get_tickets(request):
        try:
            tickets = models.Ticket.objects.filter(is_active=True)
            return tickets
        except:
            raise "Internal Server Error"

    def delete_ticket(request, id: str):
        try:
            ticket = models.Ticket.objects.filter(id=id)
            if ticket:
                ticket[0].delete()
                return "Ticket has been successful Deleted"
            return "Ticket Not found, may be was deleted"
        except:
            raise

    def delete_tickets(request):
        try:
            ticket = models.Ticket.objects.filter(is_active=True)
            if ticket:
                ticket.delete()
                return "All Tickets has been successful Deleted"
            return "Ticket Not found, may be was deleted"
        except:
            raise


class Market:
    def __init__(self):
        pass

    def create_market(request, create_market_schema):
        try:
            if type(create_market_schema) != "dict":
                create_market_schema = create_market_schema.dict()
            create_market_schema["region"] = Region.objects.get(
                id=create_market_schema["region"]
            )
            create_market_schema["association"] = Association.objects.get(
                id=create_market_schema["association"]
            )
            market = models.Market.objects.create(
                **create_market_schema, created_by=request.user
            )
            market.save()
            return market
        except:
            raise

    def get_markets(request):
        try:
            markets = models.Market.objects.all()
            return markets
        except:
            raise

    def get_buyers(request):
        buyers = models.Buyer.objects.filter(is_active=True).order_by("buyer_code")
        return buyers

    def get_verifiers(request):
        verifiers = models.GradeVerifier.objects.filter(is_active=True).order_by("code")
        return verifiers


class Bale:
    def __init__(self):
        pass

    def add_bale(request, create_bale_schema):
        try:
            if type(create_bale_schema) != "dict":
                create_bale_schema = create_bale_schema.dict()
            create_bale_schema["ticket"] = models.Ticket.objects.get(
                id=create_bale_schema["ticket"]
            )
            create_bale_schema["grade"] = CropGrade.objects.get(
                id=create_bale_schema["grade"]
            )
            create_bale_schema["crop_type"] = CropType.objects.get(
                id=create_bale_schema["crop_type"]
            )
            bale = models.Bale.objects.create(**create_bale_schema)
            bale.save()
            return bale
        except:
            raise HttpError(500, "Internal Server Error")

    def update_bale(edit_bale_schema):
        if type(edit_bale_schema) != "dict":
            edit_bale_schema = edit_bale_schema.dict()

        if edit_bale_schema["ticket"]:
            edit_bale_schema["ticket"] = models.Ticket.objects.get(
                id=edit_bale_schema["ticket"]
            )
        else:
            edit_bale_schema["ticket"] = None
        ###PRIMARY WEIGHT AND VALUES
        if edit_bale_schema["grade"] and edit_bale_schema["primary_weight"]:
            weight = edit_bale_schema["primary_weight"]
            if not weight or weight == "":
                weight = "0"
            priceobj=GradePrice.objects.filter(
                grade_id=edit_bale_schema["grade"]
            ).latest('created_on')
            """
            priceobj = GradePrice.objects.filter(
                grade_id=edit_bale_schema["grade"]
            ).first()
            """
            if priceobj:
                edit_bale_schema["price"] = priceobj.price
                edit_bale_schema["value"] = round(priceobj.price * float(weight), 2)
            else:
                edit_bale_schema["value"] = 0

        ###END VALUE UPDATE
        grade_str = edit_bale_schema["grade"]

        if edit_bale_schema["grade"]:
            edit_bale_schema["grade"] = CropGrade.objects.get(
                id=edit_bale_schema["grade"]
            )
        else:
            edit_bale_schema["grade"] = None

        if edit_bale_schema["farmer"]:
            edit_bale_schema["farmer"] = Farmer.objects.get(
                id=edit_bale_schema["farmer"]
            )
        else:
            edit_bale_schema["farmer"] = None

        if edit_bale_schema["status"]:
            status = ""
            if edit_bale_schema["status"] == "r":
                status = "R"
            if edit_bale_schema["status"] == "c":
                status = "C"
            if edit_bale_schema["status"] == "w":
                status = "W"
            if edit_bale_schema["status"] == "ok":
                status = "OK"
            edit_bale_schema["status"] = status
        else:
            edit_bale_schema["status"] = None

        if grade_str:
            if 'C' in grade_str:
                status = "C"
            elif 'W' in grade_str:
                status = "W"
            elif 'R' in grade_str:
                status = "R"
            else:
                status = 'OK'
        edit_bale_schema["status"] = status

        bale = models.Bale.objects.filter(id=edit_bale_schema["id"])
        edit_bale_schema.pop("id")
        bale.update(**edit_bale_schema)
        return bale

    def edit_bale(request, edit_bale_schema):
        try:
            update = Bale.update_bale(edit_bale_schema)
            if update:
                return "Bale successfull Updated"
            else:
                raise HttpError(400, "Input Error")

        except:
            raise HttpError(500, "Internal Server Error")

    def edit_bales(request, edit_bales_schema):
        bale_number = 0
        bales_data = []
        for bale in edit_bales_schema:
            try:
                bale_update = Bale.update_bale(bale)
                bale_number += 1
                bales_data.append(bale)
            except:
                continue

        bales_object = {"updated_bales": bale_number, "bales": bales_data}
        return bales_object

    def get_bales(request):
        try:
            bales = models.Bale.objects.filter(is_active=True)
            return bales
        except:
            raise HttpError(500, "Internal server Error")

    def get_bale_by_ticket(request, ticket_number):
        """get bale by ticket"""
        """CHECK ROLES"""
        user_data = Auth.get_user_by_token(request)
        staff = Staff.objects.filter(user_id=user_data.id)
        staff1 = staff.first()
        role = "viewer"
        if staff1:
            if staff1.role:
                if 'Supervisor' in staff1.role.role_name or 'Admin' in staff1.role.role_name:
                    role = 'editor'

        bale = models.Bale.objects.filter(ticket__ticket_number=ticket_number)
        if bale:
            bale = bale[0]
            bale_object = model_to_dict(bale)
            bale_object["role"] = role

            bale_object["ticket_number"] = bale.ticket.ticket_number
            bale_object["id"] = bale.id
            bale_object.pop("created_by")
            bale_object.pop("is_active")
            # bale_object.pop("in_house_grade")

            print("bale_object", bale_object)
            return bale_object
        else:
            raise HttpError(404, "Bale not found")

    def get_market_bales(request, market_id):
        """Get market bales from specific market by market_id"""
        try:
            tickets = models.MarketTiket.objects.filter(
                market_ticket_request__market_id=market_id
            )
            bales = models.Bale.objects.filter(
                ticket__id__in=[ticket.ticket_id for ticket in tickets]
            )
            if bales:
                return bales
            else:
                raise HttpError(404, "No bales Found in that Market")

        except:
            raise HttpError(500, "Internal Server Error")

    def load_market_data(request):
        """Load market bales"""
        user_data = Auth.get_user_by_token(request)
        personnel = Staff.objects.get(user_id=user_data.id)
        market_ticket_requests = models.MarketTicketRequest.objects.filter(
            Q(Q(on_pre_buying=True) | Q(on_buying=True)) & Q(
                personnel=personnel) & Q(print_request_status="Not Allocated"))

        if not market_ticket_requests:
            raise HttpError("404", "Staff member has no active Market Request")

        market_ticket_requests = market_ticket_requests[0]
        tickets = models.MarketTiket.objects.filter(
            Q(Q(market_ticket_request__on_pre_buying=True) | Q(market_ticket_request__on_buying=True)) & Q(
                market_ticket_request__personnel=personnel) & Q(
                market_ticket_request__personnel_id=market_ticket_requests.personnel_id)
            )
        bales_object_list = []
        bales = models.Bale.objects.filter(market_request_id=market_ticket_requests.id)
        for bale in bales:
            bale_object = model_to_dict(bale)
            bale_object["ticket_number"] = bale.ticket.ticket_number
            bale_object["id"] = bale.id
            bale_object.pop("created_by")
            bale_object.pop("is_active")

            bale_object.pop("market_request")
            bale_object.pop("current_grade")
            bale_object.pop("current_weight")
            bale_object.pop("verified_grade")
            bale_object.pop("warehouse")
            bale_object.pop("in_house_grade")
            bales_object_list.append(bale_object)

        market_details = {
            "name": market_ticket_requests.ticket_request_name,
            "sales_date": market_ticket_requests.sales_date,
            "sales_number": market_ticket_requests.sales_number,
            "market": market_ticket_requests.market.market_name,
            "primary_society": market_ticket_requests.society.name,
            "ticket_request_bales": bales_object_list,
        }
        return market_details

    def delete_bale(request, id: str):
        try:
            bale = models.Bale.objects.filter(id=id)
            if bale:
                bale[0].delete()
                return "Bale successful Deleted"
            return "Bale Not found, may be already deleted"
        except:
            raise HttpError(500, "Internal Server Error")

    def update_bale_status(request, edit_bale_schema):
        user_data = Auth.get_user_by_token(request)
        stff = Staff.objects.get(user_id=user_data.id)
        if type(edit_bale_schema) != "dict":
            edit_bale_schema = edit_bale_schema.dict()
        if edit_bale_schema["verifier"]:
            bale = models.Bale.objects.filter(id=edit_bale_schema['id']).update(
                current_grade_id=edit_bale_schema["current_grade"],
                current_weight=edit_bale_schema["current_weight"],
                warehouse_id=edit_bale_schema["warehouse"],
                verified_grade_id=edit_bale_schema["verified_grade"],
                in_house_grade_id=edit_bale_schema["in_house_grade"],
                verifier_id=edit_bale_schema["verifier"],
                verification_by_id=stff.id,
                verification_date=datetime.now()
            )

        if edit_bale_schema["verified_grade"]:
            bale = models.Bale.objects.filter(id=edit_bale_schema['id']).update(
                current_grade_id=edit_bale_schema["current_grade"],
                current_weight=edit_bale_schema["current_weight"],
                warehouse_id=edit_bale_schema["warehouse"],
                verified_grade_id=edit_bale_schema["verified_grade"],
                in_house_grade_id=edit_bale_schema["in_house_grade"],

                verification_by_id=stff.id,
                verification_date=datetime.now()
            )
            verified_by_id = stff.id
        else:
            bale = models.Bale.objects.filter(id=edit_bale_schema['id']).update(
                current_grade_id=edit_bale_schema["current_grade"],
                current_weight=edit_bale_schema["current_weight"],
                warehouse_id=edit_bale_schema["warehouse"],
                verified_grade_id=edit_bale_schema["verified_grade"],
                in_house_grade_id=edit_bale_schema["in_house_grade"],
                verifier_id=edit_bale_schema["verifier"],
            )
        bale = models.Bale.objects.filter(id=edit_bale_schema['id']).first()
        priceobj = GradePrice.objects.filter(
            grade_id=bale.verified_grade_id
        ).first()
        if priceobj:

            bale.verifiedvalue = round(priceobj.price * float(bale.primary_weight), 2)

        else:
            bale.verifiedvalue = 0
        bale.save()

        bale = models.Bale.objects.filter(id=edit_bale_schema['id'])
        if bale:
            bale = bale[0]
            bale_object = model_to_dict(bale)
            bale_object["role"] = 'viewer'
            bale_object["verified_grade"] = bale.verified_grade_id
            bale_object["verifier"] = bale.verifier_id
            bale_object["in_house_grade"] = bale.in_house_grade_id
            bale_object["ticket_number"] = bale.ticket.ticket_number
            bale_object["id"] = bale.id
            bale_object.pop("created_by")
            bale_object.pop("is_active")
            # bale_object.pop("in_house_grade")
            bale_object.pop("farmer")
            bale_object.pop("buyer_code")
            bale_object.pop("status")
            bale_object.pop("price")
            bale_object.pop("value")
            bale_object.pop("pcn")
            bale_object.pop("market_request")
            bale_object.pop("remarks")

            print("bale_object", bale_object)
            return bale_object

    def save_ticket_or_update(request, edit_bale_schema):
        reqob=models.MarketTicketRequest.objects.filter(is_mannual=True,created_on__gte='2023-03-07').latest('created_on')
        req_id=reqob.id#'b919a359-c24e-407d-8f10-cfffa358d91b'
        printreqOB=models.PrintRequest.objects.filter(is_mannual=True,created_on__gte='2023-03-07').latest('created_on')

        print_request_id=printreqOB.id

        user_data = Auth.get_user_by_token(request)
        stff = Staff.objects.get(user_id=user_data.id)
        if type(edit_bale_schema) != "dict":
            edit_bale_schema = edit_bale_schema.dict()
            ticket_number = edit_bale_schema['ticket_number']

        #####################################
        ##GRADE PRICES
        ##################################
        verivalue = value = 0
        if edit_bale_schema["grade"] and edit_bale_schema["primary_weight"]:
            weight = edit_bale_schema["primary_weight"]
            if not weight or weight == "":
                weight = "0"
            priceobj = GradePrice.objects.filter(
                grade_id=edit_bale_schema["grade"]
            ).first()
            if priceobj:
                price = priceobj.price
                value = round(priceobj.price * float(weight), 2)
            else:
                value = 0
        if edit_bale_schema["verified_grade"] and edit_bale_schema["current_weight"]:
            weight = edit_bale_schema["current_weight"]
            if not weight or weight == "":
                weight = "0"
            priceobj = GradePrice.objects.filter(
                grade_id=edit_bale_schema["verified_grade"]
            ).first()
            if priceobj:
                price = priceobj.price
                verivalue = round(priceobj.price * float(weight), 2)
            else:
                verivalue = 0

        ###END PRICES
        #####################################

        if models.Bale.objects.filter(market_request_id=req_id,
                                      ticket__ticket_number=edit_bale_schema['ticket_number']).exists():
            bale = models.Bale.objects.filter(market_request_id=req_id,
                                              ticket__ticket_number=edit_bale_schema['ticket_number']).update(
                current_grade_id=edit_bale_schema["verified_grade"],
                grade_id=edit_bale_schema["grade"],
                current_weight=edit_bale_schema["current_weight"],
                primary_weight=edit_bale_schema["primary_weight"],
                warehouse_id=edit_bale_schema["warehouse"],
                verified_grade_id=edit_bale_schema["verified_grade"],
                in_house_grade_id=edit_bale_schema["in_house_grade"],
                verifier_id=edit_bale_schema["verifier"],
                verifiedvalue=verivalue,
                value=value,
                is_mannual=True,
                buyer_code=edit_bale_schema["buyer_code"],
                verification_by_id=stff.id,
                verification_date=datetime.now()
            )
            bale = models.Bale.objects.filter(market_request_id=req_id,
                                              ticket__ticket_number=edit_bale_schema['ticket_number'])
            # return HttpResponse(edit_bale_schema['ticket_number'])

        else:
            if not models.Ticket.objects.filter(ticket_number=str(ticket_number)).exists():

                ticket = models.Ticket.objects.create(
                    print_request_id=print_request_id,
                    created_by=User.objects.get(id=user_data.id),
                    ticket_number=str(ticket_number),
                    no=int(ticket_number)
                )
                market_ticket = models.MarketTiket.objects.create(market_ticket_request_id=req_id, ticket_id=ticket.id)
                market_ticket.save()
                # creating bale
                bale = models.Bale.objects.create(
                    ticket_id=ticket.id,
                    market_request_id=req_id,
                    current_grade_id=edit_bale_schema["verified_grade"],
                    grade_id=edit_bale_schema["grade"],
                    current_weight=edit_bale_schema["current_weight"],
                    primary_weight=edit_bale_schema["primary_weight"],
                    warehouse_id=edit_bale_schema["warehouse"],
                    verified_grade_id=edit_bale_schema["verified_grade"],
                    in_house_grade_id=edit_bale_schema["in_house_grade"],
                    verifier_id=edit_bale_schema["verifier"],
                    buyer_code=edit_bale_schema["buyer_code"],
                    verifiedvalue=verivalue,
                    value=value,
                    is_mannual=True,
                    verification_by_id=stff.id,
                    verification_date=datetime.now()
                )
                if bale:
                    ticket.is_used = True
                    ticket.save()
                bale = models.Bale.objects.filter(market_request_id=req_id,
                                                  ticket__ticket_number=edit_bale_schema['ticket_number'])
            else:
                if not models.Bale.objects.filter(ticket__ticket_number=edit_bale_schema['ticket_number']).exists():

                    ticket = models.Ticket.objects.filter(ticket_number=str(ticket_number)).first()

                    market_ticket = models.MarketTiket.objects.update_or_create(market_ticket_request_id=req_id,
                                                                                ticket_id=ticket.id)

                    # creating bale
                    bale, created = models.Bale.objects.update_or_create(
                        ticket_id=ticket.id,
                        market_request_id=req_id,
                        current_grade_id=edit_bale_schema["verified_grade"],
                        grade_id=edit_bale_schema["grade"],
                        current_weight=edit_bale_schema["current_weight"],
                        primary_weight=edit_bale_schema["primary_weight"],
                        warehouse_id=edit_bale_schema["warehouse"],
                        verified_grade_id=edit_bale_schema["verified_grade"],
                        in_house_grade_id=edit_bale_schema["in_house_grade"],
                        verifier_id=edit_bale_schema["verifier"],
                        buyer_code=edit_bale_schema["buyer_code"],
                        verifiedvalue=verivalue,
                        value=value,
                        is_mannual=True,
                        verification_by_id=stff.id,
                        verification_date=datetime.now()
                    )
                    bale = models.Bale.objects.filter(market_request_id=req_id,
                                                      ticket__ticket_number=edit_bale_schema['ticket_number'])
                    if bale:
                        ticket.is_used = True
                else:
                    bale = None

        # bale=models.Bale.objects.filter(market_request_id=req_id, ticket__ticket_number=ticket_number)
        # return HttpResponse(bale)
        if bale:
            return {"ticket_number": str(ticket_number), "status": 200, "statusDesc": "Successfully saved"}
            # bale = bale[0]
            # bale_object = model_to_dict(bale)
            # bale_object["role"] = 'viewer'
            # bale_object["verified_grade"] = bale.verified_grade_id
            # bale_object["verifier"] = bale.verifier_id
            # bale_object["in_house_grade"] = bale.in_house_grade_id
            # bale_object["ticket_number"] = bale.ticket.ticket_number
            # bale_object["id"] = bale.id
            # bale_object.pop("created_by")
            # bale_object.pop("is_active")
            # # bale_object.pop("in_house_grade")
            # bale_object.pop("farmer")
            # bale_object.pop("buyer_code")
            # bale_object.pop("status")
            # bale_object.pop("price")
            # bale_object.pop("value")
            # bale_object.pop("pcn")
            # bale_object.pop("market_request")
            # bale_object.pop("remarks")

            # print("bale_object", bale_object)
            # return bale_object
        else:
            return {"ticket_number": str(ticket_number), "status": 201,
                    "statusDesc": "Failed , can't be updated or saved"}


class PrintRequest:
    def __init__(self):
        pass

    def create_print_request(request, print_request):
        try:
            if type(print_request) != "dict":
                print_request = print_request.dict()
                request = models.PrintRequest.objects.create(
                    **print_request, created_by=request.user
                )
            request.save()
            return request
        except:
            raise HttpError(500, "Internal server Error")

    def get_print_requests(request):
        try:
            print_requests = models.PrintRequest.objects.filter(is_active=True)
            return print_requests
        except:
            raise HttpError(500, "Internal Server Error")

    def delete_print_request_api_view(request, id: str):
        try:
            print_request = models.PrintRequest.objects.filter(id=id)
            if print_request:
                print_request_tickets = models.PrintRequestTicket.objects.filter(
                    print_request_id=print_request[0].id
                )
                tickets = models.Ticket.objects.filter(
                    id__in=[
                        print_request_ticket.ticket_id
                        for print_request_ticket in print_request_tickets
                    ]
                )
                tickets.delete()
                print_request_tickets.delete()
                print_request[0].delete()
                return "Print Request successful deleted"
            raise HttpError(404, "Print Request was not found")
        except:
            raise HttpError(500, "Internal Server Error")

    def delete_print_request(request, print_request_id):
        print_request = models.PrintRequest.objects.filter(id=print_request_id)
        if print_request:
            print_request_tickets = models.PrintRequestTicket.objects.filter(
                print_request_id=print_request[0].id
            )
            models.Ticket.objects.filter(print_request_id=print_request_id).delete()
            print_request_tickets.delete()
            print_request.delete()
            message = "Print Request and Associated Tickets has been Deleted"
            return redirect(request.META["HTTP_REFERER"], {"message": message})
        else:
            message = "No print request found, may be was already deleted"
            return redirect(request.META["HTTP_REFERER"], {"message": message})

    def get_print_request_tickets(request, print_request_id):
        print_request_tickets = models.PrintRequestTicket.objects.filter(
            print_request__id=print_request_id
        ).order_by("ticket__created_on")
        return print_request_tickets

    def create_market_ticket(request, market_ticket_request_id):
        # try:
        market_ticket_request = models.MarketTicketRequest.objects.get(
            id=market_ticket_request_id
        )
        number_of_tickets = market_ticket_request.number_of_tickets
        number_of_tickets = int(number_of_tickets)
        ticket_of = 0

        """
        """

        """
        """
        nulltickets = models.Ticket.objects.filter(no__isnull=True)
        for ti in nulltickets:
            ti.no = int(ti.ticket_number)
            ti.save()

        """ """
        lists = list(models.MarketTiket.objects.values_list('ticket_id', flat=True))
        tickets = models.Ticket.objects.filter(Q(print_request__is_mannual=False) & ~Q(id__in=lists) & Q(is_used=False)&Q(created_on__gte='2023-02-01')).order_by('no')[
                  :number_of_tickets]
        dbale = []
        dmarticket = []
        for ticket in tickets:
            ticket_of += 1
            dmarticket.append(models.MarketTiket(
                market_ticket_request_id=market_ticket_request.id, ticket_id=ticket.id
            ))

            dbale.append(models.Bale(
                ticket_id=ticket.id, market_request_id=market_ticket_request.id
            ))
            ticket.is_used = True
            ticket.save()

        models.Bale.objects.bulk_create(dbale)
        models.MarketTiket.objects.bulk_create(dmarticket)
        create_pcn_for_additional(market_ticket_request)

        message = f"All {number_of_tickets} Assigned Successfull"
        return redirect(reverse('market:market-ticket-requests'))
        """
        for ticket in models.PrintRequestTicket.objects.exclude(
            ticket__id__in=[
                ticket.ticket.id
                for ticket in models.MarketTiket.objects.filter(is_active=True)
            ]
        ).order_by("created_on"):



            ticket_of += 1
            market_ticket = models.MarketTiket.objects.create(
                market_ticket_request=market_ticket_request, ticket=ticket.ticket
            )
            market_ticket.save()
            # creating bale
            bale = models.Bale.objects.create(
                ticket=ticket.ticket, market_request=market_ticket_request
            )
            bale.save()

            if ticket_of == int(number_of_tickets):

                break
        create_pcn(market_ticket_request)
        message = f"All {number_of_tickets} Assigned Successfull"
        return message
        """

    # except:
    #     raise HttpError(500, "Internal Server Error")

    @app.task()
    def genarate_request_tickets_v02(user_id, print_request_id: str):

        print_request = models.PrintRequest.objects.get(id=print_request_id)
        total_number = countt = 0
        current_tk = print_request.initial_ticket
        list1 = []
        list2 = []
        while current_tk <= print_request.last_ticket:
            total_number += 1

            # ticket = Ticket.create_ticket_v02(user_id, print_request,current_tk)
            list1.append(
                models.Ticket(
                    print_request=print_request,
                    created_by=User.objects.get(id=user_id),
                    ticket_number=str(current_tk),
                    no=int(current_tk),
                    is_used=False

                )
            )
            current_tk += 1
            countt = countt + 1

            # print_request_ticket.save()
        # models.PrintRequestTicket.objects.bulk_create(list2)
        models.Ticket.objects.bulk_create(list1)
        tickets = models.Ticket.objects.filter(print_request=print_request).order_by('created_on')
        for tk in tickets:
            list2.append(
                models.PrintRequestTicket(
                    print_request=print_request,
                    ticket=tk,
                    created_by=User.objects.get(id=user_id),
                )
            )
        models.PrintRequestTicket.objects.bulk_create(list2)
        return f"All {total_number} tickets generated Successful"

    @app.task()
    def genarate_request_tickets(user_id, print_request_id: str):
        try:
            print_request = models.PrintRequest.objects.get(id=print_request_id)
            total_number = 0
            for number_of_ticket in range(print_request.number_of_tickets):
                total_number += 1
                ticket = Ticket.create_ticket(user_id, print_request)
                print_request_ticket = models.PrintRequestTicket.objects.create(
                    print_request=print_request,
                    ticket=ticket,
                    created_by=User.objects.get(id=user_id),
                )
                print_request_ticket.save()
                template_name = "pdfticket_live.html"
                rotate_bar_code(ticket)
            print_request_tickets = models.PrintRequestTicket.objects.filter(
                print_request=print_request
            ).order_by("ticket__created_on")
            pdf = render_to_pdf(
                template_name, {"tickets": print_request_tickets}, "file"
            )
            if pdf:

                models.PrintRequest.objects.filter(id=print_request_id).update(
                    ticket_file=pdf
                )
            else:
                return HttpResponse("Not found")

            bar_code_path = "static/assets/bar_code/"
            qr_code_path = "static/assets/qr_code/"
            delete_files_in_dir(bar_code_path)
            delete_files_in_dir(qr_code_path)
            return f"All {total_number} tickets generated Successful"

        except:
            raise HttpError(500, "Internal Server Error")

    def regenerate_ticket(request, print_request_id: str):
        try:
            print_request = models.PrintRequest.objects.get(id=print_request_id)
            print_request_tickets = models.PrintRequestTicket.objects.filter(
                print_request=print_request
            )
            total_number = 0
            for print_request_ticket in print_request_tickets:
                total_number += 1
                generate_qr_code(str(print_request_ticket.ticket.ticket_number))
                generate_bar_code(str(print_request_ticket.ticket.ticket_number))
                rotate_bar_code(print_request_ticket.ticket)
            template_name = "pdfticket_live.html"
            render_to_pdf(template_name, {"tickets": print_request_tickets}, "file")
            return f"All {total_number} tickets re-generated Successful"
        except:
            raise HttpError(500, "Internal Server Error")

    def end_pre_buying(request):
        user_data = Auth.get_user_by_token(request)
        staff = Staff.objects.filter(user_id=user_data.id)
        if staff:
            market_ticket_request = models.MarketTicketRequest.objects.filter(
                personnel=staff[0]
            )
            if market_ticket_request:
                if None in [
                    bale.primary_weight
                    for bale in models.Bale.objects.filter(
                        market_request_id=market_ticket_request[0].id
                    )
                ]:
                    raise HttpError(
                        400,
                        "Pre Buying can not be Ended because there are missing Bale Primary weight",
                    )
                market_ticket_request.update(on_pre_buying=False)
                return "Pre Buying Session has ended Successful"
            return "Staff has no Market Request"
        return "Staff not Found"

    def end_buying(request):
        user_data = Auth.get_user_by_token(request)
        staff = Staff.objects.filter(user_id=user_data.id)
        if staff:
            market_ticket_request = models.MarketTicketRequest.objects.filter(
                personnel=staff[0]
            )
            if market_ticket_request:
                if None in [
                    bale.grade
                    for bale in models.Bale.objects.filter(
                        market_request_id=market_ticket_request[0].id
                    )
                ]:
                    raise HttpError(
                        400,
                        "Buying Session can not be Ended because there are missing Bale Grades",
                    )
                market_ticket_request.update(on_buying=False)
                return "Buying Session has ended Successful"
            return "Staff has no Market Request"
        return "Staff not Found"


class MarketRequest2:
    def __init__(self):
        pass

    def end_buying_admin(request, data_id):
        market_ticket_request = models.MarketTicketRequest.objects.filter(
            id=data_id
        ).update(on_buying=False, on_pre_buying=False)
        models.Pcn.objects.update(is_data_verified=True)

        return redirect(reverse("market:market-ticket-requests"))

    def open_buying_admin(request, data_id):
        market_ticket_request = models.MarketTicketRequest.objects.filter(
            id=data_id
        ).update(on_buying=True, on_pre_buying=True)
        models.Pcn.objects.update(is_data_verified=True)

        return redirect(reverse("market:market-ticket-requests"))

####TICKET ZIMEZINGUA
def check_tickets(request):
    countT=countF=0
    tickets1=models.Ticket.objects.filter(no__gte=201901, no__lte=202000)
    for tk in tickets1:

        if not models.Bale.objects.filter(ticket_id=tk.id).exists():

            models.Bale.objects.filter(ticket_id=tk.id).delete()
            models.MarketTiket.objects.filter(ticket_id=tk.id).delete()
            models.PrintRequestTicket.objects.filter(ticket_id=tk.id).delete()
            tk.delete()


    tickets=models.Ticket.objects.filter(no__gte=184762, no__lte=184851)

    for tk in tickets:
        if models.Bale.objects.filter(ticket_id=tk.id).exists():
            countT +=1
            tk.is_used=True
            tk.save()

        else:
            models.MarketTiket.objects.filter(ticket_id=tk.id).delete()
            countF +=1
            tk.is_used=False
            tk.save()

    return redirect(reverse('market:available_lists'))


def available_lists(request):
    countT=countF=0
    tickets=models.Ticket.objects.filter(is_used=False).order_by('no')
    return render(request,'bale/available_lists.html',{'tickets':tickets})

