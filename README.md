# Smart Volunteer Matching System

VolunteerMatcher is a beginner-friendly Flask web application for connecting local community problems with suitable volunteers. It includes public forms for reporting problems and registering volunteers, an admin dashboard with charts, a simple recommendation engine, and a Gemini-powered help chatbot.

## Tech Stack

- Python Flask
- MongoDB Atlas
- HTML, CSS, and JavaScript
- Tailwind CSS CDN
- Chart.js CDN
- Google Gemini API
- Render free web service

## Features

- Public landing page with separate flows for problem reports and volunteer registration
- Admin login and dashboard pages for managing submitted data
- REST-style API routes for problems, volunteers, dashboard data, and chatbot support
- MongoDB Atlas persistence through PyMongo
- Volunteer matching score based on location, skills, severity, and availability
- Problem type pie chart and area-wise bar chart
- Gemini chatbot that answers questions about how the application works

## Folder Structure

```txt
VolunteerMatcher/
|-- app.py
|-- requirements.txt
|-- render.yaml
|-- .env.example
|-- config/
|-- models/
|-- routes/
|-- services/
|-- utils/
|-- templates/
`-- static/
```

## MongoDB Collections

### problems

```json
{
  "_id": "ObjectId",
  "location": "Mumbai",
  "problemType": "water",
  "severity": 4,
  "description": "No clean drinking water nearby.",
  "availability": "weekends",
  "workDate": "2026-05-10",
  "status": "open",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

### volunteers

```json
{
  "_id": "ObjectId",
  "name": "Rahul Sharma",
  "skills": ["water", "health"],
  "preferredLocation": "Mumbai",
  "availability": "weekends",
  "availableDate": "2026-05-10",
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
Availability match   +20
Date match           +30
Anytime availability +10
```

The app sorts volunteers by score and returns the top 3.

## Run Locally

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file from `.env.example`:

```powershell
Copy-Item .env.example .env
```

4. Update `.env` with your MongoDB Atlas connection string, admin credentials, and Gemini API key.

5. Start the app:

```powershell
flask --app app run
```

6. Open:

```txt
http://127.0.0.1:5000
```

## Deploy on Render Free Tier

1. Push this repository to GitHub.
2. Create a free MongoDB Atlas cluster and copy its connection string.
3. In MongoDB Atlas, create a database user and allow network access from Render. For a beginner demo, `0.0.0.0/0` is the simplest option; use a strong database password.
4. Create a new Render Web Service.
5. Connect the GitHub repository: `Aryan1771/VolunteerMatcher`.
6. Use these settings:

```txt
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

7. Add environment variables:

```txt
MONGO_URI=your-mongodb-atlas-connection-string
MONGO_DB_NAME=volunteer_matcher
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-strong-admin-password
SECRET_KEY=your-long-random-secret
GEMINI_API_KEY=your-google-ai-studio-api-key
GEMINI_MODEL=gemini-2.5-flash
FLASK_ENV=production
```

8. Deploy the service and open the Render URL.

## Database Alternatives

The current code is configured for MongoDB Atlas because it works well with Render free deployments and the existing PyMongo data layer.

| Database | Best For | Notes |
| --- | --- | --- |
| MongoDB Atlas | Recommended for this version | Cloud hosted, free tier available, works with the current code. |
| Render PostgreSQL | SQL-based Render deployment | Requires replacing PyMongo with SQLAlchemy or psycopg and rewriting queries. |
| Supabase PostgreSQL | Hosted PostgreSQL with a generous free tier | Requires a SQL schema and query rewrite. |
| Firebase Firestore | Google-based NoSQL | Requires replacing the MongoDB helper and query code; best if moving the whole app to Google Cloud Run. |
| SQLite | Local demo only | Easy for learning, but not reliable for Render free production data. |

For the fastest working website, keep MongoDB Atlas. For a Google-only stack, use Firestore and deploy on Cloud Run instead of Render.

## Notes

- `MONGO_URI` is required for forms, APIs, and dashboard data.
- Admin credentials are stored in environment variables for simplicity.
- The existing GPLv3 license is preserved.
