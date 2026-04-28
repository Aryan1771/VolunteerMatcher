from datetime import date


PROBLEM_TYPES = {"water", "health", "education"}
AVAILABILITIES = {"weekdays", "weekends", "anytime"}
PROBLEM_STATUSES = {"open", "assigned", "resolved"}


def clean_text(value):
    if value is None:
        return ""

    return str(value).strip()


def normalize_choice(value):
    return clean_text(value).lower()


def validate_date_string(value, field_name, errors):
    raw_date = clean_text(value)
    if not raw_date:
        errors[field_name] = "Date is required."
        return None

    try:
        date.fromisoformat(raw_date)
    except ValueError:
        errors[field_name] = "Date must use YYYY-MM-DD format."
        return None

    return raw_date


def validate_problem_payload(payload, partial=False):
    """Validate problem JSON and return a cleaned document plus errors."""
    payload = payload or {}
    cleaned = {}
    errors = {}

    if not partial or "location" in payload:
        location = clean_text(payload.get("location"))
        if not location:
            errors["location"] = "Location is required."
        else:
            cleaned["location"] = location

    if not partial or "problemType" in payload:
        problem_type = normalize_choice(payload.get("problemType"))
        if problem_type not in PROBLEM_TYPES:
            errors["problemType"] = "Problem type must be water, health, or education."
        else:
            cleaned["problemType"] = problem_type

    if not partial or "severity" in payload:
        try:
            severity = int(payload.get("severity"))
        except (TypeError, ValueError):
            severity = None

        if severity is None or severity < 1 or severity > 5:
            errors["severity"] = "Severity must be a number from 1 to 5."
        else:
            cleaned["severity"] = severity

    if not partial or "description" in payload:
        description = clean_text(payload.get("description"))
        if not description:
            errors["description"] = "Description is required."
        else:
            cleaned["description"] = description

    if not partial or "availability" in payload:
        availability = normalize_choice(payload.get("availability"))
        if availability not in AVAILABILITIES:
            errors["availability"] = "Availability must be weekdays, weekends, or anytime."
        else:
            cleaned["availability"] = availability

    if not partial or "workDate" in payload:
        work_date = validate_date_string(payload.get("workDate"), "workDate", errors)
        if work_date:
            cleaned["workDate"] = work_date

    if "status" in payload:
        status = normalize_choice(payload.get("status"))
        if status not in PROBLEM_STATUSES:
            errors["status"] = "Status must be open, assigned, or resolved."
        else:
            cleaned["status"] = status

    return cleaned, errors


def validate_volunteer_payload(payload, partial=False):
    """Validate volunteer JSON and return a cleaned document plus errors."""
    payload = payload or {}
    cleaned = {}
    errors = {}

    if not partial or "name" in payload:
        name = clean_text(payload.get("name"))
        if not name:
            errors["name"] = "Name is required."
        else:
            cleaned["name"] = name

    if not partial or "skills" in payload:
        raw_skills = payload.get("skills", [])
        if isinstance(raw_skills, str):
            raw_skills = [part.strip() for part in raw_skills.split(",")]

        skills = []
        for skill in raw_skills if isinstance(raw_skills, list) else []:
            normalized = normalize_choice(skill)
            if normalized:
                skills.append(normalized)

        skills = sorted(set(skills))

        if not skills:
            errors["skills"] = "Choose at least one skill."
        elif any(skill not in PROBLEM_TYPES for skill in skills):
            errors["skills"] = "Skills must use water, health, or education."
        else:
            cleaned["skills"] = skills

    if not partial or "preferredLocation" in payload:
        preferred_location = clean_text(payload.get("preferredLocation"))
        if not preferred_location:
            errors["preferredLocation"] = "Preferred location is required."
        else:
            cleaned["preferredLocation"] = preferred_location

    if not partial or "availability" in payload:
        availability = normalize_choice(payload.get("availability"))
        if availability not in AVAILABILITIES:
            errors["availability"] = "Availability must be weekdays, weekends, or anytime."
        else:
            cleaned["availability"] = availability

    if not partial or "availableDate" in payload:
        available_date = validate_date_string(payload.get("availableDate"), "availableDate", errors)
        if available_date:
            cleaned["availableDate"] = available_date

    return cleaned, errors
