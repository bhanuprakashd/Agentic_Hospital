"""Gynecology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.gynecology import GYNECOLOGY_INSTRUCTION
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
from ..tools.gynecology_tools import pregnancy_risk_assessment, menstrual_cycle_analysis
from ..tools.websearch_tools import web_search

gynecology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="gynecology_agent",
    description="Gynecology specialist: handles women's reproductive health, pregnancy care, PCOS, menstrual disorders, endometriosis, and fertility evaluation.",
    instruction=GYNECOLOGY_INSTRUCTION,
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
        pregnancy_risk_assessment,
        menstrual_cycle_analysis,
        web_search,
    ],
)
