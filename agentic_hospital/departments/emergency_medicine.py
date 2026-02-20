"""Emergency Medicine Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.emergency_medicine import EMERGENCY_MEDICINE_INSTRUCTION
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
from ..tools.emergency_medicine_tools import (
    chest_pain_risk_stratification,
    trauma_triage_assessment,
)
from ..tools.image_tools import analyze_medical_image
from ..tools.websearch_tools import web_search

emergency_medicine_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="emergency_medicine_agent",
    description="Emergency Medicine specialist: handles acute and emergency conditions including trauma, chest pain, stroke, respiratory emergencies, cardiac arrest, shock, anaphylaxis, and triage assessment. Accepts wound, trauma, and injury photos.",
    instruction=EMERGENCY_MEDICINE_INSTRUCTION,
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
        chest_pain_risk_stratification,
        trauma_triage_assessment,
        analyze_medical_image,
        web_search,
    ],
)
