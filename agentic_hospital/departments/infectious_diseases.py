"""Infectious Diseases Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.infectious_diseases import INFECTIOUS_DISEASES_INSTRUCTION
from ..tools.common_tools import (
    get_patient_info,
    record_vitals,
    check_drug_interactions,
    schedule_appointment,
    get_lab_results,
    generate_soap_note,
    calculate_medication_dose,
    record_patient_encounter,
    get_patient_encounter_history,
    request_mdt_consultation,
    generate_treatment_plan,
)
from ..tools.monitoring_tools import check_critical_lab_values, generate_deterioration_alert
from ..tools.infectious_diseases_tools import (
    sepsis_screening,
    antibiotic_selection_guide,
)
from ..tools.websearch_tools import web_search

infectious_diseases_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="infectious_diseases_agent",
    description="Infectious Diseases specialist: handles bacterial, viral, fungal, and parasitic infections including sepsis, HIV/AIDS, TB, STIs, antimicrobial stewardship, and immunization.",
    instruction=INFECTIOUS_DISEASES_INSTRUCTION,
    tools=[
        get_patient_info,
        record_vitals,
        check_drug_interactions,
        schedule_appointment,
        get_lab_results,
        generate_soap_note,
        calculate_medication_dose,
        record_patient_encounter,
        get_patient_encounter_history,
        request_mdt_consultation,
        generate_treatment_plan,
        check_critical_lab_values,
        generate_deterioration_alert,
        sepsis_screening,
        antibiotic_selection_guide,
        web_search,
    ],
)
