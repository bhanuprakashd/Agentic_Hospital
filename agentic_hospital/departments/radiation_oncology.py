"""Radiation Oncology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.radiation_oncology import RADIATION_ONCOLOGY_INSTRUCTION
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
from ..tools.radiation_oncology_tools import (
    calculate_radiation_dose,
    radiation_toxicity_assessment,
)
from ..tools.websearch_tools import web_search

radiation_oncology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="radiation_oncology_agent",
    description="Radiation Oncology specialist: calculates evidence-based radiation dose prescriptions (BED/EQD2), manages IMRT/SBRT/SRS/brachytherapy, assesses and manages CTCAE-graded radiation toxicities, and coordinates concurrent systemic therapy.",
    instruction=RADIATION_ONCOLOGY_INSTRUCTION,
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
        calculate_radiation_dose,
        radiation_toxicity_assessment,
        web_search,
    ],
)
