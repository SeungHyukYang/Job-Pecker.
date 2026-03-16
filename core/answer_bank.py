import json
from pathlib import Path

ANSWER_BANK_PATH = Path("data/jobs/answer_bank.json")
ANSWER_BANK_PATH.parent.mkdir(parents=True, exist_ok=True)


def _ensure_file():
    if not ANSWER_BANK_PATH.exists():
        ANSWER_BANK_PATH.write_text("[]", encoding="utf-8")


def load_answer_bank():
    _ensure_file()
    with open(ANSWER_BANK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_answer_bank(data):
    with open(ANSWER_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def normalize_question(question: str) -> str:
    q = question.strip().lower()
    replacements = {
        "?": "",
        ".": "",
        ",": "",
        "  ": " ",
        "\n": " ",
        "\r": " "
    }

    for old, new in replacements.items():
        q = q.replace(old, new)

    return q.strip()


def find_saved_answer(question: str):
    normalized = normalize_question(question)
    answer_bank = load_answer_bank()

    for item in answer_bank:
        if item.get("question_key") == normalized:
            return item.get("answer", "")

    return ""


def upsert_answer(question: str, answer: str):
    normalized = normalize_question(question)
    answer_bank = load_answer_bank()

    for item in answer_bank:
        if item.get("question_key") == normalized:
            item["question_text"] = question
            item["answer"] = answer
            save_answer_bank(answer_bank)
            return

    answer_bank.append({
        "question_key": normalized,
        "question_text": question,
        "answer": answer
    })
    save_answer_bank(answer_bank)


def get_default_questions(job):
    if not job:
        return []

    return [
        {
            "question": "Why are you interested in this role?",
            "suggested_answer": ""
        },
        {
            "question": "What makes you a strong fit for this role?",
            "suggested_answer": ""
        },
        {
            "question": "Do you have the legal right to work in New Zealand?",
            "suggested_answer": ""
        },
        {
            "question": f"Why do you want to work at {job.company}?",
            "suggested_answer": ""
        }
    ]


def build_answer_set(job):
    questions = get_default_questions(job)

    for item in questions:
        saved = find_saved_answer(item["question"])
        item["suggested_answer"] = saved

    return questions