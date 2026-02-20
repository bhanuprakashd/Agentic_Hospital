"""Cardiothoracic Surgery Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.cardiothoracic_surgery import CARDIOTHORACIC_SURGERY_INSTRUCTION
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
from ..tools.cardiothoracic_surgery_tools import (
    cardiac_surgery_risk_score,
    thoracic_surgery_feasibility,
)
from ..tools.websearch_tools import web_search

cardiothoracic_surgery_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="cardiothoracic_surgery_agent",
    description="Cardiothoracic Surgery specialist: handles surgical treatment of heart, lung, and chest conditions including CABG, valve surgery, aortic surgery, lung resection, and esophageal surgery.",
    instruction=CARDIOTHORACIC_SURGERY_INSTRUCTION,
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
        cardiac_surgery_risk_score,
        thoracic_surgery_feasibility,
        web_search,
    ],
)
