"""Ophthalmology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.ophthalmology import OPHTHALMOLOGY_INSTRUCTION
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
from ..tools.ophthalmology_tools import (
    vision_assessment,
    glaucoma_risk_assessment,
)
from ..tools.image_tools import analyze_medical_image
from ..tools.websearch_tools import web_search

ophthalmology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="ophthalmology_agent",
    description="Ophthalmology specialist: handles eye conditions and vision disorders including cataracts, glaucoma, macular degeneration, diabetic retinopathy, retinal detachment, and eye trauma. Accepts fundus photos, retinal images, and eye photos.",
    instruction=OPHTHALMOLOGY_INSTRUCTION,
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
        vision_assessment,
        glaucoma_risk_assessment,
        analyze_medical_image,
        web_search,
    ],
)
