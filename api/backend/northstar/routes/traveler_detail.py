from backend.northstar.blueprint import traveler_bp
from backend.northstar.contracts import TRAVELER_ID_PATH, TRAVELER_UPDATE_BODY
from backend.northstar.endpoints import traveler_detail as endpoint
from backend.northstar.route_utils import handle_request


@traveler_bp.route("/travelers/<int:traveler_id>", methods=["GET"])
def get_traveler_detail_route(traveler_id):
    return handle_request(
        endpoint="/travelers/{travelerId}",
        method="GET",
        handler=endpoint.get_traveler_detail,
        path_values={"traveler_id": traveler_id},
        path_schema=TRAVELER_ID_PATH,
    )


@traveler_bp.route("/travelers/<int:traveler_id>", methods=["PUT"])
def update_traveler_detail_route(traveler_id):
    return handle_request(
        endpoint="/travelers/{travelerId}",
        method="PUT",
        handler=endpoint.put_traveler_detail,
        path_values={"traveler_id": traveler_id},
        path_schema=TRAVELER_ID_PATH,
        body_schema=TRAVELER_UPDATE_BODY,
    )


@traveler_bp.route("/travelers/<int:traveler_id>", methods=["DELETE"])
def delete_traveler_detail_route(traveler_id):
    return handle_request(
        endpoint="/travelers/{travelerId}",
        method="DELETE",
        handler=endpoint.delete_traveler_detail,
        path_values={"traveler_id": traveler_id},
        path_schema=TRAVELER_ID_PATH,
    )


@traveler_bp.route("/travelers/<int:traveler_id>/trips", methods=["GET"])
def get_traveler_trips_route(traveler_id):
    return handle_request(
        endpoint="/travelers/{travelerId}/trips",
        method="GET",
        handler=endpoint.get_traveler_trips,
        path_values={"traveler_id": traveler_id},
        path_schema=TRAVELER_ID_PATH,
    )
