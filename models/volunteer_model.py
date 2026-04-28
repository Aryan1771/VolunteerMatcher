from datetime import datetime, timezone


def build_volunteer_document(data):
    now = datetime.now(timezone.utc)

    return {
        "name": data["name"],
        "skills": data["skills"],
        "preferredLocation": data["preferredLocation"],
        "availability": data["availability"],
        "availableDate": data["availableDate"],
        "createdAt": now,
        "updatedAt": now,
    }


def serialize_volunteer(volunteer, score=None):
    if not volunteer:
        return None

    serialized = {
        "id": str(volunteer["_id"]),
        "name": volunteer.get("name", ""),
        "skills": volunteer.get("skills", []),
        "preferredLocation": volunteer.get("preferredLocation", ""),
        "availability": volunteer.get("availability", ""),
        "availableDate": volunteer.get("availableDate", ""),
        "createdAt": volunteer.get("createdAt").isoformat() if volunteer.get("createdAt") else None,
        "updatedAt": volunteer.get("updatedAt").isoformat() if volunteer.get("updatedAt") else None,
    }

    if score is not None:
        serialized["score"] = score

    return serialized
