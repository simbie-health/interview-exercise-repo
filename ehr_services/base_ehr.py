"""
Base class for all EHR integrations.

Every clinic uses a different EHR system with a different API and data format.
Subclasses implement the specifics for each EHR.
"""

from abc import ABC, abstractmethod


class BaseEHRService(ABC):
    """Abstract base for EHR integrations. Each EHR must implement these methods."""

    ehr_name: str = ""

    @abstractmethod
    def search_patients_by_dob(self, date_of_birth: str) -> list[dict]:
        """Search for patients by date of birth.

        Args:
            date_of_birth: Patient DOB in "YYYY-MM-DD" format.

        Returns:
            List of patients in our normalized format:
            [
                {
                    "id": "P-123",              # Patient ID in the EHR
                    "first_name": "John",
                    "last_name": "Doe",
                    "date_of_birth": "1985-03-15",
                    "phone": "555-123-4567",     # or None
                    "email": "john@email.com",   # or None
                }
            ]
        """
        ...

