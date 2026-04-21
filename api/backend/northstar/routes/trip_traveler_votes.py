from backend.northstar.blueprint import northstar
from backend.northstar.contracts import (
    TRIP_TRAVELER_PATH,
    TRIP_TRAVELER_VOTE_BODY,
    TRIP_TRAVELER_VOTE_DELETE_BODY,
    TRIP_TRAVELER_LISTING_PATH,
    EMPTY_BODY,
)
from backend.northstar.endpoints import trip_traveler_votes as endpoint
from backend.northstar.route_utils import handle_request


@northstar.route("/trips/<int:trip_id>/travelers/<int:traveler_id>/votes", methods=["GET"])
def get_trip_traveler_votes_route(trip_id, traveler_id):
    return handle_request(
        endpoint="/trips/{tripId}/travelers/{travelerId}/votes",
        method="GET",
        handler=endpoint.get_trip_traveler_votes,
        path_values={"trip_id": trip_id, "traveler_id": traveler_id},
        path_schema=TRIP_TRAVELER_PATH,
    )


@northstar.route("/trips/<int:trip_id>/travelers/<int:traveler_id>/votes", methods=["POST"])
def create_trip_traveler_votes_route(trip_id, traveler_id):
    return handle_request(
        endpoint="/trips/{tripId}/travelers/{travelerId}/votes",
        method="POST",
        handler=endpoint.post_trip_traveler_votes,
        path_values={"trip_id": trip_id, "traveler_id": traveler_id},
        path_schema=TRIP_TRAVELER_PATH,
        body_schema=TRIP_TRAVELER_VOTE_BODY,
    )


@northstar.route("/trips/<int:trip_id>/travelers/<int:traveler_id>/votes", methods=["PUT"])
def update_trip_traveler_votes_route(trip_id, traveler_id):
    return handle_request(
        endpoint="/trips/{tripId}/travelers/{travelerId}/votes",
        method="PUT",
        handler=endpoint.put_trip_traveler_votes,
        path_values={"trip_id": trip_id, "traveler_id": traveler_id},
        path_schema=TRIP_TRAVELER_PATH,
        body_schema=TRIP_TRAVELER_VOTE_BODY,
    )

@northstar.route("/trips/<int:trip_id>/travelers/<int:traveler_id>/votes/<int:listing_id>/save", methods=["PUT"])
def toggle_save_route(trip_id, traveler_id, listing_id):
    return handle_request(
        endpoint="/trips/{tripId}/travelers/{travelerId}/votes/{listingId}/save",
        method="PUT",
        handler=endpoint.toggle_save,
        path_values={"trip_id": trip_id, "traveler_id": traveler_id, "listing_id": listing_id},
        path_schema=TRIP_TRAVELER_LISTING_PATH,
        body_schema=EMPTY_BODY,
    )


@northstar.route("/trips/<int:trip_id>/travelers/<int:traveler_id>/saves", methods=["GET"])
def get_saves_route(trip_id, traveler_id):
    return handle_request(
        endpoint="/trips/{tripId}/travelers/{travelerId}/saves",
        method="GET",
        handler=endpoint.get_saves,
        path_values={"trip_id": trip_id, "traveler_id": traveler_id},
        path_schema=TRIP_TRAVELER_PATH, 
    )

@northstar.route(
    "/trips/<int:trip_id>/travelers/<int:traveler_id>/votes",
    methods=["DELETE"],
)
def delete_trip_traveler_votes_route(trip_id, traveler_id):
    return handle_request(
        endpoint="/trips/{tripId}/travelers/{travelerId}/votes",
        method="DELETE",
        handler=endpoint.delete_trip_traveler_votes,
        path_values={"trip_id": trip_id, "traveler_id": traveler_id},
        path_schema=TRIP_TRAVELER_PATH,
        body_schema=TRIP_TRAVELER_VOTE_DELETE_BODY,
    )
