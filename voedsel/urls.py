from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .api import api
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("", include("core.urls")),
    path("", include("auths.urls")),
    path("", include("association.urls")),
    path("market/", include("market.urls", namespace="market")),
    path("inventory/", include("inventory.urls", namespace="inventory")),
    path("processing/", include("processing.urls", namespace="processing")),
    path("shipment/", include("shipment.urls", namespace="shipment")),
    path("report/", include("report.urls", namespace="report")),
    path("payment/", include("payment.urls", namespace="payment")),
    # path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
