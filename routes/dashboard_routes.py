from pymongo.errors import PyMongoError

from flask import Blueprint

from config.database import get_collection
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
        problems = get_collection("problems")
        volunteers = get_collection("volunteers")

        data = {
            "totalProblems": problems.count_documents({}),
            "totalVolunteers": volunteers.count_documents({}),
            "openProblems": problems.count_documents({"status": "open"}),
            "resolvedProblems": problems.count_documents({"status": "resolved"}),
        }

        return success_response(data=data)
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@dashboard_bp.get("/problem-types")
@admin_required
def problem_type_distribution():
    try:
        pipeline = [
            {"$group": {"_id": "$problemType", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]
        rows = list(get_collection("problems").aggregate(pipeline))
        data = [{"type": row["_id"], "count": row["count"]} for row in rows]

        return success_response(data=data)
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@dashboard_bp.get("/area-problems")
@admin_required
def area_wise_problems():
    try:
        pipeline = [
            {"$group": {"_id": "$location", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]
        rows = list(get_collection("problems").aggregate(pipeline))
        data = [{"location": row["_id"], "count": row["count"]} for row in rows]

        return success_response(data=data)
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@dashboard_bp.get("/recommendations")
@admin_required
def dashboard_recommendations():
    try:
        problems = list(get_collection("problems").find().sort("createdAt", -1))
        volunteers = list(get_collection("volunteers").find())

        data = []
        for problem in problems:
            data.append(
                {
                    "problem": serialize_problem(problem),
                    "recommendedVolunteers": get_top_volunteers_for_problem(problem, volunteers),
                }
            )

        return success_response(data=data)
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)


@dashboard_bp.get("/volunteers")
@admin_required
def dashboard_volunteers():
    try:
        volunteers = list(get_collection("volunteers").find().sort("createdAt", -1))
        return success_response(data=[serialize_volunteer(volunteer) for volunteer in volunteers])
    except (RuntimeError, PyMongoError) as exc:
        return error_response(str(exc), 500)
