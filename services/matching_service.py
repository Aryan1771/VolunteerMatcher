from models.volunteer_model import serialize_volunteer


def normalize(value):
    return str(value or "").strip().lower()


def calculate_volunteer_score(problem, volunteer):
    """Simple, readable scoring so beginners can tune it later."""
    score = 0

    problem_location = normalize(problem.get("location"))
    volunteer_location = normalize(volunteer.get("preferredLocation"))
    problem_type = normalize(problem.get("problemType"))
    volunteer_skills = {normalize(skill) for skill in volunteer.get("skills", [])}
    problem_availability = normalize(problem.get("availability"))
    volunteer_availability = normalize(volunteer.get("availability"))
    problem_work_date = normalize(problem.get("workDate"))
    volunteer_available_date = normalize(volunteer.get("availableDate"))

    if problem_location and problem_location == volunteer_location:
        score += 40

    if problem_type in volunteer_skills:
        score += 40

    score += int(problem.get("severity", 1)) * 4

    if problem_availability and volunteer_availability == problem_availability:
        score += 20
    elif volunteer_availability == "anytime":
        score += 10

    if problem_work_date and problem_work_date == volunteer_available_date:
        score += 30

    if volunteer_availability == "anytime":
        score += 10

    return score


def get_top_volunteers_for_problem(problem, volunteers, limit=3):
    scored_volunteers = []

    for volunteer in volunteers:
        score = calculate_volunteer_score(problem, volunteer)
        scored_volunteers.append((score, volunteer))

    scored_volunteers.sort(key=lambda item: item[0], reverse=True)

    return [
        serialize_volunteer(volunteer, score=score)
        for score, volunteer in scored_volunteers[:limit]
    ]
