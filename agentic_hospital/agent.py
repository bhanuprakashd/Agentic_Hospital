"""Root Hospital Coordinator Agent - Routes patients to specialist departments."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .prompts.coordinator import COORDINATOR_INSTRUCTION
from .tools.common_tools import (
    get_patient_info,
    triage_assessment,
    request_mdt_consultation,
    generate_treatment_plan,
    get_patient_encounter_history,
    record_patient_encounter,
)
from .tools.monitoring_tools import check_critical_lab_values, generate_deterioration_alert
from .tools.image_tools import analyze_medical_image
from .tools.websearch_tools import web_search

# ---- Department imports (alphabetical) ----
from .departments.allergy_immunology import allergy_immunology_agent
from .departments.anesthesiology import anesthesiology_agent
from .departments.cardiology import cardiology_agent
from .departments.cardiothoracic_surgery import cardiothoracic_surgery_agent
from .departments.colorectal_surgery import colorectal_surgery_agent
from .departments.critical_care import critical_care_agent
from .departments.dermatology import dermatology_agent
from .departments.emergency_medicine import emergency_medicine_agent
from .departments.endocrinology import endocrinology_agent
from .departments.ent import ent_agent
from .departments.gastroenterology import gastroenterology_agent
from .departments.general_medicine import general_medicine_agent
from .departments.general_surgery import general_surgery_agent
from .departments.gynecology import gynecology_agent
from .departments.hematology import hematology_agent
from .departments.hospital_admission import hospital_admission_agent
from .departments.infectious_diseases import infectious_diseases_agent
from .departments.nephrology import nephrology_agent
from .departments.neurology import neurology_agent
from .departments.neurosurgery import neurosurgery_agent
from .departments.nuclear_medicine import nuclear_medicine_agent
from .departments.oncology import oncology_agent
from .departments.ophthalmology import ophthalmology_agent
from .departments.orthopedics import orthopedics_agent
from .departments.pathology import pathology_agent
from .departments.pediatrics import pediatrics_agent
from .departments.physical_medicine_rehab import physical_medicine_rehab_agent
from .departments.pharmacy import pharmacy_agent
from .departments.plastic_surgery import plastic_surgery_agent
from .departments.psychology import psychology_agent
from .departments.pulmonology import pulmonology_agent
from .departments.radiation_oncology import radiation_oncology_agent
from .departments.radiology import radiology_agent
from .departments.rheumatology import rheumatology_agent
from .departments.thoracic_surgery import thoracic_surgery_agent
from .departments.triage_nurse import triage_nurse_agent
from .departments.urology import urology_agent
from .departments.vascular_surgery import vascular_surgery_agent
from .departments.discharge_planning import discharge_planning_agent
root_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="hospital_coordinator",
    description=(
        "Main Hospital Coordinator AI at Agentic Hospital. "
        "Triages patients, performs initial assessment, and routes to the most appropriate "
        "specialist department from 35 available specialties. "
        "Accepts both text and image inputs (photos, scans, X-rays, ECGs, etc.)."
    ),
    instruction=COORDINATOR_INSTRUCTION,
    tools=[
        get_patient_info,
        get_patient_encounter_history,
        check_critical_lab_values,
        triage_assessment,
        request_mdt_consultation,
        generate_treatment_plan,
        record_patient_encounter,
        generate_deterioration_alert,
        analyze_medical_image,
        web_search,
    ],
    sub_agents=[
        triage_nurse_agent,          # first contact — ESI triage before any specialist
        allergy_immunology_agent,
        anesthesiology_agent,
        cardiology_agent,
        cardiothoracic_surgery_agent,
        colorectal_surgery_agent,
        critical_care_agent,
        dermatology_agent,
        discharge_planning_agent,
        emergency_medicine_agent,
        endocrinology_agent,
        ent_agent,
        gastroenterology_agent,
        general_medicine_agent,
        general_surgery_agent,
        gynecology_agent,
        hematology_agent,
        hospital_admission_agent,
        infectious_diseases_agent,
        nephrology_agent,
        neurology_agent,
        neurosurgery_agent,
        nuclear_medicine_agent,
        oncology_agent,
        ophthalmology_agent,
        orthopedics_agent,
        pathology_agent,
        pediatrics_agent,
        pharmacy_agent,
        physical_medicine_rehab_agent,
        plastic_surgery_agent,
        psychology_agent,
        pulmonology_agent,
        radiation_oncology_agent,
        radiology_agent,
        rheumatology_agent,
        thoracic_surgery_agent,
        urology_agent,
        vascular_surgery_agent,
    ],
)
