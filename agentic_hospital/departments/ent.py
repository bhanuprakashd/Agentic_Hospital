"""ENT (Ear, Nose, Throat) Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.ent import ENT_INSTRUCTION
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
from ..tools.ent_tools import hearing_assessment, sleep_apnea_screening
from ..tools.websearch_tools import web_search

ent_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="ent_agent",
    description="ENT specialist: handles ear, nose, and throat conditions including sinusitis, hearing loss, tinnitus, vertigo, sleep apnea, and voice disorders.",
    instruction=ENT_INSTRUCTION,
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
        hearing_assessment,
        sleep_apnea_screening,
        web_search,
    ],
)
