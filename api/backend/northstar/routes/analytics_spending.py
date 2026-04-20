from backend.northstar.blueprint import trip_bp
from backend.northstar.endpoints import analytics_spending as endpoint
from backend.northstar.route_utils import handle_request


@trip_bp.route("/analytics/spending", methods=["GET"])
def get_analytics_spending_route():
    return handle_request(
        endpoint="/analytics/spending",
        method="GET",
        handler=endpoint.get_analytics_spending,
    )
