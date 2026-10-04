def build_resume_analysis_prompt(resume_text: str) -> str:
    return f"""
You are an expert AI Technical Recruiter and ATS (Applicant Tracking System) Review Specialist.
Carefully parse and evaluate the candidate resume provided below.

You MUST return a single, valid JSON object without any surrounding markdown code blocks, backticks, or extra text.

JSON Schema to follow exactly:
{{
    "summary": "Concise 2-3 sentence executive profile of the candidate.",
    "skills": ["Python", "Django", "PostgreSQL", "Docker"],
    "soft_skills": ["Leadership", "Communication", "Problem Solving"],
    "strengths": ["Strong backend experience", "Demonstrated cloud deployment"],
    "weaknesses": ["Limited unit testing mentioned", "No CI/CD pipeline detail"],
    "ats_score": 82,
    "suggested_roles": ["Full Stack Engineer", "Backend Developer", "Python Engineer"],
    "missing_keywords": ["Kubernetes", "Redis", "TDD", "REST APIs"]
}}

Rules:
1. `ats_score` MUST be an integer between 0 and 100 based on standard industry criteria.
2. `skills` must contain verified technical skills found in the text.
3. `strengths` and `weaknesses` should be concise, highly actionable bullet points.
4. Output ONLY valid parseable JSON.

Candidate Resume Text:
{resume_text}
"""


def build_question_generation_prompt(
    role_title: str,
    difficulty: str,
    interview_type: str,
    resume_summary_or_skills: str,
    count: int = 5,
) -> str:
    return f"""
You are a Lead Hiring Manager and Technical Interviewer conducting a realistic job interview.
Generate a structured set of {count} high-quality interview questions tailored for the specified candidate and target position.

Target Role: {role_title}
Difficulty Level: {difficulty} (Entry-Level, Mid-Level, Senior, or Lead)
Interview Type: {interview_type} (Technical, Behavioral, Mixed, or System Design)
Candidate Background / Skills:
{resume_summary_or_skills or 'Standard background for the specified role'}

You MUST return a single, valid JSON object containing a "questions" array.
Do not wrap in markdown quotes or extra text.

JSON Schema to follow:
{{
    "questions": [
        {{
            "order": 1,
            "category": "TECHNICAL",
            "question_text": "Explain how you handle database connection pooling and concurrency in high-traffic applications.",
            "expected_key_points": [
                "Connection pool sizing",
                "Deadlock prevention",
                "ORM vs raw connection efficiency"
            ]
        }}
    ]
}}

Rules:
1. Generate exactly {count} questions arranged progressively from warm-up to in-depth questions.
2. Categories can be "TECHNICAL", "BEHAVIORAL", "SITUATIONAL", or "SYSTEM_DESIGN".
3. Tailor the depth strictly to the {difficulty} level.
4. Output ONLY valid parseable JSON.
"""


def build_answer_evaluation_prompt(
    role_title: str,
    difficulty: str,
    question_text: str,
    category: str,
    expected_key_points: list,
    candidate_answer: str,
) -> str:
    key_points_str = "\n- ".join(expected_key_points) if expected_key_points else "General best practices"
    return f"""
You are an expert AI Interview Assessor and Hiring Manager.
Evaluate the candidate's response to the interview question below.

Role: {role_title} ({difficulty})
Question ({category}): {question_text}
Expected Key Points:
- {key_points_str}

Candidate Answer:
\"\"\"{candidate_answer}\"\"\"

You MUST return a single, valid JSON object without markdown code blocks around the JSON.

JSON Schema:
{{
    "technical_score": 85,
    "clarity_score": 90,
    "relevance_score": 80,
    "overall_score": 85,
    "strengths": [
        "Clearly explained core concepts",
        "Gave concrete architectural examples"
    ],
    "improvements": [
        "Could mention failure recovery strategies",
        "Be more concise on introductory points"
    ],
    "ai_feedback": "Structured constructive feedback on the response...",
    "ideal_answer": "### Architecture & Core Approach\\nExplain the high level architecture with clear separation...\\n\\n### Key Implementation Steps\\n1. **Step 1**: Details...\\n2. **Step 2**: Details...\\n\\n### Production & Scaling Considerations\\n- **Fault tolerance**: Details...\\n- **Performance**: Details..."
}}

Formatting Rules for `ideal_answer`:
1. Use clear Markdown headings (e.g. `### High-Level Approach`, `### Key Steps`, `### Trade-offs & Production Considerations`).
2. Separate distinct concepts with bullet points and numbered lists.
3. Use bold tags `**term**` for key terminology.
4. Ensure line breaks (`\\n\\n`) between all sections so the output is readable and structured.
5. All scores must be integers between 0 and 100.
6. Output ONLY valid parseable JSON.
"""


def build_final_summary_prompt(
    role_title: str,
    difficulty: str,
    qna_records: list,
) -> str:
    qna_text = ""
    for idx, item in enumerate(qna_records, 1):
        qna_text += f"\nQ{idx} [{item.get('category')}]: {item.get('question')}\n"
        qna_text += f"Answer: {item.get('answer')}\n"
        qna_text += f"Score: {item.get('score')}/100\n"

    return f"""
You are the Head of Engineering and Interview Committee Chair.
Synthesize the full interview session results for a candidate applying for {role_title} ({difficulty}).

Interview Transcript & Individual Evaluations:
{qna_text}

You MUST return a single, valid JSON object without markdown fences.

JSON Schema:
{{
    "overall_score": 82.5,
    "readiness_rating": "Strong Mid-Level / Ready for Next Round",
    "technical_mastery": 80,
    "communication_clarity": 85,
    "problem_solving": 82,
    "key_takeaways": [
        "Strong fundamentals in system design and data models",
        "Communicates trade-offs articulately"
    ],
    "actionable_recommendations": [
        "Review distributed caching strategies",
        "Deepen knowledge in edge-case failure modes"
    ],
    "detailed_summary": "The candidate performed solidly across both technical and behavioral aspects..."
}}

Rules:
1. All numerical scores must be 0-100.
2. Output ONLY valid parseable JSON.
"""
