# Job Pecker

Job Pecker is a semi-automated job application assistant designed to streamline the job search and application process.

The goal of the project is to reduce repetitive work when applying to multiple job postings by automatically preparing tailored resumes, cover letters, and application answers based on a job description.

Instead of manually editing documents for every job application, Job Pecker generates drafts and allows the user to review and confirm them before submitting.

---

## Features

### Job Review Queue
Displays job postings with:

- Job title
- Company
- Location
- Distance
- Fit score
- Visa risk

Users can choose to:

- Apply
- Skip
- Edit resume
- Edit answers

---

### Resume & Cover Letter Draft Generation

When **Apply** is clicked:

1. The system reads the uploaded base resume and cover letter
2. Extracts the job description
3. Generates a draft resume and cover letter for that specific job

The user can:

- Preview documents
- Edit resume
- Edit cover letter
- Confirm documents

---

### Employer Question Auto Draft

Many job applications require answering questions such as:

- Why are you interested in this role?
- What makes you a strong fit for this role?

Job Pecker automatically:

- Detects likely employer questions
- Pre-fills answers using the job description and previous responses
- Allows the user to edit before confirming

---

### Answer Memory

When the user answers a question once, the system remembers it.

For example:
