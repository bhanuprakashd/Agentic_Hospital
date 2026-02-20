"""Anesthesiology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.anesthesiology import ANESTHESIOLOGY_INSTRUCTION
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
from ..tools.anesthesiology_tools import (
    asa_physical_status_classification,
    calculate_anesthesia_risk,
)
from ..tools.websearch_tools import web_search

anesthesiology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="anesthesiology_agent",
    description="Anesthesiology specialist: handles pre-operative assessment, anesthetic management, airway management, regional/general anesthesia, sedation, and perioperative pain management.",
    instruction=ANESTHESIOLOGY_INSTRUCTION,
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
        asa_physical_status_classification,
        calculate_anesthesia_risk,
        web_search,
    ],
)
