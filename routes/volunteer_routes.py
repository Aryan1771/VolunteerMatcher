from datetime import datetime, timezone

from pymongo.errors import PyMongoError

from flask import Blueprint, request

from config.database import get_collection
from models.volunteer_model import build_volunteer_document, serialize_volunteer
from routes.auth_routes import admin_required
from utils.response_helpers import error_response, object_id_from_string, success_response
from utils.validators import validate_volunteer_payload


volunteer_bp = Blueprint("volunteers", __name__, url_prefix="/api/volunteers")


@volunteer_bp.post("")
def create_volunteer():
    data, errors = validate_volunteer_payload(request.get_json(silent=True))
    if errors:
        return error_response("Please fix the volunteer form.", 400, errors)

    try:
        volunteer = build_volunteer_document(data)
        result = get_collection("volunteers").insert_one(volunteer)
        volunteer["_id"] = result.inserted_id
        return success_response("Volunteer registered.", serialize_volunteer(volunteer), 201)
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@volunteer_bp.get("")
@admin_required
def list_volunteers():
    try:
        volunteers = list(get_collection("volunteers").find().sort("createdAt", -1))
        return success_response(data=[serialize_volunteer(volunteer) for volunteer in volunteers])
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@volunteer_bp.get("/<volunteer_id>")
@admin_required
def get_volunteer(volunteer_id):
    object_id = object_id_from_string(volunteer_id)
    if object_id is None:
        return error_response("Invalid volunteer id.", 400)

    try:
        volunteer = get_collection("volunteers").find_one({"_id": object_id})
        if not volunteer:
            return error_response("Volunteer not found.", 404)

        return success_response(data=serialize_volunteer(volunteer))
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@volunteer_bp.patch("/<volunteer_id>")
@admin_required
def update_volunteer(volunteer_id):
    object_id = object_id_from_string(volunteer_id)
    if object_id is None:
        return error_response("Invalid volunteer id.", 400)

    data, errors = validate_volunteer_payload(request.get_json(silent=True), partial=True)
    if errors:
        return error_response("Please fix the volunteer update.", 400, errors)

    if not data:
        return error_response("No valid fields were provided.", 400)

    data["updatedAt"] = datetime.now(timezone.utc)

    try:
        result = get_collection("volunteers").update_one({"_id": object_id}, {"$set": data})
        if result.matched_count == 0:
            return error_response("Volunteer not found.", 404)

        volunteer = get_collection("volunteers").find_one({"_id": object_id})
        return success_response("Volunteer updated.", serialize_volunteer(volunteer))
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@volunteer_bp.delete("/<volunteer_id>")
@admin_required
def delete_volunteer(volunteer_id):
    object_id = object_id_from_string(volunteer_id)
    if object_id is None:
        return error_response("Invalid volunteer id.", 400)

    try:
        result = get_collection("volunteers").delete_one({"_id": object_id})
        if result.deleted_count == 0:
            return error_response("Volunteer not found.", 404)

        return success_response("Volunteer deleted.")
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)
