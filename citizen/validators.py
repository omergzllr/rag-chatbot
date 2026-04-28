from typing import Dict, List

from citizen.question_flows import get_required_fields


def validate_required_fields(doc_type: str, answers: Dict[str, str]) -> List[str]:
    missing = []
    for field in get_required_fields(doc_type):
        if not field["required"]:
            continue
        if not str(answers.get(field["key"], "")).strip():
            missing.append(field["label"])
    return missing

