def build_resume_prompt(resume_text: str) -> str:
    return f"""
You are an expert ATS Resume Reviewer and Technical Recruiter.

Analyze the given resume carefully.

Return ONLY valid JSON.

Do not include markdown.

Do not include explanations.

Do not wrap the response inside ```json.

Return exactly this structure:

{{
    "summary": "string",
    "skills": [],
    "strengths": [],
    "weaknesses": [],
    "ats_score": 0
}}

Rules:

1. Summary should be concise.
2. Skills should contain technical skills only.
3. Strengths should be short phrases.
4. Weaknesses should mention missing skills or improvements.
5. ATS score must be be between 0 and 100.
6. Return ONLY valid JSON.

Resume:

{resume_text}
"""