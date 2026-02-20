"""Radiology Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.radiology import RADIOLOGY_INSTRUCTION
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
from ..tools.radiology_tools import imaging_study_selector, report_critical_findings
from ..tools.image_tools import analyze_medical_image
from ..tools.websearch_tools import web_search

radiology_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="radiology_agent",
    description="Radiology specialist: applies ACR Appropriateness Criteria to select optimal imaging modality (X-ray, CT, MRI, ultrasound, PET/CT), interprets critical findings, and communicates urgent results per Joint Commission standards. Accepts X-ray, CT, MRI, ultrasound, and PET/CT images.",
    instruction=RADIOLOGY_INSTRUCTION,
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
        imaging_study_selector,
        report_critical_findings,
        analyze_medical_image,
        web_search,
    ],
)
