"""General Medicine Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.general_medicine import GENERAL_MEDICINE_INSTRUCTION
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
from ..tools.general_medicine_tools import bmi_calculator, vaccination_schedule
from ..tools.websearch_tools import web_search

general_medicine_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="general_medicine_agent",
    description="General Medicine / Internal Medicine specialist: handles common illnesses, preventive care, chronic disease management, vaccinations, and initial evaluation before specialist referral.",
    instruction=GENERAL_MEDICINE_INSTRUCTION,
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
        bmi_calculator,
        vaccination_schedule,
        web_search,
    ],
)
