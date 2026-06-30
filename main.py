from rich import print

from src.ai_parser import create_candidate_from_resume, create_career_profile
from src.config import CANDIDATE_PATH, PROFILE_PATH, RESUME_TEXT_PATH
from src.resume_reader import load_resume
from src.storage import create_profile_if_missing, write_json, write_text


def main():
    print("[bold]Reading resume...[/bold]")
    resume_text = load_resume()
    write_text(RESUME_TEXT_PATH, resume_text)

    print("[bold]Creating candidate profile...[/bold]")
    candidate = create_candidate_from_resume(resume_text)
    write_json(CANDIDATE_PATH, candidate.model_dump())

    print("[bold]Creating job search preferences...[/bold]")
    career_profile = create_career_profile(candidate)
    create_profile_if_missing(PROFILE_PATH, career_profile)

    print("[green]Done.[/green]")
    print()
    print(f"Candidate: {CANDIDATE_PATH}")
    print(f"Profile:   {PROFILE_PATH}")
    print(f"Resume:    {RESUME_TEXT_PATH}")


if __name__ == "__main__":
    main()