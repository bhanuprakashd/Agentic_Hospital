"""Neurology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.neurology import NEUROLOGY_INSTRUCTION
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
from ..tools.neurology_tools import assess_stroke_risk, evaluate_consciousness
from ..tools.image_tools import analyze_medical_image
from ..tools.websearch_tools import web_search

neurology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="neurology_agent",
    description="Neurology specialist: handles brain and nervous system disorders including stroke, epilepsy, headaches, Parkinson's, MS, and consciousness assessment. Accepts brain MRI, CT, and neurological imaging.",
    instruction=NEUROLOGY_INSTRUCTION,
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
        assess_stroke_risk,
        evaluate_consciousness,
        analyze_medical_image,
        web_search,
    ],
)
