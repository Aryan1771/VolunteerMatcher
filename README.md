# Smart Volunteer Matching System

A beginner-friendly Flask web application that collects local problem reports, registers volunteers, matches volunteers to problems with a simple scoring algorithm, and shows admin insights with Chart.js.

## Tech Stack

- Python Flask
- MongoDB Atlas
- HTML, CSS, and JavaScript
- Tailwind CSS CDN
- Chart.js CDN
- Render free web service

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
├── render.yaml
├── .env.example
├── config/
├── models/
├── routes/
├── services/
├── utils/
├── templates/
└── static/
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

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file from `.env.example`:

```bash
copy .env.example .env
```

4. Update `.env` with your MongoDB Atlas connection string and admin credentials.

5. Start the app:

```bash
flask --app app run
```

6. Open:

```txt
http://127.0.0.1:5000
```

## Deploy on Render Free Tier

1. Push this repository to GitHub.
2. Create a new Render Web Service.
3. Connect the GitHub repository.
4. Use these settings:

```txt
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

5. Add environment variables:

```txt
MONGO_URI
MONGO_DB_NAME
ADMIN_USERNAME
ADMIN_PASSWORD
SECRET_KEY
GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash
FLASK_ENV=production
```

6. Deploy the service.

## Notes

- `MONGO_URI` is required for forms, APIs, and dashboard data.
- Admin credentials are stored in environment variables for simplicity.
- The existing GPLv3 license is preserved.
