"""Psychology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.psychology import PSYCHOLOGY_INSTRUCTION
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
from ..tools.psychology_tools import (
    phq9_depression_screening,
    crisis_assessment,
)
from ..tools.websearch_tools import web_search

psychology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="psychology_agent",
    description="Psychology specialist: handles mental health assessment, depression and anxiety screening, PTSD, crisis intervention, and therapeutic recommendations.",
    instruction=PSYCHOLOGY_INSTRUCTION,
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
        phq9_depression_screening,
        crisis_assessment,
        web_search,
    ],
)
