"""Gastroenterology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.gastroenterology import GASTROENTEROLOGY_INSTRUCTION
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
from ..tools.gastroenterology_tools import liver_function_assessment, ibs_symptom_scoring
from ..tools.websearch_tools import web_search

gastroenterology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="gastroenterology_agent",
    description="Gastroenterology specialist: handles digestive system disorders including GERD, IBS, IBD, liver disease, pancreatitis, and GI bleeding.",
    instruction=GASTROENTEROLOGY_INSTRUCTION,
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
        liver_function_assessment,
        ibs_symptom_scoring,
        web_search,
    ],
)
