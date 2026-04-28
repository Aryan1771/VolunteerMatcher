from datetime import datetime, timezone

from pymongo.errors import PyMongoError

from flask import Blueprint, request

from config.database import get_collection
from models.problem_model import build_problem_document, serialize_problem
from routes.auth_routes import admin_required
from services.matching_service import get_top_volunteers_for_problem
from utils.response_helpers import error_response, object_id_from_string, success_response
from utils.validators import validate_problem_payload


problem_bp = Blueprint("problems", __name__, url_prefix="/api/problems")


@problem_bp.post("")
def create_problem():
    data, errors = validate_problem_payload(request.get_json(silent=True))
    if errors:
        return error_response("Please fix the problem form.", 400, errors)

    try:
        problem = build_problem_document(data)
        result = get_collection("problems").insert_one(problem)
        problem["_id"] = result.inserted_id
        return success_response("Problem report submitted.", serialize_problem(problem), 201)
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@problem_bp.get("")
@admin_required
def list_problems():
    try:
        problems = list(get_collection("problems").find().sort("createdAt", -1))
        return success_response(data=[serialize_problem(problem) for problem in problems])
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@problem_bp.get("/<problem_id>")
@admin_required
def get_problem(problem_id):
    object_id = object_id_from_string(problem_id)
    if object_id is None:
        return error_response("Invalid problem id.", 400)

    try:
        problem = get_collection("problems").find_one({"_id": object_id})
        if not problem:
            return error_response("Problem not found.", 404)

        return success_response(data=serialize_problem(problem))
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@problem_bp.patch("/<problem_id>")
@admin_required
def update_problem(problem_id):
    object_id = object_id_from_string(problem_id)
    if object_id is None:
        return error_response("Invalid problem id.", 400)

    data, errors = validate_problem_payload(request.get_json(silent=True), partial=True)
    if errors:
        return error_response("Please fix the problem update.", 400, errors)

    if not data:
        return error_response("No valid fields were provided.", 400)

    data["updatedAt"] = datetime.now(timezone.utc)

    try:
        result = get_collection("problems").update_one({"_id": object_id}, {"$set": data})
        if result.matched_count == 0:
            return error_response("Problem not found.", 404)

        problem = get_collection("problems").find_one({"_id": object_id})
        return success_response("Problem updated.", serialize_problem(problem))
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@problem_bp.delete("/<problem_id>")
@admin_required
def delete_problem(problem_id):
    object_id = object_id_from_string(problem_id)
    if object_id is None:
        return error_response("Invalid problem id.", 400)

    try:
        result = get_collection("problems").delete_one({"_id": object_id})
        if result.deleted_count == 0:
            return error_response("Problem not found.", 404)

        return success_response("Problem deleted.")
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@problem_bp.get("/<problem_id>/recommendations")
@admin_required
def get_problem_recommendations(problem_id):
    object_id = object_id_from_string(problem_id)
    if object_id is None:
        return error_response("Invalid problem id.", 400)

    try:
        problem = get_collection("problems").find_one({"_id": object_id})
        if not problem:
            return error_response("Problem not found.", 404)

        volunteers = list(get_collection("volunteers").find())
        recommendations = get_top_volunteers_for_problem(problem, volunteers)

        return success_response(
            data={
                "problem": serialize_problem(problem),
                "recommendedVolunteers": recommendations,
            }
        )
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)
