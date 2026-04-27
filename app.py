import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

from routes.auth_routes import auth_bp, is_admin_logged_in
from routes.chatbot_routes import chatbot_bp
from routes.dashboard_routes import dashboard_bp
from routes.problem_routes import problem_bp
from routes.volunteer_routes import volunteer_bp
from utils.response_helpers import error_response


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "local-dev-secret-key")

app.register_blueprint(auth_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(problem_bp)
app.register_blueprint(volunteer_bp)
app.register_blueprint(dashboard_bp)


@app.get("/")
def home_page():
    return render_template("index.html")


@app.get("/report-problem")
def report_problem_page():
    return render_template("report_problem.html")


@app.get("/register-volunteer")
def register_volunteer_page():
    return render_template("register_volunteer.html")


@app.get("/admin/login")
def admin_login_page():
    if is_admin_logged_in():
        return redirect(url_for("admin_dashboard_page"))

    return render_template("admin_login.html")


@app.get("/admin/dashboard")
def admin_dashboard_page():
    if not is_admin_logged_in():
        return redirect(url_for("admin_login_page"))

    return render_template("admin_dashboard.html", admin_username=session.get("admin_username"))


@app.get("/admin/logout")
def admin_logout_page():
    session.clear()
    return redirect(url_for("admin_login_page"))


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api"):
        return error_response("API endpoint not found.", 404)

    return render_template("base.html", page_title="Page not found", content_title="Page not found"), 404


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_ENV") != "production")
