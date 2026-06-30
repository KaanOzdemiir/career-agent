import json
from pathlib import Path
from typing import Any

import yaml

from src.models import CareerProfile


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def create_profile_if_missing(path: Path, career_profile: CareerProfile) -> None:
    if path.exists():
        return

    profile = {
        "career_preferences": {
            "preferred_roles": career_profile.preferred_roles,
            "preferred_countries": ["Germany", "Netherlands", "UK"],
            "remote": career_profile.remote,
            "hybrid": career_profile.hybrid,
            "onsite": career_profile.onsite,
            "minimum_salary_eur": None,
        },
        "application_preferences": {
            "generate_cover_letter": True,
            "require_human_approval": True,
        },
        "job_filters": {
            "min_score": 75,
            "exclude_keywords": [
                "security clearance",
            ],
        },
        "ai_memory": {
            "companies_applied": [],
            "companies_rejected": [],
            "blacklist": [],
            "favorite_companies": [],
        },
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.dump(profile, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
