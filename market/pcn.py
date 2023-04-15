from market.models import Pcn
from market.models import Bale
from django.db.models import Q, Max


def pcn_no(no):
    if int(no) < 10:
        return "000" + str(no)
    elif int(no) < 100:
        return "00" + str(no)
    elif int(no) < 1000:
        return "0" + str(no)
    elif int(no) < 10000:
        return "" + str(no)
    else:
        return str(no)


def create_pcn(requestOB):
    """function to create ONE PCN only, and returns pcn object"""
    pcnlast = 0
    x = 0
    no_tickets = int(requestOB.number_of_tickets)
    maxdata = Pcn.objects.aggregate(mno=Max("no"))  ##PATA   CN KUBWA AU LAST PCN
    if maxdata["mno"]:
        mno = maxdata["mno"]
        pcn_last_no = Pcn.objects.filter(no=mno).aggregate(mno=Max("no"))
        pcnlast = pcn_last_no["mno"]
    else:
        pcnlast = 0  ##KAMA HAIPO ITAKUWA ZERO

    patial_pcn_tickets_no = no_tickets % 25  ###pata remainder
    complete_pcn = no_tickets - patial_pcn_tickets_no  ##full pcn tickets

    ##//Tengeneza full pcn bales na pcn zake
    list = []
    while x < (complete_pcn / 25):
        """Kwa kila pcn  iliyo full"""
        pcn = Pcn.objects.create(
            no=int(int(pcnlast) + 1),
            pcn_no=pcn_no(int(pcnlast) + 1),
            request_id=requestOB.id,
            is_data_verified=True
        )
        pcn_id = pcn.id
        pcnlast = pcn.no
        b = 0
        ##########GET 25 TICKETS
        bales = Bale.objects.filter(
            market_request=requestOB, pcn_id__isnull=True
        ).order_by("created_on")[
            :25
        ]  # get
        for bl in bales:
            """Update Bales"""
            Bale.objects.filter(ticket_id=bl.ticket_id).update(pcn_id=pcn_id)
        x = x + 1

    if patial_pcn_tickets_no > 0:
        pcn = Pcn.objects.create(
            no=int(int(pcnlast) + 1),
            pcn_no=pcn_no(int(pcnlast) + 1),
            request_id=requestOB.id,
            is_data_verified=True
        )
        pcn_id = pcn.id
        pcnlast = pcn.no
        b = 0
        ##########GET 25 TICKETS
        bales = Bale.objects.filter(
            market_request=requestOB, pcn_id__isnull=True
        ).order_by("created_on")[
            :patial_pcn_tickets_no
        ]  # get
        for bl in bales:
            """Update Bales"""
            Bale.objects.filter(ticket_id=bl.ticket_id).update(pcn_id=pcn_id)
    message = "Created PCN and assigned to bales to PCN"
    return message


def create_pcn_for_additional(requestOB):
    """function to create ONE PCN only, and returns pcn object"""
    pcnlast = 0
    x = 0
    countt = Bale.objects.filter(
            market_request=requestOB, pcn_id__isnull=True
        ).count()
    no_tickets = int(countt)
    maxdata = Pcn.objects.aggregate(mno=Max("no"))  ##PATA   CN KUBWA AU LAST PCN
    if maxdata["mno"]:
        mno = maxdata["mno"]
        pcn_last_no = Pcn.objects.filter(no=mno).aggregate(mno=Max("no"))
        pcnlast = pcn_last_no["mno"]
    else:
        pcnlast = 0  ##KAMA HAIPO ITAKUWA ZERO

    patial_pcn_tickets_no = no_tickets % 25  ###pata remainder
    complete_pcn = no_tickets - patial_pcn_tickets_no  ##full pcn tickets

    ##//Tengeneza full pcn bales na pcn zake
    list = []
    while x < (complete_pcn / 25):
        """Kwa kila pcn  iliyo full"""
        pcn = Pcn.objects.create(
            no=int(int(pcnlast) + 1),
            pcn_no=pcn_no(int(pcnlast) + 1),
            request_id=requestOB.id,
            is_data_verified=True
        )
        pcn_id = pcn.id
        pcnlast = pcn.no
        b = 0
        ##########GET 25 TICKETS
        bales = Bale.objects.filter(
            market_request=requestOB, pcn_id__isnull=True
        ).order_by("created_on")[
            :25
        ]  # get
        for bl in bales:
            """Update Bales"""
            Bale.objects.filter(ticket_id=bl.ticket_id).update(pcn_id=pcn_id)
        x = x + 1

    if patial_pcn_tickets_no > 0:
        pcn = Pcn.objects.create(
            no=int(int(pcnlast) + 1),
            pcn_no=pcn_no(int(pcnlast) + 1),
            request_id=requestOB.id,
            is_data_verified=True
        )
        pcn_id = pcn.id
        pcnlast = pcn.no
        b = 0
        ##########GET 25 TICKETS
        bales = Bale.objects.filter(
            market_request=requestOB, pcn_id__isnull=True
        ).order_by("created_on")[
            :patial_pcn_tickets_no
        ]  # get
        for bl in bales:
            """Update Bales"""
            Bale.objects.filter(ticket_id=bl.ticket_id).update(pcn_id=pcn_id)
    message = "Created PCN and assigned to bales to PCN"
    return message