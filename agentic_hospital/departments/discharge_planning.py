"""Discharge Planning Agent — manages patient discharge process."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from ..prompts.discharge_planning import DISCHARGE_PLANNING_INSTRUCTION
from ..tools.common_tools import get_patient_info
from ..tools.discharge_tools import (
    check_discharge_criteria,
    generate_discharge_summary,
    send_gp_letter,
    arrange_community_services,
)

discharge_planning_agent = Agent(
    model=LiteLlm(model="openrouter/google/gemini-2.5-flash-lite"),
    name="discharge_planning_agent",
    description=(
        "Discharge Planning Coordinator at Agentic Hospital. "
        "Manages the full discharge process: assesses discharge readiness, generates "
        "discharge summaries, coordinates TTA medications with pharmacy, sends GP letters, "
        "arranges community services (district nursing, physiotherapy, OT, social work), "
        "and schedules follow-up appointments."
    ),
    instruction=DISCHARGE_PLANNING_INSTRUCTION,
    tools=[
        get_patient_info,
        check_discharge_criteria,
        generate_discharge_summary,
        send_gp_letter,
        arrange_community_services,
    ],
)
