"""
Factory for creating EHR service instances.

Each clinic is configured with an EHR type. The factory returns the right
service implementation based on that type.
"""

from ehr_services.base_ehr import BaseEHRService
from ehr_services.clinic_a_service import ClinicAService

_instances: dict[str, BaseEHRService] = {}


def get_ehr_service(ehr_name: str) -> BaseEHRService:
    """Get or create the EHR service for a given clinic."""
    if ehr_name not in _instances:
        match ehr_name:
            case "clinic_a":
                _instances[ehr_name] = ClinicAService()
            # case "clinic_b":
            #     _instances[ehr_name] = ClinicBService()
            case _:
                raise ValueError(f"No EHR integration for '{ehr_name}'")
    return _instances[ehr_name]
