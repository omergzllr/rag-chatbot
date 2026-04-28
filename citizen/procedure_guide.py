from typing import Dict, List

from citizen.rights_engine import classify_case


GUIDES: Dict[str, List[dict]] = {
    "consumer": [
        {"step": 1, "action": "Fatura, sozlesme ve yazismalari toplayin"},
        {"step": 2, "action": "Saticiya yazili ihtar/tespit talebi gonderin"},
        {"step": 3, "action": "Tuketici Hakem Heyeti basvurusu yapin"},
    ],
    "rental": [
        {"step": 1, "action": "Kira sozlesmesi ve odeme dekontlarini hazirlayin"},
        {"step": 2, "action": "Yazili ihtarnameyi gonderin"},
        {"step": 3, "action": "Gerekirse sulh hukuk mahkemesi surecini baslatin"},
    ],
    "employment": [
        {"step": 1, "action": "Bordro, SGK kaydi ve mesai delillerini toplayin"},
        {"step": 2, "action": "Arabuluculuk basvurusu yapin"},
        {"step": 3, "action": "Anlasma olmazsa dava acma hazirligi yapin"},
    ],
    "criminal": [
        {"step": 1, "action": "Delilleri dijital ve fiziksel olarak saklayin"},
        {"step": 2, "action": "Savciliga suc duyurusu dilekcesi verin"},
        {"step": 3, "action": "Soru numarasi ile dosya takibi yapin"},
    ],
}


def build_procedure_guide(text: str) -> Dict:
    category = classify_case(text)
    return {"category": category, "checklist": GUIDES.get(category, GUIDES["consumer"])}

