from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RESUME_DIR = BASE_DIR / "resume"
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"

RESUME_TEXT_PATH = DATA_DIR / "resume_text.txt"
CANDIDATE_PATH = DATA_DIR / "candidate.json"
PROFILE_PATH = CONFIG_DIR / "profile.yml"