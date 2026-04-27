# VolunteerMatcher

VolunteerMatcher is a Flask web application for connecting local community problems with suitable volunteers. It includes public forms for reporting problems and registering volunteers, an admin dashboard for reviewing submissions, a simple recommendation engine, and an optional Gemini-powered help chatbot.

## Features

- Public landing page with separate flows for problem reports and volunteer registration
- Admin login and dashboard pages for managing submitted data
- REST-style API routes for problems, volunteers, dashboard data, and chatbot support
- Firestore-backed persistence through Google Cloud Firestore
- Volunteer matching score based on location, skills, severity, and availability
- Optional Gemini chatbot that answers questions about how the application works
- Cloud deployment files for Gunicorn/Procfile and Google Cloud Build

## Tech Stack

- Python
- Flask
- Google Cloud Firestore
- Google Gemini API
- HTML, CSS, and JavaScript
- Gunicorn for production serving

## Project Structure

```text
app.py                  Flask application entry point
config/                 Firestore configuration
models/                 Problem and volunteer document builders
routes/                 Auth, dashboard, problem, volunteer, and chatbot routes
services/               Gemini and volunteer matching services
static/                 Frontend CSS and JavaScript
templates/              Jinja HTML templates
utils/                  Validation and response helpers
cloudbuild.yaml         Google Cloud deployment configuration
Procfile                Production process definition
```

## Getting Started

### 1. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example environment file and fill in your project-specific values.

```powershell
Copy-Item .env.example .env
```

Required or commonly used values:

```text
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account-key.json
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-this-password
SECRET_KEY=change-this-secret-key
GEMINI_API_KEY=your-google-ai-studio-api-key
GEMINI_MODEL=gemini-2.5-flash
```

### 4. Run the application

```powershell
python app.py
```

The local development server starts with Flask debug mode enabled unless `FLASK_ENV` is set to `production`.

## API Highlights

- `POST /api/problems` submits a new community problem
- `POST /api/volunteers` registers a new volunteer
- `GET /api/problems` lists problems for authenticated admins
- `GET /api/volunteers` lists volunteers for authenticated admins
- `GET /api/problems/<problem_id>/recommendations` returns top volunteer matches
- `POST /api/chatbot` sends a help question to the Gemini-backed chatbot

## Notes

This project is designed as a practical full-stack learning app. For production use, replace default credentials, use strong secrets, configure Firestore security carefully, and deploy with a service account that has only the permissions the app needs.

## License

This repository is licensed under the GPL-3.0 license. See `LICENSE` for details.
