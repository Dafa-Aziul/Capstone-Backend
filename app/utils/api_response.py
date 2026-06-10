from datetime import datetime, timezone

from flask import jsonify


def success_response(message, data=None, meta=None, status_code=200):
    payload = {
        "success": True,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if data is not None:
        payload["data"] = data

    if meta is not None:
        payload["meta"] = meta

    return jsonify(payload), status_code


def error_response(message, errors=None, status_code=400):
    payload = {
        "success": False,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "errors": errors,
    }

    return jsonify(payload), status_code
