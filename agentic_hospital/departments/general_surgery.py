"""General Surgery Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.general_surgery import GENERAL_SURGERY_INSTRUCTION
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
from ..tools.general_surgery_tools import (
    appendicitis_scoring,
    surgical_risk_assessment,
)
from ..tools.websearch_tools import web_search

general_surgery_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="general_surgery_agent",
    description="General Surgery specialist: handles surgical treatment of general conditions including appendicitis, cholecystitis, hernia, bowel obstruction, breast surgery, thyroid surgery, and bariatric surgery.",
    instruction=GENERAL_SURGERY_INSTRUCTION,
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
        appendicitis_scoring,
        surgical_risk_assessment,
        web_search,
    ],
)
