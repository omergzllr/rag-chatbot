import unittest

from citizen.rights_engine import analyze_rights
from citizen.service import CitizenFlowService
from citizen.validators import validate_required_fields


class CitizenFlowTests(unittest.TestCase):
    def test_required_field_validation(self):
        missing = validate_required_fields("eviction_notice", {"tenant_full_name": "Ali Veli"})
        self.assertTrue(len(missing) > 0)

    def test_high_risk_referral(self):
        result = analyze_rights("Tehdit edildim, silah kullanildi ve agir ceza olabilir.")
        self.assertEqual(result["risk_level"], "high")
        self.assertTrue(result["professional_referral"])

    def test_session_generates_draft(self):
        service = CitizenFlowService()
        started = service.start_session("consumer_complaint", "Ayipli urun icin basvuru yapmak istiyorum")
        session_id = started["session_id"]
        answers = [
            "Ayse Yilmaz",
            "Ornek Magaza A.S.",
            "2026-04-10",
            "12000",
            "Iade",
            "Telefon bozuk cikti ve servis reddetti",
        ]
        payload = None
        for answer in answers:
            payload = service.submit_user_message(session_id, answer)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["flow_state"], "draft_ready")
        self.assertIn("TUKETICI HAKEM HEYETI", payload["draft"])

    def test_state_asks_missing_fields(self):
        service = CitizenFlowService()
        started = service.start_session("eviction_notice")
        self.assertEqual(started["flow_state"], "collecting")
        self.assertIn("Ilk olarak", started["assistant_message"])
        response = service.submit_user_message(started["session_id"], "Ali Veli")
        self.assertEqual(response["flow_state"], "collecting")
        self.assertIn("Bilgi eksik", response["assistant_message"])


if __name__ == "__main__":
    unittest.main()

