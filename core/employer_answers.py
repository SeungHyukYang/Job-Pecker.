from core.profile_store import load_profile
from core.answer_bank import find_saved_answer


def build_short_form_answers(job):
    profile = load_profile()

    short_questions = [
        {
            "question": "What is your desired salary?",
            "answer": profile.get("desired_salary", ""),
            "source": "profile"
        },
        {
            "question": "What is your current visa status?",
            "answer": profile.get("visa_status", ""),
            "source": "profile"
        },
        {
            "question": "Have you worked for this company before?",
            "answer": profile.get("worked_here_before", ""),
            "source": "profile"
        },
        {
            "question": "Do you have a referral for this application?",
            "answer": profile.get("has_referral", ""),
            "source": "profile"
        },
        {
            "question": "What is your notice period?",
            "answer": profile.get("notice_period", ""),
            "source": "profile"
        },
        {
            "question": "Are you open to relocation?",
            "answer": profile.get("relocation", ""),
            "source": "profile"
        },
        {
            "question": "Do you hold a valid driver license?",
            "answer": profile.get("driver_license", ""),
            "source": "profile"
        },
        {
            "question": "Gender",
            "answer": profile.get("gender", ""),
            "source": "profile"
        },
        {
            "question": "Ethnicity",
            "answer": profile.get("ethnicity", ""),
            "source": "profile"
        },
        {
            "question": "Disability status",
            "answer": profile.get("disability_status", ""),
            "source": "profile"
        },
        {
            "question": "Medical status",
            "answer": profile.get("medical_status", ""),
            "source": "profile"
        }
    ]

    return short_questions


def generate_long_form_answer(question: str, job) -> str:
    if not job:
        return ""

    title = job.title
    company = job.company
    description = job.description

    normalized = question.strip().lower()

    if "interested in this role" in normalized:
        return (
            f"I am interested in this role because it aligns well with my background and strengths in "
            f"analysis, reporting, and cross-functional coordination. The {title} position at {company} "
            f"appeals to me because it offers the opportunity to contribute in a role where analytical thinking, "
            f"attention to detail, and practical problem solving are important. Based on the job description, "
            f"I am particularly interested in the chance to support business objectives through structured work, "
            f"clear communication, and data-informed decision making."
        )

    if "strong fit" in normalized:
        return (
            f"I believe I am a strong fit for this role because my background includes relevant experience in "
            f"analysis, reporting, operations, and coordination across different functions. I have developed "
            f"strong attention to detail, process awareness, and the ability to work with stakeholders to support "
            f"business needs. Based on the requirements described for this role, I believe I can contribute by "
            f"bringing a practical, analytical, and reliable approach to the position."
        )

    if "why do you want to work at" in normalized:
        return (
            f"I want to work at {company} because this opportunity appears to offer a strong match with my skills "
            f"and professional interests. I am particularly drawn to roles where I can apply analytical thinking, "
            f"structured problem solving, and coordination skills in a meaningful business environment. Based on "
            f"the job description, {company} appears to value the kind of strengths I would like to continue "
            f"developing and contributing through in my next role."
        )

    return (
        f"My background and experience are relevant to this opportunity, and I believe I can contribute positively "
        f"to the {title} role at {company}. Based on the job description, I would bring strong attention to detail, "
        f"analytical capability, and a practical approach to supporting team and business objectives."
    )


def build_long_form_answers(job):
    if not job:
        return []

    company_question = f"Why do you want to work at {job.company}?"

    questions = [
        "Why are you interested in this role?",
        "What makes you a strong fit for this role?",
        company_question
    ]

    results = []

    for question in questions:
        saved_answer = find_saved_answer(question)

        if saved_answer:
            answer = saved_answer
            source = "memory"
        else:
            answer = generate_long_form_answer(question, job)
            source = "ai_generated"

        results.append({
            "question": question,
            "answer": answer,
            "source": source
        })

    return results


def build_employer_answers(job):
    short_form = build_short_form_answers(job)
    long_form = build_long_form_answers(job)

    return {
        "short_form": short_form,
        "long_form": long_form
    }