"""Hematology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.hematology import HEMATOLOGY_INSTRUCTION
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
from ..tools.hematology_tools import (
    anemia_classification,
    dvt_risk_assessment,
)
from ..tools.websearch_tools import web_search

hematology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="hematology_agent",
    description="Hematology specialist: handles blood disorders including anemia, bleeding disorders, thrombocytopenia, DVT/PE, leukemia, lymphoma, multiple myeloma, sickle cell disease, and anticoagulation management.",
    instruction=HEMATOLOGY_INSTRUCTION,
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
        anemia_classification,
        dvt_risk_assessment,
        web_search,
    ],
)
