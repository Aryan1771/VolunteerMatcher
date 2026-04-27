from flask import jsonify


def make_response(success, message=None, data=None, status_code=200):
    payload = {"success": success}

    if message is not None:
        payload["message"] = message

    if data is not None:
        payload["data"] = data

    return jsonify(payload), status_code


def success_response(message=None, data=None, status_code=200):
    return make_response(True, message, data, status_code)


def error_response(message, status_code=400, errors=None):
    payload = {"success": False, "message": message}

    if errors:
        payload["errors"] = errors

    return jsonify(payload), status_code


def valid_document_id(value):
    value = str(value or "").strip()
    if not value or "/" in value:
        return None

    return value
