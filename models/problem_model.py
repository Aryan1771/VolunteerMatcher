from datetime import datetime, timezone


def build_problem_document(data):
    now = datetime.now(timezone.utc)

    return {
        "location": data["location"],
        "problemType": data["problemType"],
        "severity": data["severity"],
        "description": data["description"],
        "availability": data["availability"],
        "workDate": data["workDate"],
        "status": data.get("status", "open"),
        "createdAt": now,
        "updatedAt": now,
    }


def serialize_problem(problem):
    if not problem:
        return None

    return {
        "id": str(problem["_id"]),
        "location": problem.get("location", ""),
        "problemType": problem.get("problemType", ""),
        "severity": problem.get("severity", 1),
        "description": problem.get("description", ""),
        "availability": problem.get("availability", ""),
        "workDate": problem.get("workDate", ""),
        "status": problem.get("status", "open"),
        "createdAt": problem.get("createdAt").isoformat() if problem.get("createdAt") else None,
        "updatedAt": problem.get("updatedAt").isoformat() if problem.get("updatedAt") else None,
    }
