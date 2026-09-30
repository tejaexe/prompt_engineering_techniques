import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from services.analysis_service import analyze_resume
from services.report_service import create_report


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY", "development-only-change-me"),
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,
        UPLOAD_FOLDER=BASE_DIR / "uploads",
        MISTRAL_API_KEY=os.getenv("MISTRAL_API_KEY", ""),
        MISTRAL_MODEL=os.getenv("MISTRAL_MODEL", "mistral-small-latest"),
    )
    app.config["UPLOAD_FOLDER"].mkdir(exist_ok=True)

    @app.get("/")
    def index():
        from flask import render_template
        return render_template("index.html", api_ready=bool(app.config["MISTRAL_API_KEY"]))

    @app.post("/analyze")
    def analyze():
        from flask import flash, redirect, render_template, request, url_for
        from services.resume_parser import extract_text

        resume = request.files.get("resume")
        job_description = request.form.get("job_description", "").strip()
        if not resume or not resume.filename or not job_description:
            flash("Upload a resume and provide a job description.", "danger")
            return redirect(url_for("index"))

        try:
            resume_text = extract_text(resume)
            result = analyze_resume(
                resume_text=resume_text,
                job_description=job_description,
                api_key=app.config["MISTRAL_API_KEY"],
                model=app.config["MISTRAL_MODEL"],
            )
        except ValueError as error:
            flash(str(error), "danger")
            return redirect(url_for("index"))
        except Exception as error:
            app.logger.exception("Resume analysis failed")
            if "429" in str(error) or "rate limit" in str(error).lower():
                flash("Mistral is rate-limiting this API key. Wait a few minutes or temporarily use demo mode.", "warning")
            else:
                flash("Analysis could not be completed. Check your API key or try again.", "danger")
            return redirect(url_for("index"))

        return render_template(
            "results.html",
            result=result,
            resume_text=resume_text,
            job_description=job_description,
            demo_mode=not app.config["MISTRAL_API_KEY"],
        )

    @app.post("/report")
    def report():
        from flask import request, send_file
        import json
        from io import BytesIO

        result = json.loads(request.form["result"])
        report_bytes = create_report(result)
        return send_file(
            BytesIO(report_bytes),
            as_attachment=True,
            download_name="resume-match-report.pdf",
            mimetype="application/pdf",
        )

    @app.errorhandler(413)
    def too_large(_error):
        from flask import flash, redirect, url_for
        flash("The file is too large. The maximum upload size is 5 MB.", "danger")
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
