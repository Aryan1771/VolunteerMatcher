from collections import Counter

from google.api_core.exceptions import GoogleAPIError

from flask import Blueprint

from config.database import list_documents
from models.problem_model import serialize_problem
from models.volunteer_model import serialize_volunteer
from routes.auth_routes import admin_required
from services.matching_service import get_top_volunteers_for_problem
from utils.response_helpers import error_response, success_response


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_bp.get("/summary")
@admin_required
def dashboard_summary():
    try:
        problems = list_documents("problems")
        volunteers = list_documents("volunteers")

        data = {
            "totalProblems": len(problems),
            "totalVolunteers": len(volunteers),
            "openProblems": sum(1 for problem in problems if problem.get("status") == "open"),
            "resolvedProblems": sum(1 for problem in problems if problem.get("status") == "resolved"),
        }

        return success_response(data=data)
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@dashboard_bp.get("/problem-types")
@admin_required
def problem_type_distribution():
    try:
        counts = Counter(problem.get("problemType", "unknown") for problem in list_documents("problems"))
        data = [{"type": key, "count": value} for key, value in counts.most_common()]

        return success_response(data=data)
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@dashboard_bp.get("/area-problems")
@admin_required
def area_wise_problems():
    try:
        counts = Counter(problem.get("location", "Unknown") for problem in list_documents("problems"))
        data = [{"location": key, "count": value} for key, value in counts.most_common()]

        return success_response(data=data)
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@dashboard_bp.get("/recommendations")
@admin_required
def dashboard_recommendations():
    try:
        problems = list_documents("problems", order_by="createdAt", descending=True)
        volunteers = list_documents("volunteers")

        data = []
        for problem in problems:
            data.append(
                {
                    "problem": serialize_problem(problem),
                    "recommendedVolunteers": get_top_volunteers_for_problem(problem, volunteers),
                }
            )

        return success_response(data=data)
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)


@dashboard_bp.get("/volunteers")
@admin_required
def dashboard_volunteers():
    try:
        volunteers = list_documents("volunteers", order_by="createdAt", descending=True)
        return success_response(data=[serialize_volunteer(volunteer) for volunteer in volunteers])
    except (RuntimeError, GoogleAPIError) as exc:
        return error_response(str(exc), 500)
