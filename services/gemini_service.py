import json
import os
import urllib.error
import urllib.parse
import urllib.request


SYSTEM_INSTRUCTION = """
You are the help chatbot for the Smart Volunteer Matching System.
Explain the app in simple language and help users report problems,
register as volunteers, understand admin dashboard data, and understand
how volunteer matching scores work. Keep answers short, friendly, and
focused on this application.
"""


def ask_gemini(message):
    """Send a short help question to Gemini without exposing the API key."""
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    encoded_model = urllib.parse.quote(model, safe="")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{encoded_model}:generateContent?key={api_key}"

    payload = {
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION.strip()}],
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": message}],
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 300,
        },
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        raise RuntimeError(f"Gemini API error: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach Gemini API: {exc.reason}") from exc

    parts = (
        response_data.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [])
    )

    reply = " ".join(part.get("text", "") for part in parts).strip()
    if not reply:
        raise RuntimeError("Gemini did not return a text response.")

    return reply
