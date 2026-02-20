"""Critical Care Medicine Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.critical_care import CRITICAL_CARE_INSTRUCTION
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
from ..tools.critical_care_tools import (
    calculate_severity_score,
    organ_dysfunction_assessment,
)
from ..tools.websearch_tools import web_search

critical_care_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="critical_care_agent",
    description="Critical Care Medicine specialist: handles ICU-level care including sepsis, ARDS, mechanical ventilation, multi-organ dysfunction, hemodynamic monitoring, and post-cardiac arrest care.",
    instruction=CRITICAL_CARE_INSTRUCTION,
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
        calculate_severity_score,
        organ_dysfunction_assessment,
        web_search,
    ],
)
