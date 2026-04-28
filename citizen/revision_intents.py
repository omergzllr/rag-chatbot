from typing import Dict


INTENT_KEYWORDS = {
    "notice_days": ["sureyi", "gun", "süreyi", "30 gün", "45 gün"],
    "notary_clause": ["noter", "noterden", "tasdik", "onay"],
}


def apply_revision(answers: Dict[str, str], command: str) -> Dict[str, str]:
    updated = dict(answers)
    lower = command.lower()

    if any(token in lower for token in INTENT_KEYWORDS["notary_clause"]):
        current = updated.get("extra_clauses", "")
        clause = "Noter kanaliyla ihtar gonderilecektir."
        updated["extra_clauses"] = f"{current} {clause}".strip()

    if any(token in lower for token in INTENT_KEYWORDS["notice_days"]):
        for part in lower.split():
            if part.isdigit():
                updated["notice_days"] = part
                break

    return updated

