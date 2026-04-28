import json
from pathlib import Path
from typing import Dict

from citizen.rights_engine import classify_case


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_json(path: Path, fallback: dict) -> dict:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def estimate_cost_and_duration(case_text: str, city: str = "istanbul") -> Dict:
    category = classify_case(case_text)
    costs = _load_json(DATA_DIR / "court_costs_tr.json", {})
    durations = _load_json(DATA_DIR / "case_duration_baseline_tr.json", {})

    city_key = city.lower()
    category_cost = costs.get(category, {})
    category_duration = durations.get(category, {})

    estimated_cost = category_cost.get(city_key, category_cost.get("default", {}))
    estimated_duration = category_duration.get(city_key, category_duration.get("default", {}))

    return {
        "category": category,
        "city": city_key,
        "cost_breakdown": estimated_cost,
        "duration_estimate": estimated_duration,
        "disclaimer": "Tahminler bilgilendirme amaclidir; resmi tarifeler ve yerel mahkeme yogunlugu degisebilir.",
    }

