"""Dermatology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.dermatology import DERMATOLOGY_INSTRUCTION
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
from ..tools.dermatology_tools import skin_lesion_analysis, allergy_patch_test_interpretation
from ..tools.image_tools import analyze_medical_image
from ..tools.websearch_tools import web_search

dermatology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="dermatology_agent",
    description="Dermatology specialist: handles skin conditions, acne, eczema, psoriasis, skin cancer screening (ABCDE criteria), and allergy testing. Accepts skin lesion photos and rash images.",
    instruction=DERMATOLOGY_INSTRUCTION,
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
        skin_lesion_analysis,
        allergy_patch_test_interpretation,
        analyze_medical_image,
        web_search,
    ],
)
