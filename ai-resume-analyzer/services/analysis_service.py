import json
import re

from services.prompt_templates import build_analysis_prompt


REQUIRED_KEYS = {
    "candidate_summary", "detected_skills", "job_required_skills", "matched_skills",
    "skill_gaps", "match_score", "score_explanation", "resume_improvements",
    "interview_questions", "cover_letter", "missing_information",
}


def analyze_resume(resume_text: str, job_description: str, api_key: str, model: str) -> dict:
    if api_key:
        result = _analyze_with_mistral(resume_text, job_description, api_key, model)
    else:
        result = _demo_analysis(resume_text, job_description)
    return validate_result(result)


def _analyze_with_mistral(resume_text: str, job_description: str, api_key: str, model: str) -> dict:
    from mistralai import Mistral

    client = Mistral(api_key=api_key)
    response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": build_analysis_prompt(resume_text, job_description)}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def validate_result(result: dict) -> dict:
    missing = REQUIRED_KEYS - set(result)
    if missing:
        raise ValueError(f"The AI response was incomplete; missing: {', '.join(sorted(missing))}.")
    score = result.get("match_score")
    if not isinstance(score, (int, float)) or not 0 <= score <= 100:
        raise ValueError("The AI response contained an invalid match score.")
    for key in REQUIRED_KEYS - {"match_score", "candidate_summary", "score_explanation", "cover_letter"}:
        if not isinstance(result[key], list):
            raise ValueError(f"The AI response contained an invalid {key} field.")
    return result


def _demo_analysis(resume_text: str, job_description: str) -> dict:
    """A transparent local fallback for demonstrations; it does not claim AI analysis."""
    tokens = lambda text: set(re.findall(r"[a-zA-Z][a-zA-Z+#]*", text.lower()))
    resume_tokens, job_tokens = tokens(resume_text), tokens(job_description)
    known_skills = ["python", "flask", "sql", "javascript", "html", "css", "react", "git", "docker", "aws", "excel", "pandas", "mongodb"]
    detected = [skill for skill in known_skills if skill in resume_tokens]
    required = [skill for skill in known_skills if skill in job_tokens]
    matched = [skill for skill in required if skill in detected]
    gaps = [skill for skill in required if skill not in detected]
    score = round((len(matched) / len(required) * 100) if required else 0)
    return {
        "candidate_summary": "Demo-mode summary based on direct keyword matches only. Configure MISTRAL_API_KEY for AI analysis.",
        "detected_skills": detected,
        "job_required_skills": required,
        "matched_skills": matched,
        "skill_gaps": gaps,
        "match_score": score,
        "score_explanation": "The demo score is the percentage of recognized job keywords found in the resume; it is not a hiring assessment.",
        "resume_improvements": ["Add measurable project outcomes where supported by your experience.", "Name relevant tools only when you have used them."],
        "interview_questions": ["Describe a project that best demonstrates your relevant skills.", "How would you approach the main responsibilities in this role?"],
        "cover_letter": "Demo mode does not generate a personalized cover letter. Add a Mistral API key to use this feature.",
        "missing_information": ["Demo mode cannot reliably infer education, experience duration, or project impact."],
    }
