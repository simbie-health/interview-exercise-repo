"""
Agent tools for patient lookup.

These are the tools the AI agent can call during a phone call with a patient.
Each tool interacts with the EHR through the factory — so it works regardless
of which clinic the call is for.
"""

from ehr_services.ehr_factory import get_ehr_service


def search_patient(clinic: str, date_of_birth: str) -> dict:
    """Search for a patient by date of birth.

    This tool is called by the agent when a patient calls in and provides their DOB.
    The agent uses this to identify who's calling.

    Args:
        clinic: Which clinic the call is for (e.g., "clinic_a")
        date_of_birth: Patient DOB in "YYYY-MM-DD" format

    Returns:
        {
            "found": True/False,
            "patients": [...],     # list of matching patients
            "message": "..."       # human-readable result for the agent
        }
    """
    ehr = get_ehr_service(clinic)
    patients = ehr.search_patients_by_dob(date_of_birth)

    if not patients:
        return {
            "found": False,
            "patients": [],
            "message": "No patients found with that date of birth.",
        }

    if len(patients) == 1:
        p = patients[0]
        return {
            "found": True,
            "patients": patients,
            "message": f"Found patient: {p['first_name']} {p['last_name']}.",
        }

    return {
        "found": True,
        "patients": patients,
        "message": f"Found {len(patients)} patients with that date of birth.",
    }
