# Prompt Engineering Techniques: Practical Examples

A concise reference project showing nine common prompting techniques, their use cases, and ready-to-adapt examples.

## Goal

Use these patterns to make requests clearer, more consistent, and easier to evaluate. A technique is a tool, not a guarantee: validate important outputs, especially when they affect production systems or people.

## Techniques

### 1. Zero-shot prompting

**Use it for:** Testing a model's baseline knowledge without examples or detailed guidance.

```text
Explain the difference between a REST API and GraphQL in three simple bullet points for a beginner.
```

### 2. Few-shot prompting

**Use it for:** Teaching a specific pattern through examples.

```text
Convert the following requirements into user stories.

Requirement: User wants to log in
Story: As a user, I want to log in so that I can access my dashboard.

Requirement: User wants to reset a password
Story: As a user, I want to reset my password so that I can regain account access.

Requirement: User wants to upload a profile picture
Story:
```

### 3. Structured-reasoning prompting

**Use it for:** Comparing technical options against explicit decision criteria.

```text
I need to choose PostgreSQL or MongoDB for a new e-commerce application with
complex relationships among users, orders, and products.

Evaluate the decision in this order:
1. Data structure and relationships
2. ACID and transactional requirements
3. Scalability and operational trade-offs

Then recommend one option and give a concise rationale.
```

### 4. Role-based prompting

**Use it for:** Setting the perspective, tone, and depth of a review.

```text
Act as a senior technical interviewer. I will provide a candidate's answer to a
coding question. Critique its time and space complexity, identify any correctness
risks, and ask one challenging follow-up question that tests depth.
```

### 5. Iterative prompting

**Use it for:** Improving a draft over several focused rounds.

```text
Round 1: Write a Python function that fetches data from a website.

Round 2: Rewrite it to handle pagination and use asynchronous requests with aiohttp.

Round 3: Add robust handling for timeouts, 404 responses, and 500 responses.
```

Only fetch sites you are authorized to access, and follow their terms and rate limits.

### 6. Prompt chaining

**Use it for:** Breaking a workflow into smaller, dependent stages.

```text
Step 1: Summarize this resume as a list of the candidate's five strongest technical skills.

Step 2: Using only the five skills listed above, suggest three specific job roles
the candidate may be qualified for. Briefly explain each match.
```

Pass the output of Step 1 into Step 2. Review intermediate outputs before continuing when accuracy matters.

### 7. Negative prompting

**Use it for:** Excluding unwanted language, topics, or styles.

```text
Write a cover letter for a frontend developer role.

Do not use phrases such as "passionate professional" or "hard-working".
Do not mention my GPA.
Avoid overly formal corporate jargon.
```

### 8. Template prompting

**Use it for:** Reusing one prompt while swapping variables.

```text
Act as a {role}. Explain {topic} to {audience} in a {output_format} style.
Difficulty level: {difficulty}.
```

Example variables:

```text
role: science teacher
topic: photosynthesis
audience: 10-year-old students
output_format: short story
difficulty: beginner
```

### 9. JSON-output prompting

**Use it for:** Returning data that a program can parse.

```text
Analyze the job description between <job_description> tags.

Return valid JSON only, using this schema:
{
  "job_title": "string or null",
  "required_skills": ["string"],
  "years_experience": "string or null",
  "salary_range": "string or null"
}

Use null when a value is not stated. Do not infer missing details.

<job_description>
[Insert job description here]
</job_description>
```

## Quick selection guide

| If you need to... | Try... |
| --- | --- |
| Ask a straightforward question | Zero-shot |
| Match an example or style | Few-shot |
| Compare choices with clear criteria | Structured reasoning |
| Change voice or expertise | Role-based |
| Improve a result incrementally | Iterative |
| Build a multi-stage workflow | Prompt chaining |
| Prevent unwanted content or style | Negative prompting |
| Reuse one pattern with variables | Template prompting |
| Feed output into software | JSON output |

## Notes

- Delimit any untrusted source material, as shown with `<job_description>`.
- State the expected output format and any constraints near the end of a prompt.
- Ask for concise reasoning or a decision summary when you need explainability; do not rely on hidden reasoning as proof of correctness.
- For JSON, validate the response in your application before using it.

## License

This project is available under the [MIT License](LICENSE).
