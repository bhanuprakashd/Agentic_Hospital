"""Endocrinology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.endocrinology import ENDOCRINOLOGY_INSTRUCTION
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
from ..tools.endocrinology_tools import (
    diabetes_management_assessment,
    thyroid_nodule_assessment,
)
from ..tools.websearch_tools import web_search

endocrinology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="endocrinology_agent",
    description="Endocrinology specialist: handles hormonal and metabolic disorders including diabetes, thyroid disorders, adrenal disorders, pituitary disorders, osteoporosis, PCOS, and obesity.",
    instruction=ENDOCRINOLOGY_INSTRUCTION,
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
        diabetes_management_assessment,
        thyroid_nodule_assessment,
        web_search,
    ],
)
