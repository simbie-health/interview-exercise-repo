"""
Mock data for the EHR system.
Simulates the raw API response from the clinic's EHR.

The candidate should READ this to understand the data format, but NOT modify it.
"""


# ──────────────────────────────────────────────
# Clinic A — raw EHR API data
#
# - DOB is stored as MM/DD/YYYY
# - Phone numbers have no dashes
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
