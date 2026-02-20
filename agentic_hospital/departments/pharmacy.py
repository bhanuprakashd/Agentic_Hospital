"""Pharmacy Agent — Medication verification, dispensing, and reconciliation."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.pharmacy import PHARMACY_INSTRUCTION
from ..tools.common_tools import get_patient_info, check_drug_interactions
from ..tools.pharmacy_tools import (
    verify_medication_order,
    dispense_medication,
    medication_reconciliation,
    generate_tta_prescription,
)

pharmacy_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="pharmacy_agent",
    description=(
        "Clinical Pharmacist at Agentic Hospital. "
        "Verifies all medication orders against formulary and patient allergies, "
        "performs medication reconciliation at admission and discharge, "
        "dispenses medications with batch tracking, and generates TTA (Take-To-Away) "
        "prescriptions for discharged patients. Ensures medication safety through "
        "comprehensive interaction checking and renal dose adjustment verification."
    ),
    instruction=PHARMACY_INSTRUCTION,
    tools=[
        get_patient_info,
        check_drug_interactions,
        verify_medication_order,
        dispense_medication,
        medication_reconciliation,
        generate_tta_prescription,
    ],
)
