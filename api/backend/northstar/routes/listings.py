from backend.northstar.blueprint import listing_bp
from backend.northstar.contracts import LISTING_CREATE_BODY, LISTINGS_QUERY
from backend.northstar.endpoints import listings as endpoint
from backend.northstar.route_utils import handle_request


@listing_bp.route("/listings", methods=["GET"])
def get_listings_route():
    return handle_request(
        endpoint="/listings",
        method="GET",
        handler=endpoint.get_listings,
        query_schema=LISTINGS_QUERY,
    )


@listing_bp.route("/listings", methods=["POST"])
def create_listings_route():
    return handle_request(
        endpoint="/listings",
        method="POST",
        handler=endpoint.post_listings,
        body_schema=LISTING_CREATE_BODY,
    )
