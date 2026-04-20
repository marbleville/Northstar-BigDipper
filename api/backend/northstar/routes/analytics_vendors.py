from backend.northstar.blueprint import vendor_bp
from backend.northstar.endpoints import analytics_vendors as endpoint
from backend.northstar.route_utils import handle_request


@vendor_bp.route("/analytics/vendors", methods=["GET"])
def get_analytics_vendors_route():
    return handle_request(
        endpoint="/analytics/vendors",
        method="GET",
        handler=endpoint.get_analytics_vendors,
    )
