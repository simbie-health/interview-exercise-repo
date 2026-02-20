"""
Mock data for EHR systems.
Simulates the raw API responses from different EHR systems.

The candidate should READ this to understand data formats, but NOT modify it.
"""


# ──────────────────────────────────────────────
# Clinic A — raw API data
# ──────────────────────────────────────────────

CLINIC_A_PATIENTS = [
    {
        "patientId": "PA-101",
        "firstName": "John",
        "lastName": "Doe",
        "dob": "03/15/1985",
        "phoneNumber": "5551234567",
        "emailAddress": "john.doe@email.com",
    },
    {
        "patientId": "PA-102",
        "firstName": "Jane",
        "lastName": "Wilson",
        "dob": "11/08/1972",
        "phoneNumber": "5559876543",
        "emailAddress": None,
    },
    {
        "patientId": "PA-103",
        "firstName": "Bob",
        "lastName": "Martin",
        "dob": "03/15/1985",  # Same DOB as John — tests multiple results
        "phoneNumber": None,
        "emailAddress": "bob.m@email.com",
    },
]


# ──────────────────────────────────────────────
# Clinic B — raw API data (different format!)
#
# - Patient names are "Last, First"
# - DOB is ISO format (YYYY-MM-DD) instead of MM/DD/YYYY
# - Phone numbers already have dashes
# - Different field names for everything
# ──────────────────────────────────────────────

CLINIC_B_PATIENTS = [
    {
        "record_id": "REC-5001",
        "full_name": "Garcia, Maria",
        "birth_date": "1985-03-15",
        "contact_phone": "555-111-2222",
        "contact_email": "maria.garcia@email.com",
    },
    {
        "record_id": "REC-5002",
        "full_name": "Thompson, Robert",
        "birth_date": "1972-11-08",
        "contact_phone": None,
        "contact_email": None,
    },
    {
        "record_id": "REC-5003",
        "full_name": "Kim, Susan",
        "birth_date": "1985-03-15",  # Same DOB as Maria
        "contact_phone": "555-333-4444",
        "contact_email": None,
    },
    {
        "record_id": "REC-5004",
        "full_name": "Patel, Raj",
        "birth_date": "1998-11-06",  # Missing DOB!
        "contact_phone": "555-555-6666",
        "contact_email": "raj@email.com",
    },
]
