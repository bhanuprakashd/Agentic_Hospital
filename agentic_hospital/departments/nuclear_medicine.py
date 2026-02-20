"""Nuclear Medicine Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.nuclear_medicine import NUCLEAR_MEDICINE_INSTRUCTION
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
from ..tools.nuclear_medicine_tools import (
    pet_ct_oncology_assessment,
    thyroid_scan_interpretation,
)
from ..tools.image_tools import analyze_medical_image
from ..tools.websearch_tools import web_search

nuclear_medicine_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="nuclear_medicine_agent",
    description="Nuclear Medicine specialist: handles diagnostic and therapeutic nuclear medicine including PET/CT imaging, bone scans, thyroid scanning and therapy, cardiac nuclear stress testing, and V/Q scans. Accepts PET/CT and nuclear scintigraphy images.",
    instruction=NUCLEAR_MEDICINE_INSTRUCTION,
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
        pet_ct_oncology_assessment,
        thyroid_scan_interpretation,
        analyze_medical_image,
        web_search,
    ],
)
