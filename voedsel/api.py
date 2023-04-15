from ninja import NinjaAPI, Form

# from auths.auth_token import Authenticate
from ninja.security import HttpBearer
from auths.api import api as user_apis
from core.api import api as core_apis
from market.api import api as market_apis
from market.api import PrintRequestApi
from inventory.api import api as inventory_aois
from auths.authenticate import api as auth_apis
from association.api import api as society_apis
from auths.auth_token import Auth
from shipment.api import api as shipment_apis

api = NinjaAPI(
    title="CAPTURE API",
    docs_url="/docs",
)
api.add_router("auth", auth_apis, tags=["Authentication APIs"])
api.add_router("user", user_apis, tags=["User APIs"])
api.add_router("society", society_apis, tags=["Society APIs"])
api.add_router("print_request", PrintRequestApi.api, tags=["Print Request APIs"])
api.add_router("market", market_apis, tags=["Market Place APIs"])
api.add_router("shipment", shipment_apis, tags=["Shipment APIs"])
api.add_router("inventory", inventory_aois, tags=["Inventory APIs"])
api.add_router("core", core_apis, tags=["Core Module APIs"])
