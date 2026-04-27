from datetime import datetime, timezone

from google.api_core.exceptions import GoogleAPIError

from flask import Blueprint, request

from config.database import create_document, delete_document, get_document, list_documents, update_document
from models.problem_model import build_problem_document, serialize_problem
from routes.auth_routes import admin_required
from services.matching_service import get_top_volunteers_for_problem
from utils.response_helpers import error_response, success_response, valid_document_id
from utils.validators import validate_problem_payload


problem_bp = Blueprint("problems", __name__, url_prefix="/api/problems")


@problem_bp.post("")
def create_problem():
    data, errors = validate_problem_payload(request.get_json(silent=True))
    if errors:
        return error_response("Please fix the problem form.", 400, errors)

    try:
        problem = build_problem_document(data)
        problem = create_document("problems", problem)
        return success_response("Problem report submitted.", serialize_problem(problem), 201)
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@problem_bp.get("")
@admin_required
def list_problems():
    try:
        problems = list_documents("problems", order_by="createdAt", descending=True)
        return success_response(data=[serialize_problem(problem) for problem in problems])
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@problem_bp.get("/<problem_id>")
@admin_required
def get_problem(problem_id):
    document_id = valid_document_id(problem_id)
    if document_id is None:
        return error_response("Invalid problem id.", 400)

    try:
        problem = get_document("problems", document_id)
        if not problem:
            return error_response("Problem not found.", 404)

        return success_response(data=serialize_problem(problem))
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@problem_bp.patch("/<problem_id>")
@admin_required
def update_problem(problem_id):
    document_id = valid_document_id(problem_id)
    if document_id is None:
        return error_response("Invalid problem id.", 400)

    data, errors = validate_problem_payload(request.get_json(silent=True), partial=True)
    if errors:
        return error_response("Please fix the problem update.", 400, errors)

    if not data:
        return error_response("No valid fields were provided.", 400)

    data["updatedAt"] = datetime.now(timezone.utc)

    try:
        problem = update_document("problems", document_id, data)
        if not problem:
            return error_response("Problem not found.", 404)

        return success_response("Problem updated.", serialize_problem(problem))
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@problem_bp.delete("/<problem_id>")
@admin_required
def delete_problem(problem_id):
    document_id = valid_document_id(problem_id)
    if document_id is None:
        return error_response("Invalid problem id.", 400)

    try:
        deleted = delete_document("problems", document_id)
        if not deleted:
            return error_response("Problem not found.", 404)

        return success_response("Problem deleted.")
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@problem_bp.get("/<problem_id>/recommendations")
@admin_required
def get_problem_recommendations(problem_id):
    document_id = valid_document_id(problem_id)
    if document_id is None:
        return error_response("Invalid problem id.", 400)

    try:
        problem = get_document("problems", document_id)
        if not problem:
            return error_response("Problem not found.", 404)

        volunteers = list_documents("volunteers")
        recommendations = get_top_volunteers_for_problem(problem, volunteers)

        return success_response(
            data={
                "problem": serialize_problem(problem),
                "recommendedVolunteers": recommendations,
            }
        )
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)
