"""Orthopedics Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.orthopedics import ORTHOPEDICS_INSTRUCTION
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
from ..tools.orthopedics_tools import fracture_risk_assessment, joint_mobility_score
from ..tools.image_tools import analyze_medical_image
from ..tools.websearch_tools import web_search

orthopedics_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="orthopedics_agent",
    description="Orthopedics specialist: handles bone and joint issues, fractures, arthritis, sports injuries, spine disorders, and osteoporosis assessment. Accepts bone X-rays and joint MRI images.",
    instruction=ORTHOPEDICS_INSTRUCTION,
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
        fracture_risk_assessment,
        joint_mobility_score,
        analyze_medical_image,
        web_search,
    ],
)
