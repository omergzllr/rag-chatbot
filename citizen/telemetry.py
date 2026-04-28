import json
from datetime import datetime
from pathlib import Path
from typing import Dict


LOG_PATH = Path(__file__).resolve().parent.parent / "telemetry_log.jsonl"


def track_event(event_type: str, payload: Dict) -> None:
    event = {"event_type": event_type, "timestamp": datetime.utcnow().isoformat(), **payload}
    try:
        with LOG_PATH.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass

