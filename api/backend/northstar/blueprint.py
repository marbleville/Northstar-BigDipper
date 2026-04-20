from flask import Blueprint


planner_bp = Blueprint("planner", __name__)
traveler_bp = Blueprint("traveler", __name__)
vendor_bp = Blueprint("vendor", __name__)
trip_bp = Blueprint("trip", __name__)
notification_bp = Blueprint("notification", __name__)
promotion_bp = Blueprint("promotion", __name__)
listing_bp = Blueprint("listing", __name__)
booking_bp = Blueprint("booking", __name__)
funding_request_bp = Blueprint("funding_request", __name__)
trip_traveler_bp = Blueprint("trip_traveler", __name__)
traveler_booking_bp = Blueprint("traveler_booking", __name__)
traveler_preference_bp = Blueprint("traveler_preference", __name__)
listing_amenity_bp = Blueprint("listing_amenity", __name__)
traveler_vote_bp = Blueprint("traveler_vote", __name__)


NORTHSTAR_BLUEPRINTS = (
    planner_bp,
    traveler_bp,
    vendor_bp,
    trip_bp,
    notification_bp,
    promotion_bp,
    listing_bp,
    booking_bp,
    funding_request_bp,
    trip_traveler_bp,
    traveler_booking_bp,
    traveler_preference_bp,
    listing_amenity_bp,
    traveler_vote_bp,
)
