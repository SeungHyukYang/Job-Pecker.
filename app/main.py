from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List

from core.job_collector import load_jobs, load_decisions, save_decision
from core.resume_tailor import (
    get_job_by_id,
    load_saved_resume,
    save_resume_text,
    load_saved_cover_letter,
    save_cover_letter_text,
)
from core.answer_bank import upsert_answer
from core.employer_answers import build_employer_answers
from core.file_store import (
    has_uploaded_documents,
    save_uploaded_resumes,
    save_uploaded_cover_letter,
    list_uploaded_resumes,
    get_uploaded_cover_letter_name,
)
from core.profile_store import load_profile, save_profile

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    if not has_uploaded_documents():
        return RedirectResponse(url="/onboarding", status_code=303)

    jobs = load_jobs()
    decisions = load_decisions()
    uploaded_resumes = list_uploaded_resumes()
    uploaded_cover_letter = get_uploaded_cover_letter_name()

    return templates.TemplateResponse(
        "review_queue.html",
        {
            "request": request,
            "jobs": jobs,
            "decisions": decisions,
            "uploaded_resumes": uploaded_resumes,
            "uploaded_cover_letter": uploaded_cover_letter,
        }
    )


@app.get("/onboarding")
def onboarding_page(request: Request):
    uploaded_resumes = list_uploaded_resumes()
    uploaded_cover_letter = get_uploaded_cover_letter_name()

    return templates.TemplateResponse(
        "onboarding.html",
        {
            "request": request,
            "uploaded_resumes": uploaded_resumes,
            "uploaded_cover_letter": uploaded_cover_letter,
        }
    )


@app.post("/onboarding")
async def onboarding_submit(
    resumes: List[UploadFile] = File(...),
    cover_letter: UploadFile = File(...)
):
    save_uploaded_resumes(resumes)
    save_uploaded_cover_letter(cover_letter)
    return RedirectResponse(url="/profile", status_code=303)


@app.get("/profile")
def profile_page(request: Request):
    profile = load_profile()

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "profile": profile,
        }
    )


@app.post("/profile")
def save_profile_page(
    desired_salary: str = Form(""),
    visa_status: str = Form(""),
    worked_here_before: str = Form(""),
    has_referral: str = Form(""),
    notice_period: str = Form(""),
    relocation: str = Form(""),
    driver_license: str = Form(""),
    gender: str = Form(""),
    ethnicity: str = Form(""),
    disability_status: str = Form(""),
    medical_status: str = Form(""),
):
    profile_data = {
        "desired_salary": desired_salary,
        "visa_status": visa_status,
        "worked_here_before": worked_here_before,
        "has_referral": has_referral,
        "notice_period": notice_period,
        "relocation": relocation,
        "driver_license": driver_license,
        "gender": gender,
        "ethnicity": ethnicity,
        "disability_status": disability_status,
        "medical_status": medical_status,
    }

    save_profile(profile_data)
    return RedirectResponse(url="/", status_code=303)


@app.post("/decision")
def make_decision(job_id: str = Form(...), action: str = Form(...)):
    if action == "apply":
        save_decision(job_id, "generating_documents")
        return RedirectResponse(url=f"/prepare-application/{job_id}", status_code=303)

    if action == "skip":
        save_decision(job_id, "skipped")
        return RedirectResponse(url="/", status_code=303)

    if action == "edit_resume":
        return RedirectResponse(url=f"/edit-resume/{job_id}", status_code=303)

    if action == "edit_answers":
        return RedirectResponse(url=f"/prepare-answers/{job_id}", status_code=303)

    return RedirectResponse(url="/", status_code=303)


@app.get("/prepare-application/{job_id}")
def prepare_application(request: Request, job_id: str):
    job = get_job_by_id(job_id)

    if not job:
        return {"message": "Job not found"}

    resume_text = load_saved_resume(job_id)
    cover_letter_text = load_saved_cover_letter(job_id)

    save_resume_text(job_id, resume_text)
    save_cover_letter_text(job_id, cover_letter_text)
    save_decision(job_id, "documents_ready")

    return templates.TemplateResponse(
        "application_preview.html",
        {
            "request": request,
            "job": job,
            "resume_text": resume_text,
            "cover_letter_text": cover_letter_text
        }
    )


@app.get("/prepare-answers/{job_id}")
def prepare_answers(request: Request, job_id: str):
    job = get_job_by_id(job_id)

    if not job:
        return {"message": "Job not found"}

    answers = build_employer_answers(job)
    save_decision(job_id, "answers_ready")

    return templates.TemplateResponse(
        "edit_answers.html",
        {
            "request": request,
            "job": job,
            "answers": answers
        }
    )


@app.get("/edit-resume/{job_id}")
def edit_resume_page(request: Request, job_id: str):
    job = get_job_by_id(job_id)
    resume_text = load_saved_resume(job_id)

    return templates.TemplateResponse(
        "edit_resume.html",
        {
            "request": request,
            "job": job,
            "resume_text": resume_text
        }
    )


@app.post("/edit-resume/{job_id}")
def save_resume_page(job_id: str, content: str = Form(...)):
    save_resume_text(job_id, content)
    save_decision(job_id, "resume_edited")
    return RedirectResponse(url=f"/prepare-application/{job_id}", status_code=303)


@app.get("/edit-cover-letter/{job_id}")
def edit_cover_letter_page(request: Request, job_id: str):
    job = get_job_by_id(job_id)
    cover_letter_text = load_saved_cover_letter(job_id)

    return templates.TemplateResponse(
        "edit_cover_letter.html",
        {
            "request": request,
            "job": job,
            "cover_letter_text": cover_letter_text
        }
    )


@app.post("/edit-cover-letter/{job_id}")
def save_cover_letter_page(job_id: str, content: str = Form(...)):
    save_cover_letter_text(job_id, content)
    save_decision(job_id, "documents_ready")
    return RedirectResponse(url=f"/prepare-application/{job_id}", status_code=303)


@app.get("/edit-answers/{job_id}")
def edit_answers_page(request: Request, job_id: str):
    job = get_job_by_id(job_id)

    if not job:
        return {"message": "Job not found"}

    answers = build_employer_answers(job)

    return templates.TemplateResponse(
        "edit_answers.html",
        {
            "request": request,
            "job": job,
            "answers": answers
        }
    )


@app.post("/edit-answers/{job_id}")
async def save_answers_page(request: Request, job_id: str):
    form = await request.form()

    for key, value in form.items():
        if key.startswith("question__"):
            question = key.replace("question__", "", 1)
            answer_key = f"answer__{question}"
            answer = form.get(answer_key, "")

            if answer.strip():
                upsert_answer(question, answer)

    save_decision(job_id, "ready_to_apply")
    return RedirectResponse(url=f"/edit-answers/{job_id}", status_code=303)