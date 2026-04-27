# Smart Volunteer Matching System

A beginner-friendly Flask web application that collects local problem reports, registers volunteers, matches volunteers to problems with a simple scoring algorithm, and shows admin insights with Chart.js.

## Tech Stack

- Python Flask
- Google Cloud Firestore
- Google Cloud Run
- Google Cloud Build
- Google Gemini API
- HTML, CSS, and JavaScript
- Tailwind CSS CDN
- Chart.js CDN

## Features

- Public problem report form
- Public volunteer registration form
- Admin login with environment variable credentials
- Protected admin dashboard
- REST JSON APIs
- Problem and volunteer CRUD APIs
- Top 3 volunteer recommendations for every problem
- Problem type pie chart and area-wise bar chart
- Gemini API help chatbot on every page

## Folder Structure

```txt
VolunteerMatcher/
├── app.py
├── requirements.txt
├── Procfile
├── cloudbuild.yaml
├── .env.example
├── config/
├── models/
├── routes/
├── services/
├── utils/
├── templates/
└── static/
```

## Firestore Collections

### problems

```json
{
  "id": "Firestore document id",
  "location": "Mumbai",
  "problemType": "water",
  "severity": 4,
  "description": "No clean drinking water nearby.",
  "status": "open",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

### volunteers

```json
{
  "id": "Firestore document id",
  "name": "Rahul Sharma",
  "skills": ["water", "health"],
  "preferredLocation": "Mumbai",
  "availability": "weekends",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

## API Endpoints

### Auth

```http
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
```

### Problems

```http
POST   /api/problems
GET    /api/problems
GET    /api/problems/:id
PATCH  /api/problems/:id
DELETE /api/problems/:id
GET    /api/problems/:id/recommendations
```

### Volunteers

```http
POST   /api/volunteers
GET    /api/volunteers
GET    /api/volunteers/:id
PATCH  /api/volunteers/:id
DELETE /api/volunteers/:id
```

### Dashboard

```http
GET /api/dashboard/summary
GET /api/dashboard/problem-types
GET /api/dashboard/area-problems
GET /api/dashboard/recommendations
```

Admin-only endpoints require a successful login through `/api/auth/login`.

### Chatbot

```http
POST /api/chatbot/message
```

Request:

```json
{
  "message": "How do I register as a volunteer?"
}
```

The chatbot uses the Gemini API from the Flask backend so the browser never sees your API key.

## Matching Algorithm

Each volunteer receives a score for a problem:

```txt
Location match       +40
Skill match          +40
Severity priority    severity * 4
Anytime availability +10
```

The app sorts volunteers by score and returns the top 3.

## Run Locally

1. Install the Google Cloud CLI and sign in:

```bash
gcloud auth login
gcloud auth application-default login
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file from `.env.example`:

```bash
copy .env.example .env
```

5. Update `.env` with your Google Cloud project id, admin credentials, and Gemini API key.

6. Make sure Firestore is enabled in your Google Cloud project.

7. Start the app:

```bash
flask --app app run
```

8. Open:

```txt
http://127.0.0.1:5000
```

## Deploy on Google Cloud Run

1. Create or choose a Google Cloud project.

2. Enable required APIs:

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com firestore.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com
```

3. Create a Firestore database in Native mode from the Google Cloud Console.

4. Deploy from the repository folder:

```bash
gcloud run deploy volunteer-matcher ^
  --source . ^
  --region asia-south1 ^
  --allow-unauthenticated ^
  --set-env-vars ADMIN_USERNAME=admin,ADMIN_PASSWORD=change-this-password,SECRET_KEY=change-this-secret,GEMINI_API_KEY=your-gemini-key,GEMINI_MODEL=gemini-2.5-flash,FLASK_ENV=production
```

5. Open the Cloud Run service URL printed by the command.

## Optional Firebase Hosting Front Door

Use Firebase Hosting if you want a Firebase website URL or custom domain while still running Flask on Cloud Run.

1. Install Firebase CLI:

```bash
npm install -g firebase-tools
```

2. Sign in and initialize hosting:

```bash
firebase login
firebase init hosting
```

3. Configure `firebase.json` with a Cloud Run rewrite:

```json
{
  "hosting": {
    "rewrites": [
      {
        "source": "**",
        "run": {
          "serviceId": "volunteer-matcher",
          "region": "asia-south1"
        }
      }
    ]
  }
}
```

4. Deploy:

```bash
firebase deploy
```

## Environment Variables

```txt
GOOGLE_CLOUD_PROJECT
ADMIN_USERNAME
ADMIN_PASSWORD
SECRET_KEY
GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash
FLASK_ENV=production
```

## Notes

- Firestore is the database for forms, APIs, and dashboard data.
- Cloud Run uses its Google service account automatically when deployed on Google Cloud.
- Admin credentials are stored in environment variables for simplicity.
- The existing GPLv3 license is preserved.
