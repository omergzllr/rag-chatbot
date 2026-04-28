import re
from pathlib import Path
from typing import Dict

from citizen.doc_types import DOCUMENT_TYPES, CitizenDocType


TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates" / "citizen"
_PLACEHOLDER_RE = re.compile(r"\{\{\s*([\w.]+)\s*\}\}")


def _safe_fill(template: str, values: Dict[str, str]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
        rendered = rendered.replace("{{ " + key + " }}", str(value))

    rendered = _PLACEHOLDER_RE.sub("", rendered)
    rendered = re.sub(r"\n[ \t]*\n[ \t]*\n+", "\n\n", rendered)
    return rendered.strip() + "\n"


def render_document(doc_type: str, answers: Dict[str, str]) -> str:
    definition = DOCUMENT_TYPES[CitizenDocType(doc_type)]
    template_path = TEMPLATE_DIR / f"{doc_type}.j2"
    if not template_path.exists():
        raise FileNotFoundError(f"Template bulunamadi: {template_path}")

    template = template_path.read_text(encoding="utf-8")
    base = _safe_fill(template, answers)
    return f"{base}\n---\nUyari: {definition.legal_notice}"

