"""Neurosurgery Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.neurosurgery import NEUROSURGERY_INSTRUCTION
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
from ..tools.neurosurgery_tools import (
    intracranial_pressure_assessment,
    spinal_cord_injury_assessment,
)
from ..tools.websearch_tools import web_search

neurosurgery_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="neurosurgery_agent",
    description="Neurosurgery specialist: handles surgical treatment of neurological conditions including brain tumors, intracranial hemorrhage, spinal disorders, cerebral aneurysms, hydrocephalus, and traumatic brain injury.",
    instruction=NEUROSURGERY_INSTRUCTION,
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
        intracranial_pressure_assessment,
        spinal_cord_injury_assessment,
        web_search,
    ],
)
