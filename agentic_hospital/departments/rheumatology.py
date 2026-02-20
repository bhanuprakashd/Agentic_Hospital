"""Rheumatology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.rheumatology import RHEUMATOLOGY_INSTRUCTION
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
from ..tools.rheumatology_tools import (
    arthritis_assessment,
    lupus_activity_assessment,
)
from ..tools.websearch_tools import web_search

rheumatology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="rheumatology_agent",
    description="Rheumatology specialist: handles autoimmune and musculoskeletal diseases including rheumatoid arthritis, lupus, psoriatic arthritis, gout, Sjögren's syndrome, vasculitis, and fibromyalgia.",
    instruction=RHEUMATOLOGY_INSTRUCTION,
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
        arthritis_assessment,
        lupus_activity_assessment,
        web_search,
    ],
)
