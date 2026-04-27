from flask import Blueprint, request

from services.gemini_service import ask_gemini
from utils.response_helpers import error_response, success_response
from utils.validators import clean_text


chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/api/chatbot")


@chatbot_bp.post("/message")
def send_chatbot_message():
    payload = request.get_json(silent=True) or {}
    message = clean_text(payload.get("message"))

    if not message:
        return error_response("Please enter a message.", 400)

    if len(message) > 1000:
        return error_response("Please keep your message under 1000 characters.", 400)

    try:
        reply = ask_gemini(message)
        return success_response(data={"reply": reply})
    except RuntimeError as exc:
        return error_response(str(exc), 500)
