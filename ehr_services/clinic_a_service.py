"""
EHR integration for Clinic A.
Transforms Clinic A's raw API format into our normalized internal format.
"""

from datetime import datetime

from ehr_services.base_ehr import BaseEHRService
from ehr_services.mock_data import CLINIC_A_PATIENTS


class ClinicAService(BaseEHRService):
    ehr_name = "clinic_a"

    def search_patients_by_dob(self, date_of_birth: str) -> list[dict]:
        # Clinic A stores DOB as "MM/DD/YYYY", we receive "YYYY-MM-DD"
        dob_obj = datetime.strptime(date_of_birth, "%Y-%m-%d")
        clinic_a_dob = dob_obj.strftime("%m/%d/%Y")

        results = []
        for raw in CLINIC_A_PATIENTS:
            if raw["dob"] == clinic_a_dob:
                results.append(self._transform_patient(raw))
        return results

    def _transform_patient(self, raw: dict) -> dict:
        return {
            "id": raw["patientId"],
            "first_name": raw["firstName"],
            "last_name": raw["lastName"],
            "date_of_birth": datetime.strptime(raw["dob"], "%m/%d/%Y").strftime("%Y-%m-%d"),
            "phone": self._format_phone(raw.get("phoneNumber")),
            "email": raw.get("emailAddress"),
        }

    def _format_phone(self, phone: str | None) -> str | None:
        if not phone:
            return None
        # "5551234567" → "555-123-4567"
        if len(phone) == 10:
            return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
        return phone
