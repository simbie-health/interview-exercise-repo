"""
Simbie AI — Interview Exercise: Backend/Integrations

We build AI agents that handle phone calls for medical clinics.
Each clinic uses a different EHR (Electronic Health Records) system.
We have a base class + factory pattern to support multiple EHRs.

Currently Clinic A is integrated. Your task: add Clinic B.

Run the agent:
    python main.py agent

Run the tests:
    python main.py test
"""

import sys
from ehr_services.ehr_factory import get_ehr_service


def run_agent_mode():
    """Start the interactive agent."""
    from agent import run_agent

    print("Which clinic is calling?")
    print("  1. clinic_a")
    print("  2. clinic_b")
    choice = input("\nSelect (1/2): ").strip()

    clinic = "clinic_a" if choice == "1" else "clinic_b"

    try:
        get_ehr_service(clinic)  # Verify it's registered
    except Exception as e:
        print(f"\nError: {e}")
        return

    run_agent(clinic)


def main():
    run_agent_mode()


if __name__ == "__main__":
    main()
