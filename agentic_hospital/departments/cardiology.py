"""Cardiology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.cardiology import CARDIOLOGY_INSTRUCTION
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
from ..tools.cardiology_tools import analyze_ecg, assess_cardiac_risk
from ..tools.image_tools import analyze_medical_image
from ..tools.websearch_tools import web_search

cardiology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="cardiology_agent",
    description="Cardiology specialist: handles heart diseases, chest pain, palpitations, hypertension, arrhythmia, heart failure, and cardiovascular risk assessment. Accepts ECG images and cardiac imaging.",
    instruction=CARDIOLOGY_INSTRUCTION,
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
        analyze_ecg,
        assess_cardiac_risk,
        analyze_medical_image,
        web_search,
    ],
)
