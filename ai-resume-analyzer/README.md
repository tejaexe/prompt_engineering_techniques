# AI Resume Analyzer & Job Matcher

A Flask application for analyzing a PDF/DOCX resume against a job description. It uses structured prompting and the Mistral API to return a transparent match score, skill gaps, resume suggestions, interview questions, a cover-letter draft, and a downloadable PDF report.

## Assignment coverage

- Resume upload and text extraction: PDF via PyMuPDF; DOCX via python-docx
- Role-based, few-shot, template, prompt-chaining, iterative, negative, and JSON-output prompt design
- Mistral JSON mode plus Python validation before results are displayed
- Explicit anti-fabrication instruction: unsupported qualifications are reported as missing, not invented
- Match explanation, skill gaps, resume improvement guidance, interview preparation, cover letter, and PDF report

## Setup

Requires Python 3.9+.

```bash
cd ai-resume-analyzer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and add your Mistral API key:

```text
MISTRAL_API_KEY=your_key_here
MISTRAL_MODEL=mistral-small-latest
FLASK_SECRET_KEY=replace-with-a-long-random-value
```

Run the app:

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Demo mode

If `MISTRAL_API_KEY` is blank, the app still runs using a local keyword-matching demo. The interface labels this mode clearly; it is useful for testing uploads and the report flow but does not represent AI analysis.

## Prompt design

The app's prompt is in `services/prompt_templates.py`. It combines:

1. **Role-based prompting** - professional resume reviewer and fair job-match analyst.
2. **Few-shot prompting** - a short Python/SQL example clarifies how matches and gaps work.
3. **Negative prompting** - explicitly prohibits inventing qualifications.
4. **Template prompting** - injects delimited resume and job-description inputs.
5. **JSON output prompting** - defines the required response structure.
6. **Prompt chaining** - document extraction -> LLM analysis -> JSON validation -> results/report.

## Test data

Upload [sample_resume_aarav_sharma.docx](sample-data/sample_resume_aarav_sharma.docx), then paste [sample_job_description.txt](sample-data/sample_job_description.txt) into the job-description field. The resume is fictional and is safe for testing. Do not commit real personal resumes or API keys.

## Limitations and responsible use

- The match score is an assistive estimate, never an automated hiring decision.
- Human review is required. The application should not be used to exclude candidates.
- Results depend on the text extractable from the uploaded document and the quality of the job description.
- Review generated cover letters before use.

## Project structure

```text
ai-resume-analyzer/
├── app.py
├── services/
│   ├── analysis_service.py
│   ├── prompt_templates.py
│   ├── report_service.py
│   └── resume_parser.py
├── templates/
├── static/css/
├── sample-data/
├── requirements.txt
└── .env.example
```
