import json
from pathlib import Path

PROFILE_PATH = Path("data/profile/user_profile.json")
PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _ensure_file():
    if not PROFILE_PATH.exists():
        default_profile = {
            "desired_salary": "",
            "visa_status": "",
            "worked_here_before": "",
            "has_referral": "",
            "notice_period": "",
            "relocation": "",
            "driver_license": "",
            "gender": "",
            "ethnicity": "",
            "disability_status": "",
            "medical_status": ""
        }
        PROFILE_PATH.write_text(
            json.dumps(default_profile, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )


def load_profile():
    _ensure_file()
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_profile(profile_data: dict):
    _ensure_file()
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=2, ensure_ascii=False)


def get_profile_value(key: str, default: str = "") -> str:
    profile = load_profile()
    return profile.get(key, default)


def get_default_profile():
    _ensure_file()
    return load_profile()