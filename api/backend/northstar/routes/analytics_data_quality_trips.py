from backend.northstar.blueprint import trip_bp
from backend.northstar.endpoints import analytics_data_quality_trips as endpoint
from backend.northstar.route_utils import handle_request


@trip_bp.route("/analytics/data-quality/trips", methods=["GET"])
def get_analytics_data_quality_trips_route():
    return handle_request(
        endpoint="/analytics/data-quality/trips",
        method="GET",
        handler=endpoint.get_analytics_data_quality_trips,
    )
