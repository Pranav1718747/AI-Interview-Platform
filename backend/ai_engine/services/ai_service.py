import json
import logging
import re
import requests
from django.conf import settings
from .prompt_service import (
    build_resume_analysis_prompt,
    build_question_generation_prompt,
    build_answer_evaluation_prompt,
    build_final_summary_prompt,
)

logger = logging.getLogger(__name__)


def clean_json_response(raw_text: str) -> dict:
    """
    Cleans markdown formatting and parses JSON strictly.
    """
    cleaned = raw_text.strip()
    # Remove markdown code blocks if present
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try finding JSON block inside text
        match = re.search(r"(\{.*\}|\[.*\])", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        raise ValueError(f"LLM returned non-JSON output: {raw_text[:250]}")


def call_llm(prompt: str) -> dict:
    """
    Calls OpenRouter API directly.
    No fallback data or mock responses. If the API or key fails, raises an explicit error.
    """
    api_key = getattr(settings, "OPENROUTER_API_KEY", None)
    model = getattr(settings, "OPENROUTER_MODEL", "google/gemini-2.5-flash")

    if not api_key or api_key.strip() in ["", "your-openrouter-api-key-here"]:
        raise ValueError("OPENROUTER_API_KEY is not configured. Please set your key in backend/.env")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-interview-platform.local",
        "X-Title": "AI-Interview-Platform",
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a specialized AI Interviewer and ATS Resume Intelligence engine. Always respond in valid JSON matching the requested schema.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 1500,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
    except requests.exceptions.Timeout:
        raise RuntimeError("OpenRouter LLM request timed out after 60 seconds.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Unable to connect to OpenRouter API. Please check your network connection.")
    except Exception as e:
        raise RuntimeError(f"Network error calling OpenRouter LLM: {str(e)}")

    if not response.ok:
        try:
            err_json = response.json()
            err_msg = err_json.get("error", {}).get("message", response.text)
        except Exception:
            err_msg = response.text
        raise RuntimeError(f"OpenRouter LLM Error ({response.status_code}): {err_msg}")

    try:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected response structure from OpenRouter: {response.text[:200]}")

    return clean_json_response(content)


def analyze_resume(resume_text: str) -> dict:
    """
    Analyzes resume text using OpenRouter AI directly.
    """
    if not resume_text or len(resume_text.strip()) < 20:
        raise ValueError("Resume text is empty or too short to analyze.")

    prompt = build_resume_analysis_prompt(resume_text)
    return call_llm(prompt)


def generate_interview_questions(
    role_title: str,
    difficulty: str = "MID",
    interview_type: str = "MIXED",
    resume_skills_or_text: str = "",
    count: int = 5,
) -> list:
    """
    Generates tailored interview questions directly via OpenRouter AI.
    """
    prompt = build_question_generation_prompt(
        role_title=role_title,
        difficulty=difficulty,
        interview_type=interview_type,
        resume_summary_or_skills=resume_skills_or_text,
        count=count,
    )
    result = call_llm(prompt)
    questions = result.get("questions", [])
    if not questions:
        raise RuntimeError("LLM did not return a valid list of questions.")
    return questions


def evaluate_interview_answer(
    role_title: str,
    difficulty: str,
    question_text: str,
    category: str,
    expected_key_points: list,
    candidate_answer: str,
) -> dict:
    """
    Evaluates candidate's answer directly via OpenRouter AI.
    """
    prompt = build_answer_evaluation_prompt(
        role_title=role_title,
        difficulty=difficulty,
        question_text=question_text,
        category=category,
        expected_key_points=expected_key_points,
        candidate_answer=candidate_answer,
    )
    return call_llm(prompt)


def generate_interview_summary(
    role_title: str,
    difficulty: str,
    qna_records: list,
) -> dict:
    """
    Generates a full post-interview scorecard summary directly via OpenRouter AI.
    """
    if not qna_records:
        raise ValueError("Cannot generate interview summary without any answered questions.")

    prompt = build_final_summary_prompt(
        role_title=role_title,
        difficulty=difficulty,
        qna_records=qna_records,
    )
    return call_llm(prompt)