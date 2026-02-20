"""Nurse Triage Agent — Emergency Severity Index (ESI v4) triage station."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.triage_nurse import TRIAGE_NURSE_INSTRUCTION
from ..tools.common_tools import get_patient_info
from ..tools.triage_tools import (
    calculate_esi_score,
    record_nurse_triage,
    assign_waiting_priority,
    get_triage_queue,
)

triage_nurse_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="triage_nurse_agent",
    description=(
        "Senior ED Triage Nurse at Agentic Hospital. "
        "First clinical contact for every patient — performs ESI v4 triage scoring, "
        "records vital signs and chief complaint, assigns waiting priority, and "
        "produces a structured triage summary for the receiving physician. "
        "Routes ESI 1–2 patients to emergency/critical care; ESI 3–5 to appropriate "
        "specialist via the coordinator."
    ),
    instruction=TRIAGE_NURSE_INSTRUCTION,
    tools=[
        get_patient_info,
        calculate_esi_score,
        record_nurse_triage,
        assign_waiting_priority,
        get_triage_queue,
    ],
)
