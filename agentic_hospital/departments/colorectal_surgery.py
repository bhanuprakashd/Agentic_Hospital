"""Colorectal Surgery Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.colorectal_surgery import COLORECTAL_SURGERY_INSTRUCTION
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
from ..tools.colorectal_surgery_tools import (
    colorectal_cancer_screening,
    bowel_obstruction_assessment,
)
from ..tools.websearch_tools import web_search

colorectal_surgery_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="colorectal_surgery_agent",
    description="Colorectal Surgery specialist: handles surgical treatment of colon, rectum, and anal conditions including colorectal cancer, bowel obstruction, hemorrhoids, IBD surgery, and ostomy management.",
    instruction=COLORECTAL_SURGERY_INSTRUCTION,
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
        colorectal_cancer_screening,
        bowel_obstruction_assessment,
        web_search,
    ],
)
