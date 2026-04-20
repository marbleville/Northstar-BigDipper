from backend.northstar.blueprint import trip_bp
from backend.northstar.endpoints import analytics_destinations as endpoint
from backend.northstar.route_utils import handle_request


@trip_bp.route("/analytics/destinations", methods=["GET"])
def get_analytics_destinations_route():
    return handle_request(
        endpoint="/analytics/destinations",
        method="GET",
        handler=endpoint.get_analytics_destinations,
    )
