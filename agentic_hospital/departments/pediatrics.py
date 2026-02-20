"""Pediatrics Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.pediatrics import PEDIATRICS_INSTRUCTION
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
from ..tools.pediatrics_tools import (
    pediatric_growth_assessment,
    vaccination_tracker,
)
from ..tools.websearch_tools import web_search

pediatrics_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="pediatrics_agent",
    description="Pediatrics specialist: handles medical care of infants, children, and adolescents including well-child visits, vaccinations, developmental screening, common pediatric infections, and behavioral concerns.",
    instruction=PEDIATRICS_INSTRUCTION,
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
        pediatric_growth_assessment,
        vaccination_tracker,
        web_search,
    ],
)
