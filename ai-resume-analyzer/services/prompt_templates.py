import json


ANALYSIS_SCHEMA = {
    "candidate_summary": "string",
    "detected_skills": ["string"],
    "job_required_skills": ["string"],
    "matched_skills": ["string"],
    "skill_gaps": ["string"],
    "match_score": 0,
    "score_explanation": "string",
    "resume_improvements": ["string"],
    "interview_questions": ["string"],
    "cover_letter": "string",
    "missing_information": ["string"],
}


def build_analysis_prompt(resume_text: str, job_description: str) -> str:
    """Role, constraints, a tiny example, and a strict JSON contract."""
    return f"""
You are a professional resume reviewer and fair job-match analyst.

Analyze only the evidence in the resume and job description. Never invent skills,
degrees, employers, dates, achievements, or qualifications. If information is absent,
put it in missing_information. A match score is an estimate, not a hiring decision.

Example: if a job requires Python and SQL, and the resume explicitly lists Python
but never mentions SQL, include Python in matched_skills and SQL in skill_gaps.

Return a valid JSON object only. Follow this schema exactly:
{json.dumps(ANALYSIS_SCHEMA, indent=2)}

<resume>
{resume_text}
</resume>

<job_description>
{job_description}
</job_description>
""".strip()
