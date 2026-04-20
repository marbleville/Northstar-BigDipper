from __future__ import annotations

from flask import request, jsonify

from backend.db_connection import get_db
from backend.northstar.responses import not_implemented, validation_error
from backend.northstar.validation import (
    EMPTY_SCHEMA,
    ValidationError,
    ensure_no_body,
    validate_json_body,
    validate_mapping,
)


NO_BODY = object()


def execute_query(query_payload):
    """Execute a query payload against the database"""
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        if "queries" in query_payload:
            # Multi-query execution
            results = []
            for query in query_payload["queries"]:
                cursor.execute(query["sql"], query.get("params", []))
                if query["sql"].strip().upper().startswith("SELECT"):
                    results.extend(cursor.fetchall())
                else:
                    db.commit()
            return {"data": results}
        elif "sql" in query_payload:
            # Single query execution
            cursor.execute(query_payload["sql"], query_payload.get("params", []))
            if query_payload["sql"].strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                return {"data": results}
            else:
                db.commit()
                return {"data": []}
        else:
            return {"error": "Invalid query payload"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()


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
        result = execute_query(query_payload)

        if "error" in result:
            return jsonify({"error": result["error"]}), 500
        else:
            return jsonify(result["data"]), 200
    except ValidationError as exc:
        return validation_error(exc.errors)
