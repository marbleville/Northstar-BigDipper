from __future__ import annotations

from flask import request

from backend.northstar.responses import not_implemented, validation_error
from backend.northstar.validation import (
    EMPTY_SCHEMA,
    ValidationError,
    ensure_no_body,
    validate_json_body,
    validate_mapping,
)


NO_BODY = object()


def handle_request(
    *,
    endpoint,
    method,
    handler,
    path_values=None,
    path_schema=None,
    query_schema=None,
    body_schema=NO_BODY,
):
    try:
        validated = {}

        if path_schema is not None:
            validated["path"] = validate_mapping(path_values or {}, path_schema)

        active_query_schema = query_schema or EMPTY_SCHEMA
        validated["query"] = validate_mapping(
            request.args.to_dict(flat=True),
            active_query_schema,
        )

        if body_schema is NO_BODY:
            ensure_no_body(request)
        else:
            validated["body"] = validate_json_body(request, body_schema)

        query_payload = handler(validated)
        return not_implemented(endpoint, method, validated, query_payload)
    except ValidationError as exc:
        return validation_error(exc.errors)
