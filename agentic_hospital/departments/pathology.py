"""Pathology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.pathology import PATHOLOGY_INSTRUCTION
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
from ..tools.pathology_tools import interpret_biopsy_result, critical_lab_value_alert
from ..tools.image_tools import analyze_medical_image
from ..tools.websearch_tools import web_search

pathology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="pathology_agent",
    description="Pathology specialist: interprets biopsy and histopathology results using WHO classification and IHC biomarkers (ER/PR/HER2, MSI, PD-L1), identifies AACC critical lab values with immediate management protocols, and provides MDT-ready reports. Accepts histopathology slide images and microscopy photos.",
    instruction=PATHOLOGY_INSTRUCTION,
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
        interpret_biopsy_result,
        critical_lab_value_alert,
        analyze_medical_image,
        web_search,
    ],
)
