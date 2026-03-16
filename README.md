# Job Pecker

Project Status: Prototype / In Development

Job Pecker is a semi-automated job application assistant designed to reduce repetitive work when applying to multiple jobs.

Instead of manually editing resumes, cover letters, and application answers for every job posting, Job Pecker generates drafts based on a job description and allows the user to review and confirm them before applying.

The goal is to build a system that automates the repetitive parts of job applications while keeping the final confirmation under user control.

---

# Features

## Job Review Queue

The system displays available job postings with key information such as:

- Job title
- Company
- Location
- Distance
- Fit score
- Visa risk

Each job has four possible actions:

- **Apply**
- **Skip**
- **Edit Resume**
- **Edit Answers**

---

## Resume & Cover Letter Draft Generation

When **Apply** is clicked:

1. The system reads the uploaded base resume and cover letter
2. Extracts the job description
3. Generates a draft resume and cover letter for that job

The user can then:

- Preview both documents
- Edit the resume
- Edit the cover letter
- Confirm the documents

---

## Employer Question Auto Draft

Many job applications include written questions such as:

- Why are you interested in this role?
- What makes you a strong fit for this role?

Job Pecker automatically:

- Generates draft answers based on the job description
- Allows the user to edit them
- Saves answers for reuse later

---

## Answer Memory

If the user answers a question once, the system remembers it.

For example:

- Visa status
- Desired salary
- Notice period
- Referral status

These answers can be reused automatically in future applications.

---

## Profile Storage

Common application information is stored once:

- Visa status
- Desired salary
- Referral status
- Notice period
- Relocation availability
- Driver license status
- Optional demographic questions

This prevents users from entering the same information repeatedly.

---

## Resume Upload

On first use, the user uploads:

- One or more base resumes
- A base cover letter

These documents are used as the source for generating tailored drafts.

---

# Workflow
Upload Resume & Cover Letter
↓
Review Job List
↓
Click Apply
↓
Generate Resume + Cover Letter Draft
↓
Preview and Edit Documents
↓
Generate Employer Answers
↓
Preview and Confirm Answers
↓
Open Job Application Page


---

# Tech Stack

- Python
- FastAPI
- Jinja2 Templates
- HTML
- python-docx (for reading uploaded resumes)
- JSON storage for decisions and answer memory

---

# Project Structure

Job-Pecker
│
├── app
│ └── main.py
│
├── core
│ ├── job_collector.py
│ ├── resume_tailor.py
│ ├── employer_answers.py
│ ├── answer_bank.py
│ ├── profile_store.py
│ ├── file_store.py
│ └── docx_reader.py
│
├── templates
│ ├── review_queue.html
│ ├── application_preview.html
│ ├── edit_resume.html
│ ├── edit_cover_letter.html
│ ├── edit_answers.html
│ └── onboarding.html
│
├── data
│ ├── uploads
│ ├── generated
│ └── profile
│
└── requirements.txt
---
# Running the Project

Install dependencies:


pip install -r requirements.txt


Run the server:


uvicorn app.main:app --reload


Open in browser:


http://127.0.0.1:8000


---

# Future Improvements

Planned features:

- AI-powered resume tailoring
- Job scraping from Seek / Indeed / LinkedIn
- Automatic application form filling
- Browser automation for applications
- Resume-job fit scoring
- Job ranking by relevance

---

# Purpose

This project explores how automation and AI can simplify the job application process and reduce repetitive work when applying to multiple positions.
