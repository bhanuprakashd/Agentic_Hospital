"""Physical Medicine and Rehabilitation Department Agent."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.physical_medicine_rehab import PHYSICAL_MEDICINE_REHAB_INSTRUCTION
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
from ..tools.physical_medicine_rehab_tools import (
    functional_independence_assessment,
    stroke_rehabilitation_prognosis,
)
from ..tools.websearch_tools import web_search

physical_medicine_rehab_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="physical_medicine_rehab_agent",
    description="Physical Medicine and Rehabilitation specialist: handles rehabilitation and functional restoration including stroke rehab, spinal cord injury rehab, TBI rehab, amputee rehab, pain management, and electrodiagnostic medicine.",
    instruction=PHYSICAL_MEDICINE_REHAB_INSTRUCTION,
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
        functional_independence_assessment,
        stroke_rehabilitation_prognosis,
        web_search,
    ],
)
