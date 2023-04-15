from django.shortcuts import render, redirect
from .forms import *
from django.core.paginator import Paginator


class Processing:
    def __init__(self):
        pass

    def add_processing_centre(request):
        template_name = "processing/add_processing_centre.html"
        if request.method == "POST":
            form = ProcessingCentreForm(request.POST or None)
            if form.is_valid():
                if ProcessingCentre.objects.filter(
                    centre_name=form.cleaned_data["centre_name"]
                ).exists():
                    cenre_name = form.cleaned_data["centre_name"]
                    message = (
                        f" Processing Centre with name {cenre_name} Already exists"
                    )
                    return render(request, template_name, {"message": message})
                processing_centre = ProcessingCentre.objects.create(**form.cleaned_data)
                processing_centre.save()
                return redirect("/processing/processing-centres")
            message = "invalid form Data"
            return render(request, template_name, {"message": message})
        return render(request, template_name)

    def get_processing_centres(request):
        template_name = "processing/processing_centres.html"
        centres = ProcessingCentre.objects.filter(is_active=True).order_by(
            "centre_name"
        )
        paginated_centres = Paginator(centres, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_centres.get_page(page_number)
        return render(request, template_name, {"page_obj": page_obj})

    def delete_processing_centre(request, centre_id):
        centre = ProcessingCentre.objects.filter(id=centre_id)
        if not centre.exists():
            template_name = "processing/processing_centres.html"
            centres = ProcessingCentre.objects.filter(is_active=True).order_by(
                "centre_name"
            )
            paginated_centres = Paginator(centres, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_centres.get_page(page_number)
            message = "Processing centre was Already deleted"
            return render(
                request, template_name, {"page_obj": page_obj, "message": message}
            )
        centre.delete()
        return redirect("/processing/processing-centres")


class ProcessingReport:
    def __init__(self):
        pass
