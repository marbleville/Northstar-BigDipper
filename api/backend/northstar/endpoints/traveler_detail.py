from backend.northstar.endpoint_utils import (
    collect_fields,
    deactivate_payload,
    select_payload,
    update_payload,
)


TRAVELER_UPDATE_FIELDS = [
    "first_name",
    "last_name",
    "phone",
    "email",
    "availability",
    "traveler_status",
    "is_active",
]


def get_traveler_detail(validated):
    traveler_id = validated["path"]["traveler_id"]
    sql = """
        SELECT
            traveler_id,
            first_name,
            last_name,
            phone,
            email,
            availability,
            traveler_status,
            is_active
        FROM Traveler
    """
    return select_payload(sql, filters=(["traveler_id = %s"], [traveler_id]))


def put_traveler_detail(validated):
    traveler_id = validated["path"]["traveler_id"]
    values = collect_fields(validated["body"], TRAVELER_UPDATE_FIELDS)
    return update_payload(
        "Traveler",
        values,
        where_clause="traveler_id = %s",
        where_params=[traveler_id],
    )


def delete_traveler_detail(validated):
    traveler_id = validated["path"]["traveler_id"]
    return deactivate_payload(
        "Traveler",
        where_clause="traveler_id = %s",
        where_params=[traveler_id],
    )


def get_traveler_trips(validated):
    traveler_id = validated["path"]["traveler_id"]
    sql = """
        SELECT
            t.trip_id,
            t.trip_name,
            t.destination,
            t.city,
            t.country,
            t.start_date,
            t.end_date,
            t.trip_status,
            t.group_size,
            tt.start_date as traveler_start_date,
            tt.end_date as traveler_end_date
        FROM Trip t
        JOIN Trip_Traveler tt ON t.trip_id = tt.trip_id
        WHERE tt.traveler_id = %s
        ORDER BY t.start_date DESC
    """
    return select_payload(sql, params=[traveler_id])
