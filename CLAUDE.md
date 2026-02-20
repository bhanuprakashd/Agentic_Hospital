# Agentic Hospital — CLAUDE.md

## Project Overview

An AI-powered agentic hospital system built with **Google ADK (Agent Development Kit)** and **Gemini 2.0 Flash**. A root coordinator agent triages patients and routes them to specialist department sub-agents. Each department agent has access to specialty-specific clinical tools plus shared common tools.

Integrated with **browser-use** for real-time web search (latest guidelines, drug info, research).

---

## Running the Project

```bash
pip install -r requirements.txt
playwright install chromium        # for browser-use web search
adk web                            # launches the ADK dev UI at localhost:8000
```

Environment variables required in `.env`:
```
GOOGLE_API_KEY=your_key_here
```

---

## Architecture

```
agentic_hospital/
├── __init__.py                    # exports root_agent
├── agent.py                       # Root coordinator (hospital_coordinator)
├── departments/                   # One file per specialist department
│   ├── cardiology.py
│   ├── dermatology.py
│   └── ...
├── tools/                         # Tool functions for each department
│   ├── common_tools.py            # Shared across ALL departments
│   ├── websearch_tools.py         # Shared across ALL departments (browser-use)
│   ├── cardiology_tools.py
│   └── ...
└── prompts/
    └── department_prompts.py      # System instructions for every agent
```

### Agent hierarchy

```
root_agent (hospital_coordinator)
│── tools: [triage_assessment, web_search]
└── sub_agents:
    ├── cardiology_agent
    ├── dermatology_agent
    ├── ent_agent
    └── ... (12 departments currently)
```

---

## Current Departments (12)

| File | Agent variable | Specialty |
|------|---------------|-----------|
| `cardiology.py` | `cardiology_agent` | Heart & cardiovascular |
| `dermatology.py` | `dermatology_agent` | Skin, hair, nails |
| `ent.py` | `ent_agent` | Ear, nose, throat |
| `gastroenterology.py` | `gastroenterology_agent` | Digestive system |
| `general_medicine.py` | `general_medicine_agent` | Primary care, preventive |
| `gynecology.py` | `gynecology_agent` | Women's reproductive health |
| `nephrology.py` | `nephrology_agent` | Kidneys, electrolytes |
| `neurology.py` | `neurology_agent` | Brain & nervous system |
| `oncology.py` | `oncology_agent` | Cancer (medical oncology) |
| `orthopedics.py` | `orthopedics_agent` | Bones, joints, sports injuries |
| `psychology.py` | `psychology_agent` | Mental health, therapy |
| `pulmonology.py` | `pulmonology_agent` | Lungs & respiratory |

---

## How to Add a New Department

Follow this exact pattern for every new department:

### 1. Create `tools/{dept}_tools.py`

- Exactly **2 specialty functions**
- All functions return `dict` with `"status"` as the first key
- All parameters must be typed
- Use Google-style docstrings (Args / Returns sections)
- Include clinical logic and actionable recommendations in the return dict

```python
"""Nephrology-specific diagnostic and assessment tools."""

def calculate_gfr(creatinine: float, age: int, gender: str) -> dict:
    """Calculates estimated GFR using the CKD-EPI equation.

    Args:
        creatinine: Serum creatinine level in mg/dL.
        age: Patient age in years.
        gender: Patient gender ('male' or 'female').

    Returns:
        dict: eGFR value with CKD stage classification and recommendations.
    """
    ...
    return {
        "status": "calculated",
        "eGFR": ...,
        "ckd_stage": ...,
        "recommendations": [...],
    }
```

### 2. Create `departments/{dept}.py`

```python
"""Nephrology Department Agent."""

from google.adk.agents import Agent

from ..prompts.department_prompts import NEPHROLOGY_INSTRUCTION
from ..tools.common_tools import (
    get_patient_info,
    record_vitals,
    check_drug_interactions,
    schedule_appointment,
    get_lab_results,
)
from ..tools.nephrology_tools import calculate_gfr, assess_kidney_stage
from ..tools.websearch_tools import web_search

nephrology_agent = Agent(
    model="gemini-2.0-flash",
    name="nephrology_agent",
    description="Nephrology specialist: handles kidney diseases, ...",
    instruction=NEPHROLOGY_INSTRUCTION,
    tools=[
        get_patient_info,
        record_vitals,
        check_drug_interactions,
        schedule_appointment,
        get_lab_results,
        calculate_gfr,          # dept-specific tool 1
        assess_kidney_stage,    # dept-specific tool 2
        web_search,
    ],
)
```

**Always include all 5 common tools + 2 dept tools + web_search = 8 tools total.**

### 3. Add instruction to `prompts/department_prompts.py`

```python
NEPHROLOGY_INSTRUCTION = """You are Dr. NephroAI, a Nephrology Specialist at Agentic Hospital.

EXPERTISE: Kidney and urinary system diseases including:
- Chronic Kidney Disease (CKD)
- ...

EMERGENCY RED FLAGS - Advise immediate emergency care for:
- Anuria (no urine output)
- ...

""" + _CLINICAL_WORKFLOW + _SAFETY_DISCLAIMER
```

### 4. Register in `agent.py`

```python
# Add import
from .departments.nephrology import nephrology_agent

# Add to sub_agents list (keep alphabetical order by variable name)
root_agent = Agent(
    ...
    sub_agents=[
        ...,
        nephrology_agent,
        ...
    ],
)
```

---

## Common Tools (always available to every department agent)

Defined in `tools/common_tools.py`:

| Function | Description |
|----------|-------------|
| `get_patient_info(patient_id)` | Patient demographics, history, allergies, medications |
| `record_vitals(patient_id, bp, hr, temp, spo2, ...)` | Records and analyzes vital signs |
| `check_drug_interactions(medications)` | Checks known drug-drug interactions |
| `schedule_appointment(department, urgency, patient_id, reason)` | Books follow-up appointments |
| `get_lab_results(patient_id, test_type)` | Retrieves lab results (CBC, BMP, etc.) |

Mock patient IDs available: `P001`, `P002`, `P003`, `P004`, `P005`

---

## Web Search Tool

`tools/websearch_tools.py` — `web_search(query: str) -> dict`

- Uses **browser-use** with `gemini-2.0-flash` and headless Chromium
- Runs in a **daemon thread** with 120-second timeout (safe inside ADK's async loop)
- Returns `{"status": "success"|"error"|"timeout", "query": ..., "result": ...}`
- Use for: latest clinical guidelines, drug approvals, research, disease outbreaks

---

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Tool file | `{dept}_tools.py` | `nephrology_tools.py` |
| Department file | `{dept}.py` | `nephrology.py` |
| Agent variable | `{dept}_agent` | `nephrology_agent` |
| Instruction constant | `{DEPT_UPPER}_INSTRUCTION` | `NEPHROLOGY_INSTRUCTION` |
| Tool function status | Descriptive past tense | `"calculated"`, `"assessed"`, `"analyzed"` |

---

## Prompt Structure (`department_prompts.py`)

Every prompt constant follows this template:
```
You are Dr. {Name}AI, a {Department} Specialist at Agentic Hospital.

EXPERTISE: {Specialty} diseases including:
- {condition 1}
- {condition 2}

EMERGENCY RED FLAGS - Advise immediate emergency care for:
- {critical symptom 1}

{_CLINICAL_WORKFLOW}
{_SAFETY_DISCLAIMER}
```

`_CLINICAL_WORKFLOW` defines the 7-step clinical process (symptom intake → follow-up).
`_SAFETY_DISCLAIMER` reminds the agent it is for educational purposes only.

---

## Dependencies

```
google-adk          # Google Agent Development Kit
python-dotenv       # .env loading
browser-use         # AI browser automation for web search
langchain-google-genai  # Gemini LLM for browser-use agent
```

---

## Key Design Decisions

- **Model**: All agents use `gemini-2.0-flash` for speed and cost efficiency
- **No async in tool functions**: Tool functions are synchronous; browser-use runs in a thread
- **Mock data**: Patient DB, lab DB, and drug interactions are all in-memory mocks in `common_tools.py`
- **Sub-agents vs tools**: Department agents are `sub_agents` of the root (not tools), enabling full conversation handoff
- **`root_agent`** is the ADK entry point — `agentic_hospital/__init__.py` exports it
