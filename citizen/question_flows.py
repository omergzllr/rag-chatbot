from typing import Dict, List, Optional

from citizen.doc_types import DOCUMENT_TYPES, CitizenDocType


def get_required_fields(doc_type: str) -> List[dict]:
    definition = DOCUMENT_TYPES[CitizenDocType(doc_type)]
    return [{"key": field.key, "label": field.label, "required": field.required} for field in definition.fields]


def next_missing_field(doc_type: str, answers: Dict[str, str]) -> Optional[dict]:
    for field in get_required_fields(doc_type):
        value = str(answers.get(field["key"], "")).strip()
        if field["required"] and not value:
            return field
    return None


def parse_answer_for_field(user_text: str, target_field_key: str) -> Dict[str, str]:
    return {target_field_key: user_text.strip()}

