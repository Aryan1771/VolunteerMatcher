from datetime import datetime, timezone

from google.api_core.exceptions import GoogleAPIError

from flask import Blueprint, request

from config.database import create_document, delete_document, get_document, list_documents, update_document
from models.volunteer_model import build_volunteer_document, serialize_volunteer
from routes.auth_routes import admin_required
from utils.response_helpers import error_response, success_response, valid_document_id
from utils.validators import validate_volunteer_payload


volunteer_bp = Blueprint("volunteers", __name__, url_prefix="/api/volunteers")


@volunteer_bp.post("")
def create_volunteer():
    data, errors = validate_volunteer_payload(request.get_json(silent=True))
    if errors:
        return error_response("Please fix the volunteer form.", 400, errors)

    try:
        volunteer = build_volunteer_document(data)
        volunteer = create_document("volunteers", volunteer)
        return success_response("Volunteer registered.", serialize_volunteer(volunteer), 201)
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@volunteer_bp.get("")
@admin_required
def list_volunteers():
    try:
        volunteers = list_documents("volunteers", order_by="createdAt", descending=True)
        return success_response(data=[serialize_volunteer(volunteer) for volunteer in volunteers])
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@volunteer_bp.get("/<volunteer_id>")
@admin_required
def get_volunteer(volunteer_id):
    document_id = valid_document_id(volunteer_id)
    if document_id is None:
        return error_response("Invalid volunteer id.", 400)

    try:
        volunteer = get_document("volunteers", document_id)
        if not volunteer:
            return error_response("Volunteer not found.", 404)

        return success_response(data=serialize_volunteer(volunteer))
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@volunteer_bp.patch("/<volunteer_id>")
@admin_required
def update_volunteer(volunteer_id):
    document_id = valid_document_id(volunteer_id)
    if document_id is None:
        return error_response("Invalid volunteer id.", 400)

    data, errors = validate_volunteer_payload(request.get_json(silent=True), partial=True)
    if errors:
        return error_response("Please fix the volunteer update.", 400, errors)

    if not data:
        return error_response("No valid fields were provided.", 400)

    data["updatedAt"] = datetime.now(timezone.utc)

    try:
        volunteer = update_document("volunteers", document_id, data)
        if not volunteer:
            return error_response("Volunteer not found.", 404)

        return success_response("Volunteer updated.", serialize_volunteer(volunteer))
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@volunteer_bp.delete("/<volunteer_id>")
@admin_required
def delete_volunteer(volunteer_id):
    document_id = valid_document_id(volunteer_id)
    if document_id is None:
        return error_response("Invalid volunteer id.", 400)

    try:
        deleted = delete_document("volunteers", document_id)
        if not deleted:
            return error_response("Volunteer not found.", 404)

        return success_response("Volunteer deleted.")
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)
