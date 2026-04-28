from typing import Dict, List


RIGHTS_MAP = {
    "consumer": [
        "Ayipli malda iade, degisim veya bedel indirimi isteme hakkiniz vardir.",
        "Saticidan yazili cevap ve servis raporu talep edebilirsiniz.",
        "Tuketici Hakem Heyeti basvurusu ile uyusmazligi resmi olarak tasiyabilirsiniz.",
    ],
    "rental": [
        "Kira sozlesmesi kapsaminda yazili bildirim ve makul sure talep etme hakkiniz vardir.",
        "Kotu niyetli tahliye baskisina karsi yasal itiraz hakkiniz bulunur.",
        "Depozito iadesi ve hasar kalemlerinin belgeli olmasini isteme hakkiniz vardir.",
    ],
    "employment": [
        "Ucret, fazla mesai ve yillik izin alacaklarinizi talep etme hakkiniz vardir.",
        "Fesihte gerekce ve bildirim surecine iliskin bilgi isteme hakkiniz vardir.",
        "Arabuluculuk ve ise iade basvurusu hakkiniz olabilir.",
    ],
    "criminal": [
        "Savciliga suc duyurusunda bulunma hakkiniz vardir.",
        "Delil, mesaj ve tanik bilgilerini dosyaya sunma hakkiniz vardir.",
        "Sikayet surelerini kacirmadan basvurma hakkiniz vardir.",
    ],
}


def classify_case(text: str) -> str:
    lower = text.lower()
    if any(token in lower for token in ["ayipli", "urun", "hizmet", "iade", "hakem heyeti"]):
        return "consumer"
    if any(token in lower for token in ["kira", "kiraci", "tahliye", "depozito"]):
        return "rental"
    if any(token in lower for token in ["isveren", "maas", "mesai", "istifa", "fesih"]):
        return "employment"
    if any(token in lower for token in ["dolandiricilik", "hakaret", "tehdit", "savcilik", "suc"]):
        return "criminal"
    return "consumer"


def analyze_rights(text: str) -> Dict[str, List[str]]:
    category = classify_case(text)
    rights = RIGHTS_MAP.get(category, RIGHTS_MAP["consumer"])
    high_risk = any(token in text.lower() for token in ["silah", "olum", "cinsel", "agir ceza", "tutuklama"])
    return {
        "category": category,
        "rights": rights,
        "first_step": "Olaya ait tarihceyi ve belgeleri kronolojik sekilde toplayin.",
        "risk_level": "high" if high_risk else "normal",
        "professional_referral": (
            "Konu yuksek riskli gorunuyor. Baro adli yardim veya bir avukattan birebir destek alin."
            if high_risk
            else ""
        ),
    }

