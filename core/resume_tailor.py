from pathlib import Path

from core.job_collector import load_jobs
from core.file_store import read_primary_resume_text, read_uploaded_cover_letter_text

GENERATED_RESUME_DIR = Path("data/generated/resumes")
GENERATED_COVER_LETTER_DIR = Path("data/generated/cover_letters")

GENERATED_RESUME_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_COVER_LETTER_DIR.mkdir(parents=True, exist_ok=True)


def get_job_by_id(job_id: str):
    jobs = load_jobs()
    for job in jobs:
        if job.id == job_id:
            return job
    return None


def get_resume_file_path(job_id: str) -> Path:
    return GENERATED_RESUME_DIR / f"{job_id}.txt"


def get_cover_letter_file_path(job_id: str) -> Path:
    return GENERATED_COVER_LETTER_DIR / f"{job_id}.txt"


def _truncate_text(text: str, max_chars: int = 4000) -> str:
    if not text:
        return ""
    return text[:max_chars].strip()


def get_default_resume_text(job_id: str) -> str:
    job = get_job_by_id(job_id)
    if not job:
        return ""

    uploaded_resume_text = read_primary_resume_text()
    uploaded_resume_text = _truncate_text(uploaded_resume_text, max_chars=5000)

    if not uploaded_resume_text:
        uploaded_resume_text = (
            "No uploaded resume content was found. Please upload at least one base resume."
        )

    return f"""Tailored Resume Draft for {job.title} at {job.company}

Target Role
- Title: {job.title}
- Company: {job.company}
- Location: {job.location}

Job Description Snapshot
{job.description}

Base Resume Content
{uploaded_resume_text}

Draft Notes
- This draft is currently based on the uploaded base resume.
- In the next version, bullet points can be rewritten more precisely to align with the job description.
- The goal is to preserve truthful experience while improving relevance to the role.

Suggested Positioning
- Highlight experience most relevant to {job.title}
- Emphasize analytical, operational, and stakeholder-facing work where applicable
- Reorder content so that the most relevant experience appears first
"""


def get_default_cover_letter_text(job_id: str) -> str:
    job = get_job_by_id(job_id)
    if not job:
        return ""

    uploaded_cover_letter_text = read_uploaded_cover_letter_text()
    uploaded_cover_letter_text = _truncate_text(uploaded_cover_letter_text, max_chars=3500)

    if not uploaded_cover_letter_text:
        uploaded_cover_letter_text = (
            "No uploaded base cover letter content was found. Please upload a base cover letter."
        )

    return f"""Cover Letter Draft for {job.title} at {job.company}

Target Role
- Title: {job.title}
- Company: {job.company}
- Location: {job.location}

Job Description Snapshot
{job.description}

Base Cover Letter Content
{uploaded_cover_letter_text}

Draft Notes
- This draft is currently based on the uploaded base cover letter.
- In the next version, the wording can be rewritten more precisely for the target company and job description.
- The final version should reflect truthful experience and role-specific motivation.
"""


def load_saved_resume(job_id: str) -> str:
    file_path = get_resume_file_path(job_id)
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")

    return get_default_resume_text(job_id)


def load_saved_cover_letter(job_id: str) -> str:
    file_path = get_cover_letter_file_path(job_id)
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")

    return get_default_cover_letter_text(job_id)


def save_resume_text(job_id: str, content: str):
    file_path = get_resume_file_path(job_id)
    file_path.write_text(content, encoding="utf-8")


def save_cover_letter_text(job_id: str, content: str):
    file_path = get_cover_letter_file_path(job_id)
    file_path.write_text(content, encoding="utf-8")