"""Allergy and Immunology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.allergy_immunology import ALLERGY_IMMUNOLOGY_INSTRUCTION
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
from ..tools.allergy_immunology_tools import (
    allergy_skin_test_interpretation,
    immunodeficiency_risk_assessment,
)
from ..tools.websearch_tools import web_search

allergy_immunology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="allergy_immunology_agent",
    description="Allergy and Immunology specialist: handles allergic diseases, immunodeficiency, anaphylaxis, asthma, food/drug allergies, and immune system disorders.",
    instruction=ALLERGY_IMMUNOLOGY_INSTRUCTION,
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
        allergy_skin_test_interpretation,
        immunodeficiency_risk_assessment,
        web_search,
    ],
)
