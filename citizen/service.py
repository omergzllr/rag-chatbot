import re
from datetime import datetime
from typing import Dict
from uuid import uuid4

from citizen.doc_types import DOCUMENT_TYPES, CitizenDocType, list_document_catalog
from citizen.estimator import estimate_cost_and_duration
from citizen.procedure_guide import build_procedure_guide
from citizen.question_flows import get_required_fields, next_missing_field, parse_answer_for_field
from citizen.revision_intents import apply_revision
from citizen.rights_engine import analyze_rights
from citizen.template_renderer import render_document
from citizen.telemetry import track_event
from citizen.validators import validate_required_fields


_DATE_RE = re.compile(r"\b(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})\b")
_DAYS_RE = re.compile(r"\b(\d{1,3})\s*(?:gun|gün)\b", re.IGNORECASE)
_AMOUNT_RE = re.compile(r"\b(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?)\s*(?:tl|try|₺)\b", re.IGNORECASE)


def _prefill_answers_from_prompt(doc_type: str, prompt: str) -> Dict[str, str]:
    if not prompt:
        return {}
    fields = {f["key"]: f["label"] for f in get_required_fields(doc_type)}
    answers: Dict[str, str] = {}

    date_match = _DATE_RE.search(prompt)
    if date_match:
        for key in ("incident_date", "contract_date", "sale_date", "termination_date", "employment_start_date"):
            if key in fields and key not in answers:
                answers[key] = date_match.group(1)
                break

    days_match = _DAYS_RE.search(prompt)
    if days_match and "notice_days" in fields:
        answers["notice_days"] = days_match.group(1)

    amount_match = _AMOUNT_RE.search(prompt)
    if amount_match:
        for key in ("purchase_amount", "sale_price"):
            if key in fields and key not in answers:
                answers[key] = f"{amount_match.group(1)} TL"
                break

    return answers


class CitizenFlowService:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}

    def list_document_types(self) -> list:
        return list_document_catalog()

    def start_session(self, doc_type: str, initial_prompt: str = "") -> Dict:
        definition = DOCUMENT_TYPES[CitizenDocType(doc_type)]
        session_id = str(uuid4())
        prefilled = _prefill_answers_from_prompt(doc_type, initial_prompt)
        self.sessions[session_id] = {
            "session_id": session_id,
            "doc_type": doc_type,
            "flow_state": "collecting",
            "answers": dict(prefilled),
            "draft": "",
            "created_at": datetime.utcnow().isoformat(),
            "history": [{"role": "user", "content": initial_prompt}] if initial_prompt else [],
            "asked_field": "",
        }
        track_event(
            "citizen_session_started",
            {"session_id": session_id, "doc_type": doc_type, "prefilled_keys": list(prefilled.keys())},
        )

        first_missing = next_missing_field(doc_type, self.sessions[session_id]["answers"])
        intro = f"\"{definition.title}\" hazirligina basliyoruz."
        if prefilled:
            captured = ", ".join(prefilled.keys())
            intro += f" Anlatiminizdan su alanlari aldim: {captured}."
        if first_missing:
            assistant_message = f"{intro} Lutfen {first_missing['label']} bilgisini yazar misiniz?"
        else:
            assistant_message = f"{intro} Tum gerekli bilgiler hazir, taslagi olusturuyorum."

        self.sessions[session_id]["asked_field"] = first_missing["key"] if first_missing else ""
        self.sessions[session_id]["history"].append({"role": "assistant", "content": assistant_message})

        if not first_missing:
            self.sessions[session_id]["draft"] = render_document(doc_type, self.sessions[session_id]["answers"])
            self.sessions[session_id]["flow_state"] = "draft_ready"
            track_event(
                "citizen_draft_ready",
                {"session_id": session_id, "doc_type": doc_type, "answer_count": len(self.sessions[session_id]["answers"])},
            )

        return self._build_response(session_id, assistant_message)

    def submit_user_message(self, session_id: str, message: str) -> Dict:
        if session_id not in self.sessions:
            raise ValueError("Session bulunamadi")
        session = self.sessions[session_id]
        session["history"].append({"role": "user", "content": message})

        if session["flow_state"] in {"draft_ready", "review"}:
            session["answers"] = apply_revision(session["answers"], message)

        missing = next_missing_field(session["doc_type"], session["answers"])
        if missing and session["flow_state"] == "collecting":
            target_field = session.get("asked_field") or missing["key"]
            session["answers"].update(parse_answer_for_field(message, target_field))
            missing = next_missing_field(session["doc_type"], session["answers"])
            if missing:
                assistant = f"Bilgi eksik: {missing['label']} bilgisini yazar misiniz?"
                session["asked_field"] = missing["key"]
                session["history"].append({"role": "assistant", "content": assistant})
                track_event(
                    "citizen_session_missing_field",
                    {"session_id": session_id, "doc_type": session["doc_type"], "missing_field": missing["key"]},
                )
                return self._build_response(session_id, assistant)

        errors = validate_required_fields(session["doc_type"], session["answers"])
        if errors:
            first = errors[0]
            assistant = f"Devam etmek icin su alan gerekli: {first}."
            session["history"].append({"role": "assistant", "content": assistant})
            return self._build_response(session_id, assistant)

        session["draft"] = render_document(session["doc_type"], session["answers"])
        session["flow_state"] = "draft_ready"
        session["asked_field"] = ""
        track_event(
            "citizen_draft_ready",
            {"session_id": session_id, "doc_type": session["doc_type"], "answer_count": len(session["answers"])},
        )
        assistant = "Taslak hazir. Degisiklik icin komut verebilir veya onaylayabilirsiniz."
        session["history"].append({"role": "assistant", "content": assistant})
        return self._build_response(session_id, assistant)

    def get_session(self, session_id: str) -> Dict:
        if session_id not in self.sessions:
            raise ValueError("Session bulunamadi")
        return self._build_response(session_id)

    def run_citizen_assist(self, narrative: str, city: str = "istanbul") -> Dict:
        rights = analyze_rights(narrative)
        procedure = build_procedure_guide(narrative)
        estimate = estimate_cost_and_duration(narrative, city)
        track_event("citizen_assist_run", {"city": city, "category": rights["category"], "risk_level": rights["risk_level"]})
        return {"rights_analysis": rights, "procedure_guide": procedure, "cost_duration_estimate": estimate}

    def _build_response(self, session_id: str, assistant_message: str = "") -> Dict:
        session = self.sessions[session_id]
        effective_message = assistant_message
        if not effective_message:
            for entry in reversed(session.get("history", [])):
                if entry.get("role") == "assistant" and entry.get("content"):
                    effective_message = entry["content"]
                    break
        if not effective_message and session.get("flow_state") == "collecting":
            missing = next_missing_field(session["doc_type"], session["answers"])
            if missing:
                effective_message = f"Lutfen su bilgiyi yazar misiniz: {missing['label']}"
        return {
            "session_id": session["session_id"],
            "doc_type": session["doc_type"],
            "flow_state": session["flow_state"],
            "answers": session["answers"],
            "draft": session["draft"],
            "assistant_message": effective_message,
            "asked_field": session.get("asked_field", ""),
            "safety_notice": "Uyari: Bu arac bilgilendirme amaclidir ve avukat danismanliginin yerine gecmez.",
        }

