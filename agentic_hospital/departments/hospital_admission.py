"""Hospital Admission & Bed Management Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.hospital_admission import HOSPITAL_ADMISSION_INSTRUCTION
from ..tools.common_tools import (
    get_patient_info,
    record_patient_encounter,
    get_patient_encounter_history,
)
from ..tools.bed_management_tools import (
    get_hospital_dashboard,
    get_ward_visualization,
    check_bed_availability,
    assign_bed,
    discharge_patient_from_bed,
    transfer_patient_bed,
    add_to_waitlist,
    get_waitlist_status,
)

hospital_admission_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="hospital_admission_agent",
    description=(
        "Hospital Admission & Bed Management coordinator: handles patient admissions, "
        "bed assignments, discharges, inter-ward transfers, priority waitlist management, "
        "and real-time hospital capacity visualisation across all 20 inpatient wards "
        "(325 beds). Generates ASCII ward floor-plan maps and markdown hospital dashboards."
    ),
    instruction=HOSPITAL_ADMISSION_INSTRUCTION,
    tools=[
        get_patient_info,
        record_patient_encounter,
        get_patient_encounter_history,
        get_hospital_dashboard,
        get_ward_visualization,
        check_bed_availability,
        assign_bed,
        discharge_patient_from_bed,
        transfer_patient_bed,
        add_to_waitlist,
        get_waitlist_status,
    ],
)
