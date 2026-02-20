"""Vascular Surgery Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.vascular_surgery import VASCULAR_SURGERY_INSTRUCTION
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
from ..tools.vascular_surgery_tools import (
    peripheral_arterial_disease_assessment,
    aortic_aneurysm_assessment,
)
from ..tools.websearch_tools import web_search

vascular_surgery_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="vascular_surgery_agent",
    description="Vascular Surgery specialist: handles blood vessel disorders including abdominal aortic aneurysm, peripheral arterial disease, carotid disease, DVT, varicose veins, acute limb ischemia, and diabetic foot ulcers.",
    instruction=VASCULAR_SURGERY_INSTRUCTION,
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
        peripheral_arterial_disease_assessment,
        aortic_aneurysm_assessment,
        web_search,
    ],
)
