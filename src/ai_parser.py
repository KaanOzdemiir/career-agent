import json

import requests
from pydantic import ValidationError

from src.models import Candidate, CareerProfile


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"


CANDIDATE_PROMPT = """
You extract objective candidate data from resumes.

Return only valid JSON.
Do not use markdown.
Do not wrap the output in ```json.

Rules:
- Only extract facts supported by the resume.
- Do not invent missing information.
- Use null for unknown scalar values.
- Use empty arrays for unknown list values.
- current_title should come from the most recent job.
- current_company should come from the most recent job.
- companies should include every company found in the work experience.
- Return companies as an array of strings.
- previous_titles should include older titles, not the current title.
- total_years_experience may be estimated from resume dates.
- primary_role_family should be a short objective label.
- domains should include all professional/technical/product/business domains represented across the full resume.
- industries should include all industries represented across the full resume.
- keywords should include strong ATS/search keywords found or clearly supported by the resume.

JSON schema:
{
  "personal": {
    "full_name": null,
    "email": null,
    "phone": null,
    "location": null,
    "country": null,
    "linkedin": null,
    "github": null,
    "website": null
  },
  "headline": null,
  "summary": null,
  "current_title": null,
  "current_company": null,
  "total_years_experience": null,
  "primary_role_family": null,
  "companies": [],
  "previous_titles": [],
  "programming_languages": [],
  "frameworks": [],
  "tools": [],
  "keywords": [],
  "domains": [],
  "industries": [],
  "experience": [],
  "education": [],
  "projects": [],
  "certifications": [],
  "languages": []
}
"""


CAREER_PROFILE_PROMPT = """
You create job search preferences from a structured candidate profile.

Return only valid JSON.
Do not use markdown.
Do not wrap the output in ```json.

Rules:
- Suggest realistic role titles based only on the candidate profile.
- Derive roles from current_title, previous_titles, primary_role_family, domains, industries, skills, tools, and experience.
- Keep role suggestions aligned with the candidate's actual specialization.
- Keep seniority aligned with the candidate's experience level.
- Include multiple role title variants recruiters and job boards commonly use.
- Prefer specific role titles over generic ones.
- Do not suggest broad or unrelated roles unless the candidate profile clearly supports them.
- Do not suggest unrelated career changes.
- preferred_countries must be exactly: ["Germany", "Netherlands", "UK"].
- minimum_salary_eur must be null unless salary expectations are explicitly available.

JSON schema:
{
  "preferred_roles": [],
  "preferred_countries": ["Germany", "Netherlands", "UK"],
  "remote": true,
  "hybrid": true,
  "onsite": false,
  "minimum_salary_eur": null
}
"""


def extract_json(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("The model did not return valid JSON.")

    return json.loads(text[start : end + 1])


def call_ollama(prompt: str) -> dict:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        },
        timeout=180,
    )

    response.raise_for_status()
    return extract_json(response.json()["response"])


def normalize_candidate_data(data: dict) -> dict:
    companies = data.get("companies", [])
    data["companies"] = normalize_string_list(companies)

    languages = data.get("languages", [])
    data["languages"] = normalize_language_list(languages)

    return data


def normalize_string_list(items: list) -> list[str]:
    normalized = []

    for item in items:
        if isinstance(item, str):
            normalized.append(item)
        elif isinstance(item, dict):
            value = item.get("name") or item.get("company") or item.get("value")
            if value:
                normalized.append(value)

    return normalized


def normalize_language_list(items: list) -> list[dict]:
    normalized = []

    for item in items:
        if isinstance(item, str):
            normalized.append(
                {
                    "language": item,
                    "proficiency": None,
                }
            )
        elif isinstance(item, dict):
            normalized.append(item)

    return normalized


def create_candidate_from_resume(resume_text: str) -> Candidate:
    prompt = f"{CANDIDATE_PROMPT}\n\nResume:\n{resume_text}"
    data = normalize_candidate_data(call_ollama(prompt))

    try:
        return Candidate.model_validate(data)
    except ValidationError as error:
        raise ValueError(
            f"Model output does not match Candidate schema: {error}"
        ) from error


def create_career_profile(candidate: Candidate) -> CareerProfile:
    candidate_json = json.dumps(
        candidate.model_dump(),
        ensure_ascii=False,
        indent=2,
    )

    prompt = f"{CAREER_PROFILE_PROMPT}\n\nCandidate profile:\n{candidate_json}"
    data = call_ollama(prompt)

    try:
        return CareerProfile.model_validate(data)
    except ValidationError as error:
        raise ValueError(
            f"Model output does not match CareerProfile schema: {error}"
        ) from error