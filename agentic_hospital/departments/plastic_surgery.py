"""Plastic Surgery Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.plastic_surgery import PLASTIC_SURGERY_INSTRUCTION
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
from ..tools.plastic_surgery_tools import burn_assessment, reconstructive_planning
from ..tools.image_tools import analyze_medical_image
from ..tools.websearch_tools import web_search

plastic_surgery_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="plastic_surgery_agent",
    description="Plastic Surgery specialist: handles burns (Parkland resuscitation, ABA referral criteria), wound reconstruction, skin grafting, flap surgery, breast reconstruction, cleft repair, and cosmetic procedures. Accepts burn and wound images for assessment.",
    instruction=PLASTIC_SURGERY_INSTRUCTION,
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
        burn_assessment,
        reconstructive_planning,
        analyze_medical_image,
        web_search,
    ],
)
