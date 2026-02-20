"""Urology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.urology import UROLOGY_INSTRUCTION
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
from ..tools.urology_tools import (
    kidney_stone_assessment,
    prostate_assessment,
)
from ..tools.websearch_tools import web_search

urology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="urology_agent",
    description="Urology specialist: handles urinary tract and male reproductive system conditions including kidney stones, BPH, prostate cancer, bladder cancer, urinary incontinence, hematuria, and erectile dysfunction.",
    instruction=UROLOGY_INSTRUCTION,
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
        kidney_stone_assessment,
        prostate_assessment,
        web_search,
    ],
)
