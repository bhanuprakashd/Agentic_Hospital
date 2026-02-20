"""Thoracic Surgery Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.thoracic_surgery import THORACIC_SURGERY_INSTRUCTION
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
from ..tools.thoracic_surgery_tools import (
    pulmonary_function_surgical_risk,
    pleural_disease_assessment,
)
from ..tools.websearch_tools import web_search

thoracic_surgery_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="thoracic_surgery_agent",
    description="Thoracic Surgery specialist: handles lung resection risk assessment (BTS/ESTS guidelines, ppo-FEV1/DLCO), pleural disease (Light's criteria, empyema, pneumothorax), esophageal surgery, mediastinal tumors, and lung cancer surgery.",
    instruction=THORACIC_SURGERY_INSTRUCTION,
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
        pulmonary_function_surgical_risk,
        pleural_disease_assessment,
        web_search,
    ],
)
