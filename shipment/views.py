from django.shortcuts import render,HttpResponse
from django.forms.models import model_to_dict
from auths.auth_token import Auth
from auths.models import Staff
from shipment.models import (
    MarketProcessingShipment,
    MarketProcessingShipmentBale,
    MarketWarehouseShipment,
    MarketWarehouseShipmentBale,
    WarehouseProcessingShipment,
    WarehouseProcessingShipmentBale,
    WarehouseShipment,
    WarehouseShipmentBale,
    GeneralShipment,
    GeneralShipmentBale
)
from market import models, schemas
from market.models import Bale
from core.models import CropGrade, CropType, Region, GradePrice
from ninja.errors import HttpError
from django.db.models import Q,Sum


# Create your views here.


class Shipment:
    def __init__(self):
        pass

    def load_market_to_warehouse_shipment_bales(request):
        user_data = Auth.get_user_by_token(request)
        shipment = MarketWarehouseShipment.objects.filter(
            Q(personnel=Staff.objects.get(user__id=user_data.id))
            | Q(personnel_receiver=Staff.objects.get(user__id=user_data.id))
        )
        if not shipment:
            raise HttpError(400, "Staff not assigned in any Transportation (Shipment)")

        bales = MarketWarehouseShipmentBale.objects.filter(shipment=shipment[0])
        bales_list = []
        for bale in bales:
            bale_object = model_to_dict(bale)
            bale_object.pop("delivery_status")
            bale_object.pop("shipment")
            bale_object.pop("is_active")
            bale_object.pop("created_by")
            bale_object.pop("bale")
            bale_object["primary_weight"] = bale.bale.primary_weight
            bale_object["ticket_number"] = bale.bale.ticket.ticket_number
            bale_object["id"] = bale.id
            bales_list.append(bale_object)

        shipment = shipment[0]
        return_object = {
            "shipment_number": shipment.shipment_number,
            "market": shipment.market.market_name,
            "warehouse": shipment.warehouse.warehouse_name,
            "sales_number": shipment.market_request.sales_number,
            "market_request": shipment.market_request.ticket_request_name,
            "shipment_bales": bales_list,
        }

        return return_object

    def update_market_to_warehouse_shipment_bales(bales_list):
        bale_numbers = 0
        updated_bales = []
        for bale in bales_list:
            try:
                if type(bale) != "dict":
                    bale = dict(bale)
                bale_id = bale["id"]

                bale_to_update = MarketWarehouseShipmentBale.objects.filter(
                    id=bale["id"]
                )
                bale.pop("id")
                bale_to_update.update(**bale)
                shpbale = MarketWarehouseShipmentBale.objects.filter(
                    id=bale["id"]
                ).first()
                if shpbale.received_weight:
                    Bale.objects.filter(id=bale_id).update(current_grade=shpbale.bale.grade,current_weight=shpbale.received_weight,warehouse=shpbale.shipment.warehouse)

                    
                bale_numbers += 1
                bale["id"] = bale_id
                updated_bales.append(bale)
            except:
                continue
        updated_object = {"updated_bales": bale_numbers, "bales": updated_bales}
        return updated_object

    def load_market_to_processing_shipment_bales(request):
        user_data = Auth.get_user_by_token(request)
        shipment = MarketProcessingShipment.objects.filter(
            Q(personnel=Staff.objects.get(user__id=user_data.id))
            | Q(personnel_receiver=Staff.objects.get(user__id=user_data.id))
        )
        if not shipment:
            raise HttpError(400, "Staff not assigned in any Transportation (Shipment)")

        bales = MarketProcessingShipmentBale.objects.filter(shipment=shipment[0])
        bales_list = []
        for bale in bales:
            bale_object = model_to_dict(bale)
            bale_object.pop("delivery_status")
            bale_object.pop("shipment")
            bale_object.pop("is_active")
            bale_object.pop("created_by")
            bale_object.pop("bale")
            bale_object["primary_weight"] = bale.bale.primary_weight
            bale_object["ticket_number"] = bale.bale.ticket.ticket_number
            bale_object["id"] = bale.id
            bales_list.append(bale_object)

        shipment = shipment[0]
        return_object = {
            "shipment_number": shipment.shipment_number,
            "market": shipment.market.market_name,
            "processing_centre": shipment.processing_centre.centre_name,
            "sales_number": shipment.market_request.sales_number,
            "market_request": shipment.market_request.ticket_request_name,
            "shipment_bales": bales_list,
        }

        return return_object

    def update_market_to_processing_shipment_bales(bales_list):
        bale_numbers = 0
        updated_bales = []
        for bale in bales_list:
            try:
                if type(bale) != "dict":
                    bale = dict(bale)
                bale_id = bale["id"]
                bale_to_update = MarketProcessingShipmentBale.objects.filter(
                    id=bale["id"]
                )
                bale.pop("id")
                bale_to_update.update(**bale)
                bale_numbers += 1
                bale["id"] = bale_id
                updated_bales.append(bale)
            except:
                continue
        updated_object = {"updated_bales": bale_numbers, "bales": updated_bales}
        return updated_object

    def load_warehouse_to_warehouse_shipment_bales(request):
        user_data = Auth.get_user_by_token(request)
        shipment = WarehouseShipment.objects.filter(
            Q(personnel=Staff.objects.get(user__id=user_data.id))
            | Q(personnel_receiver=Staff.objects.get(user__id=user_data.id))
        )
        if not shipment:
            raise HttpError(400, "Staff not assigned in any Transportation (Shipment)")

        bales = WarehouseShipmentBale.objects.filter(shipment=shipment[0])
        bales_list = []
        for bale in bales:
            bale_object = model_to_dict(bale)
            bale_object.pop("delivery_status")
            bale_object.pop("shipment")
            bale_object.pop("is_active")
            bale_object.pop("created_by")
            bale_object.pop("bale")
            bale_object["primary_weight"] = bale.bale.primary_weight
            bale_object["ticket_number"] = bale.bale.ticket.ticket_number
            bale_object["id"] = bale.id
            bales_list.append(bale_object)

        shipment = shipment[0]
        return_object = {
            "shipment_number": shipment.shipment_number,
            "from_warehouse": shipment.from_warehouse.warehouse_name,
            "to_warehouse": shipment.to_warehouse.warehouse_name,
            "shipment_bales": bales_list,
        }

        return return_object

    def update_warehouse_to_warehouse_shipment_bales(bales_list):
        bale_numbers = 0
        updated_bales = []
        for bale in bales_list:
            try:
                if type(bale) != "dict":
                    bale = dict(bale)
                bale_id = bale["id"]
                bale_to_update = WarehouseShipmentBale.objects.filter(id=bale["id"])
                bale.pop("id")
                bale_to_update.update(**bale)
                bale_numbers += 1
                bale["id"] = bale_id
                updated_bales.append(bale)
            except:
                continue
        updated_object = {"updated_bales": bale_numbers, "bales": updated_bales}
        return updated_object

    def load_warehouse_to_processing_shipment_bales(request):
        user_data = Auth.get_user_by_token(request)
        shipment = WarehouseProcessingShipment.objects.filter(
            Q(personnel=Staff.objects.get(user__id=user_data.id))
            | Q(personnel_receiver=Staff.objects.get(user__id=user_data.id))
        )
        if not shipment:
            raise HttpError(400, "Staff not assigned in any Transportation (Shipment)")

        bales = WarehouseProcessingShipmentBale.objects.filter(shipment=shipment[0])
        bales_list = []
        for bale in bales:
            bale_object = model_to_dict(bale)
            bale_object.pop("delivery_status")
            bale_object.pop("shipment")
            bale_object.pop("is_active")
            bale_object.pop("created_by")
            bale_object.pop("bale")
            bale_object["primary_weight"] = bale.bale.primary_weight
            bale_object["ticket_number"] = bale.bale.ticket.ticket_number
            bale_object["id"] = bale.id
            bales_list.append(bale_object)
        # getting single Shipment
        shipment = shipment[0]
        return_object = {
            "shipment_number": shipment.shipment_number,
            "warehouse": shipment.warehouse.warehouse_name,
            "processing_centre": shipment.processing_centre.centre_name,
            "shipment_bales": bales_list,
        }

        return return_object

    def update_warehouse_to_processing_shipment_bales(bales_list):
        bale_numbers = 0
        updated_bales = []
        for bale in bales_list:
            try:
                if type(bale) != "dict":
                    bale = dict(bale)
                bale_id = bale["id"]
                bale_to_update = WarehouseProcessingShipmentBale.objects.filter(
                    id=bale["id"]
                )
                bale.pop("id")
                bale_to_update.update(**bale)
                bale_numbers += 1
                bale["id"] = bale_id
                updated_bales.append(bale)
            except:
                continue
        updated_object = {"updated_bales": bale_numbers, "bales": updated_bales}
        return updated_object

    def end_loading(request, db_shipment_table, bale_table):
        user_data = Auth.get_user_by_token(request)
        staff = Staff.objects.filter(user_id=user_data.id)
        if staff:
            shipment = db_shipment_table.objects.filter(
                Q(personnel=staff[0]) | Q(personnel_receiver=staff[0]), on_loading=True
            )
            if shipment:
                if None in [
                    bale.transport_weight
                    for bale in bale_table.objects.filter(shipment_id=shipment[0].id)
                ]:
                    raise HttpError(
                        400,
                        "Loading Session can not be Ended because there are missing Bale Transport weight",
                    )
                shipment.update(on_loading=False)
                return "Loading Session has ended Successful"
            return "Staff has no active Trasportation duty"
        raise HttpError(404, "Staff not Found")

    def end_receiving(request, db_shipment_table, bale_table):
        user_data = Auth.get_user_by_token(request)
        staff = Staff.objects.filter(user_id=user_data.id)
        if staff:
            shipment = db_shipment_table.objects.filter(
                Q(personnel=staff[0]) | Q(personnel_receiver=staff[0]),
                on_receiving=True,
            )
            if shipment:
                if None in [
                    bale.receiving_weight
                    for bale in bale_table.objects.filter(shipment_id=shipment[0].id)
                ]:
                    raise HttpError(
                        400,
                        "Receiving Session can not be Ended because there are missing Bale Receiving weight",
                    )
                shipment.update(on_receiving=False)
                return "Receiving Session has ended Successful"
            return "Staff has no active Trasportation duty"
        raise HttpError(404, "Staff not Found")

    def end_market_warehouse_loading(request):
        return Shipment.end_loading(
            request, MarketWarehouseShipment, MarketWarehouseShipmentBale
        )

    def end_market_warehouse_receiving(request):
        return Shipment.end_receiving(
            request, MarketWarehouseShipment, MarketWarehouseShipmentBale
        )

    def end_market_processing_loading(request):
        return Shipment.end_loading(
            request, MarketProcessingShipment, MarketProcessingShipmentBale
        )

    def end_market_processing_receiving(request):
        return Shipment.end_receiving(
            request, MarketProcessingShipment, MarketProcessingShipmentBale
        )

    def end_warehouse_warehouse_loading(request):
        return Shipment.end_loading(request, WarehouseShipment, WarehouseShipmentBale)

    def end_warehouse_warehouse_receiving(request):
        return Shipment.end_receiving(request, WarehouseShipment, WarehouseShipmentBale)

    def end_warehouse_processing_loading(request):
        return Shipment.end_loading(
            request, WarehouseProcessingShipment, WarehouseProcessingShipmentBale
        )

    def end_warehouse_processing_receiving(request):
        return Shipment.end_receiving(
            request, WarehouseProcessingShipment, WarehouseProcessingShipmentBale
        )

    def load_custom_shipment(request):
        user_data = Auth.get_user_by_token(request)
        shipment = GeneralShipment.objects.filter(
            Q(receiver=Staff.objects.get(user__id=user_data.id))
            | Q(transporter=Staff.objects.get(user__id=user_data.id))
        )
        #return HttpResponse(shipment[0].receiver.user.username)
        if not shipment:
            raise HttpError(400, "Staff not assigned in any Transportation (Shipment)")

        bales = GeneralShipmentBale.objects.filter(general_shipment=shipment[0])
        type1 = 'transporter'
        if shipment[0].receiver.user_id == user_data.id:
            type1='receiver'




        shipment = shipment[0]
        return_object = {
            "shipment_id": str(shipment.id),
            'shipment_type':type1,
            "from_warehouse": shipment.from_warehouse.warehouse_name,
            "to_warehouse": shipment.to_warehouse.warehouse_name,
            "total_tickets": bales.count(),
            "total_receiving_weight":0.00 if bales.aggregate(RWT=Sum('receiving_weight'))["RWT"] is None else bales.aggregate(RWT=Sum('receiving_weight'))["RWT"],
            "total_transport_weight": 0.00 if bales.aggregate(RWT=Sum('transport_weight'))["RWT"] is None else bales.aggregate(RWT=Sum('transport_weight'))["RWT"],
        }

        return return_object

    def get_ticket_for_shipment(request, ticket_number):
        """get bale by ticket for shipment"""
        """get the role and shipment"""
        user_data = Auth.get_user_by_token(request)
        shipment = GeneralShipment.objects.filter(
            Q(receiver=Staff.objects.get(user__id=user_data.id))
            | Q(transporter=Staff.objects.get(user__id=user_data.id))
        )
        if not shipment:
            raise HttpError(400, "Staff not assigned in any Transportation (Shipment)")
        ticket_number=str(ticket_number)
        ticket = models.Ticket.objects.filter(ticket_number=ticket_number).first()
        bale=None
        if ticket:
            bale = models.Bale.objects.filter(ticket_id=ticket.id)

        bales = GeneralShipmentBale.objects.filter(general_shipment=shipment[0])
        #return HttpResponse(ticket)

        type1 = 'transporter'
        if shipment[0].receiver.user_id == user_data.id:
            type1 = 'receiver'
        if bale:
            bale = bale[0]
            bale_object = model_to_dict(bale)
            shipbale = GeneralShipmentBale.objects.filter(bale_id=bale.id).first()
            if shipbale:

                bale_object["ticket_number"] = shipbale.bale.ticket.ticket_number
                bale_object["bale_id"] = shipbale.bale_id
                bale_object["shipment_id"] = shipment[0].id
                bale_object["shipment_type"] = type1

                bale_object["grade"] = "" if shipbale.shipment_grade is None else shipbale.shipment_grade_id
                bale_object["in_house_grade"] = "" if shipbale.bale.in_house_grade_id is None else shipbale.bale.in_house_grade_id
                bale_object["receiving_weight"] = 0.0 if shipbale.receiving_weight is None else shipbale.receiving_weight
                bale_object["current_weight"]=0.0 if bale.current_weight is None else bale.current_weight
                bale_object["transport_weight"] = 0.0 if shipbale.transport_weight is None else shipbale.transport_weight
                bale_object["primary_weight"] = 0.0 if shipbale.bale.primary_weight is None else shipbale.bale.primary_weight

                if shipbale.bale.in_house_grade:
                    if shipbale.bale.in_house_grade.is_special:
                        bale_object["in_house_grade"]=None
                else:
                    bale_object["in_house_grade"]=None

                if shipbale.bale.verified_grade:
                    if shipbale.bale.verified_grade.grade_name == 'C' or shipbale.bale.verified_grade.grade_name == 'R' or shipbale.bale.verified_grade.grade_name == 'W':
                        bale_object["in_house_grade"]=None
                else:
                    bale_object["in_house_grade"]=None

            else:
                bale_object["ticket_number"] = bale.ticket.ticket_number
                bale_object["bale_id"] = bale.id
                bale_object["shipment_id"] = shipment[0].id
                bale_object["shipment_type"] = type1
                bale_object["grade"] = "" if bale.grade is None else bale.grade_id

                if bale.in_house_grade:
                    bale_object["in_house_grade"] =  bale.in_house_grade_id
                    if bale.in_house_grade.is_special:
                        bale_object["in_house_grade"]=None
                else:
                    bale_object["in_house_grade"]=None

                if bale.verified_grade:
                    if bale.verified_grade.grade_name == 'C' or bale.verified_grade.grade_name == 'R' or bale.verified_grade.grade_name == 'W':
                        bale_object["in_house_grade"]=None



                bale_object["primary_weight"] = 0.0 if bale.primary_weight is None else bale.primary_weight
                bale_object["current_weight"] = 0.0 if bale.current_weight is None else bale.current_weight
                bale_object["transport_weight"] = 0.0
                bale_object["receiving_weight"] = 0.0



            print("bale_object", bale_object)
            return bale_object
        else:
            raise HttpError(404, "Bale not found")

    def add_update_bale_for_shipment(request,add_update_ship_bale_schema):
        """Update bale by ticket for shipment"""


        add_update_ship_bale_schema = add_update_ship_bale_schema.dict()
        print((add_update_ship_bale_schema))
        #try:
        shipment = GeneralShipment.objects.filter(id=add_update_ship_bale_schema["shipment_id"]).first()
        #return HttpResponse(add_update_ship_bale_schema["in_house_grade"])

        if shipment:
            """Check shipment bales"""

            if GeneralShipmentBale.objects.filter(bale_id=add_update_ship_bale_schema["bale_id"]).exists():
                if 'transporter' in add_update_ship_bale_schema["shipment_type"] :
                    #return HttpResponse(GeneralShipmentBale.objects.filter(bale_id=add_update_ship_bale_schema["bale_id"]).first().in_house_grade)

                    GeneralShipmentBale.objects.filter(bale_id=add_update_ship_bale_schema["bale_id"]).update(
                        transport_weight=add_update_ship_bale_schema["transport_weight"],

                        shipment_grade_id=add_update_ship_bale_schema["grade"],
                        in_house_grade_id=add_update_ship_bale_schema["in_house_grade"],
                        general_shipment_id=add_update_ship_bale_schema["shipment_id"]
                    )
                elif  'receiver' in add_update_ship_bale_schema["shipment_type"]:
                    GeneralShipmentBale.objects.filter(bale_id=add_update_ship_bale_schema["bale_id"]).update(
                        receiving_weight=add_update_ship_bale_schema["receiving_weight"],
                        shipment_grade_id=add_update_ship_bale_schema["grade"],
                        in_house_grade_id=add_update_ship_bale_schema["in_house_grade"],
                        general_shipment_id=add_update_ship_bale_schema["shipment_id"]
                    )
                databale=GeneralShipmentBale.objects.filter(bale_id=add_update_ship_bale_schema["bale_id"]).first()

            else:

                if models.Bale.objects.filter(id=add_update_ship_bale_schema["bale_id"]).exists():

                    if 'transporter' in add_update_ship_bale_schema["shipment_type"]:
                        #return HttpResponse(add_update_ship_bale_schema["shipment_type"])
                        databale=GeneralShipmentBale.objects.create(
                            transport_weight=add_update_ship_bale_schema["transport_weight"],
                            bale_id=add_update_ship_bale_schema["bale_id"],
                            shipment_grade_id=add_update_ship_bale_schema["grade"],
                            in_house_grade_id=add_update_ship_bale_schema["in_house_grade"],
                            general_shipment_id=add_update_ship_bale_schema["shipment_id"]
                        )
                    if 'receiver' in add_update_ship_bale_schema["shipment_type"]:
                        databale=GeneralShipmentBale.objects.create(
                            receiving_weight=add_update_ship_bale_schema["receiving_weight"],
                            bale_id=add_update_ship_bale_schema["bale_id"],
                            in_house_grade_id=add_update_ship_bale_schema["in_house_grade"],
                            shipment_grade_id=add_update_ship_bale_schema["grade"],
                            general_shipment_id=add_update_ship_bale_schema["shipment_id"]
                        )
                
            if databale:
                """
                if databale.transport_weight:
                    priceob=GradePrice.objects.filter(grade_id=add_update_ship_bale_schema["grade"],season_id=databale.bale.market_request.season_id)
                    if priceob:
                        val=round(priceob.price*databale.transport_weight,2)
                        Bale.objects.filter(id=bale_id).update(shipmentvalue=val)
                """

                #return HttpResponse('WEKIWEZA')
                bale_object = {}
                bale_object["ticket_number"] = databale.bale.ticket.ticket_number
                bale_object["bale_id"] = databale.bale_id

                bale_object["shipment_id"] = add_update_ship_bale_schema["shipment_id"]
                bale_object["shipment_type"] = add_update_ship_bale_schema["shipment_type"]
                bale_object["in_house_grade"] = "" if databale.in_house_grade is None else databale.in_house_grade_id
                bale_object["grade"] = "" if databale.shipment_grade is None else databale.shipment_grade.id
                bale_object["primary_weight"] = 0.0 if databale.bale.primary_weight is None else databale.bale.primary_weight
                bale_object["current_weight"] = 0.0 if databale.bale.current_weight is None else databale.bale.current_weight
                bale_object["receiving_weight"] = 0.0 if databale.receiving_weight is None else databale.receiving_weight
                bale_object["transport_weight"] = 0.0 if databale.transport_weight is None else databale.transport_weight


                print("bale_object", bale_object)
                return bale_object
        else:
            return 'You do not have a shipment'
        #except :
        #    return 'Internal Server Error'



