# Research Review & Improvement Recommendations
## Agentic Hospital — AI/ML Research Synthesis

> Synthesized from 5 peer-reviewed papers on agentic AI in healthcare (2025–2026).
> All improvement suggestions are grounded in specific research findings cited below.

---

## Table of Contents

1. [Paper Summaries](#1-paper-summaries)
2. [Cross-Paper Themes](#2-cross-paper-themes)
3. [Gap Analysis: Current System vs. Research Benchmarks](#3-gap-analysis)
4. [Improvement Recommendations](#4-improvement-recommendations)
5. [Implementation Roadmap](#5-implementation-roadmap)

---

## 1. Paper Summaries

### Paper 1 — Next-Generation Agentic AI for Transforming Healthcare

| Field | Detail |
|-------|--------|
| **Title** | Next-generation agentic AI for transforming healthcare |
| **Author** | Nalan Karunanayake, Memorial Sloan Kettering Cancer Center |
| **Venue** | *Informatics and Health* 2 (2025) 73–83 |
| **Focus** | Comprehensive survey of agentic AI capabilities and clinical applications |

**Key Findings:**
- Traditional AI is task-specific and rigid; agentic AI is autonomous, adaptive, and can use tools, plan actions, and operate across clinical domains without retraining.
- Technical stack: pretrained deep learning encoders + central LLM reasoning core using Chain-of-Thought (CoT), ReAct, and Tree of Thought (ToT) strategies.
- Diagnostic performance benchmarks: agentic systems achieved **61.4% accuracy** on brain MRI interpretation vs 46.5% for standard internet search — a 32% relative improvement.
- Key functional domains where agentic AI adds value: diagnostics, clinical decision support, treatment planning, patient monitoring, drug discovery, and robotic surgery.
- Recommends **Federated Learning** for privacy-preserving multi-institutional collaboration; **Edge AI** for low-latency deployment at point of care; **Explainable AI (XAI)** for clinical trust and regulatory compliance.
- Identifies seven capability dimensions distinguishing agentic from traditional AI: reasoning approach, domain flexibility, decision structure, data/training method, tool integration, explanation quality, and primary use cases.

**Specific Recommendations from Authors:**
1. Integrate federated learning to enable model improvement without centralizing patient data.
2. Deploy edge AI components for real-time monitoring applications.
3. Implement XAI layers so clinicians can interrogate reasoning at every decision step.
4. Use ReAct (Reasoning + Acting) loops to enable iterative refinement of diagnostic hypotheses.

---

### Paper 2 — Agent Hospital: A Simulacrum of Hospital with Evolvable Medical Agents

| Field | Detail |
|-------|--------|
| **Title** | Agent Hospital: A Simulacrum of Hospital with Evolvable Medical Agents |
| **Authors** | Junkai Li et al., Tsinghua University (AIR/DCST) |
| **Venue** | arXiv:2405.02957v3 (2025) |
| **Focus** | End-to-end hospital simulation for autonomous agent evolution |

**Architecture:**
- Full hospital simulacrum with **16 functional areas**: triage → registration → waiting → consultation → examination → pharmacy → follow-up.
- **42 LLM-powered doctor agents** across 32 departments covering **339 diseases**, plus 4 nurse agents and dynamically generated patient agents.
- Built on Tiled map editor + Phaser web game framework for spatial agent navigation.

**SEAL Paradigm (core contribution):**
The **S**imulacrm-based **E**volutionary **A**gent **L**earning paradigm allows doctor agents to improve autonomously:
1. Synthetic patient agents are generated (disease → symptoms → medical history → report).
2. Doctor agents conduct consultations and make diagnoses.
3. Outcomes are assessed against ground truth.
4. Agent knowledge is updated via in-context learning (no labeled human data required).

**Performance Results:**
| Metric | Before SEAL | After SEAL | Improvement |
|--------|-------------|------------|-------------|
| Cardiology diagnostic accuracy | 52.5% | 96.0% | +43.5 pp |
| MedQA (USMLE subset) | — | **92.22%** | State-of-the-art |

**MedAgent-Zero:** An agent variant that reaches high accuracy with zero manually-labeled training data — all learning is self-supervised through simulation.

**Eight Event Types** modeled: Disease Onset, Triage, Registration, Consultation, Medical Examination, Diagnosis, Medicine Dispensary, Convalescence.

**Specific Recommendations from Authors:**
1. Enable inter-department consultation — complex cases should involve multiple specialists simultaneously, not just sequential routing.
2. Implement parameter-level adaptation (fine-tuning agent prompts/weights based on simulation outcomes).
3. Use automatic patient generation pipelines for continuous agent stress-testing.
4. Model the full care pathway from onset through convalescence, not just diagnosis.

---

### Paper 3 — Agentic AI in Healthcare & Medicine: A Seven-Dimensional Taxonomy

| Field | Detail |
|-------|--------|
| **Title** | Agentic AI in Healthcare & Medicine: A Seven-Dimensional Taxonomy for Empirical Evaluation of LLM-based Agents |
| **Authors** | Shubham Vatsal, Harsh Dubey, Aditi Singh (NYU / Cleveland State) |
| **Venue** | *IEEE Access* (2026), DOI 10.1109/ACCESS.2026.3651218 |
| **Focus** | Systematic review of 49 studies; gaps and best practices |

**Seven Evaluation Dimensions (29 sub-dimensions):**
1. **Cognitive Capabilities** — reasoning depth, multi-step planning, hypothesis generation
2. **Knowledge Management** — external knowledge integration, episodic/procedural memory
3. **Interaction Patterns** — multi-agent coordination, human-in-the-loop, feedback loops
4. **Adaptation & Learning** — drift detection, online learning, event-triggered activation
5. **Safety & Ethics** — bias mitigation, explainability, audit trails, privacy
6. **Framework Typology** — architecture pattern (single-agent vs multi-agent), orchestration
7. **Core Tasks & Subtasks** — diagnosis, triage, treatment planning, documentation

**Critical Gaps Found Across 49 Studies:**

| Gap | Prevalence | Impact |
|----|-----------|--------|
| Drift Detection & Mitigation | **98% absent** | Systems degrade silently over time |
| Event-Triggered Activation | **92% absent** | No reactive response to critical changes |
| Treatment Planning depth | **59% absent** | Diagnosis without full therapeutic follow-through |
| Episodic Memory | **71% absent** | No longitudinal patient context |
| Multi-agent Consultation | **67% absent** | Single-specialist bottleneck |
| Bias Auditing | **84% absent** | Unknown demographic fairness |
| Explainability Layer | **63% absent** | Black-box decisions unacceptable clinically |

**External Knowledge Integration:** Only ~76% of systems fully implement it — 24% rely solely on parametric knowledge (outdated guidelines).

**Specific Recommendations from Authors:**
1. Implement drift detection to monitor for distribution shift in inputs and outputs over time.
2. Add event-triggered agents that activate on critical lab values, vital sign deterioration, or flag words in patient notes.
3. Formalize multi-agent consultation protocols for high-stakes decisions.
4. Include episodic memory so agents recall prior interactions with the same patient.
5. Build standardized evaluation benchmarks for treatment planning, not just diagnosis.

---

### Paper 4 — AI with Agency: A Vision for Adaptive, Efficient, and Ethical Healthcare

| Field | Detail |
|-------|--------|
| **Title** | AI with agency: a vision for adaptive, efficient, and ethical healthcare |
| **Authors** | Hinostroza Fuentes, Abdul Karim, Toledo Tan, AlDahoul |
| **Venue** | *Frontiers in Digital Health* 7:1600216 (May 2025) |
| **Focus** | Economic impact, administrative efficiency, and ethical design of healthcare AI |

**Economic Context:**
- US healthcare consumes 16.8% of GDP; 20% of hospital budgets go to administrative tasks.
- Physicians spend 13% of work time on administrative duties (documentation, scheduling, coding).
- Agentic AI can **reduce cognitive workload by up to 52%** and cut administrative time by **25%**.
- Projected economic benefit: **$100–150 billion annually** from AI-enabled healthcare.
- ROI analysis: **451% return** on AI investment in healthcare settings.

**Administrative Automation Findings:**
- EHR dictation and automated note generation reduces documentation burden by 30–40%.
- AI-driven scheduling reduced no-show rates from **19.3% to 15.9%** (18% relative reduction).
- Insurance claims automation (fraud detection, compliance checking) reduces manual review by 60%.
- Predictive staffing analytics improves shift allocation efficiency.

**Clinical Decision Support:**
- CDSS integration resulted in **5% change in treatment decisions** — indicating measurable clinical impact.
- AI surpassed radiologists in tuberculosis screening, diabetic retinopathy detection, and early cancer detection.
- Sepsis detection in pediatrics: earlier identification reducing mortality.
- Mental health monitoring: passive symptom tracking via NLP on patient-reported data.

**Ethics and Equity:**
- Demographic bias in training data leads to differential performance across patient subgroups.
- Explainability and traceability are prerequisites for regulatory approval (FDA, EU AI Act).
- Human-in-the-loop (HITL) mechanisms required for high-stakes clinical decisions.
- Equity-focused design: systems must be tested across age, gender, ethnicity, and socioeconomic groups.

**Specific Recommendations from Authors:**
1. Implement audit trails for every agent decision — traceable reasoning chains.
2. Add equity metrics to evaluation: measure performance parity across demographic groups.
3. Deploy HITL checkpoints for high-stakes actions (surgery planning, chemotherapy dosing).
4. Automate administrative workflows (scheduling, documentation, billing) alongside clinical ones.
5. Design for explainability from the start, not as an add-on.

---

### Paper 5 — Exploring Agentic AI in Healthcare: A Study on Its Working Mechanism

| Field | Detail |
|-------|--------|
| **Title** | Exploring Agentic AI in Healthcare: A Study on Its Working Mechanism |
| **Authors** | Parvathaneni Naga Srinivasu, Gorli L. Aruna Kumari, Shakeel Ahmed, Abdulaziz Alhumam |
| **Venue** | *Frontiers in Medicine* 12:1753443 (January 2026) |
| **Focus** | Operational framework, coordination mechanisms, 6G integration, SWOT analysis |

**ACRF Framework (core contribution):**
Four-phase operational model for agentic AI systems:
1. **Perception** — data intake from EHRs, sensors, wearables, imaging using NLP encoders and signal processing
2. **Cognition/Reasoning** — knowledge graphs + rule-based systems + probabilistic reasoning for hypothesis generation
3. **Action** — API integrations, robotic control, workflow automation, agent tool calls
4. **Feedback/Learning** — meta-learning, reinforcement learning, continual learning for self-improvement

**Multi-Agent Coordination Mechanisms:**
- Hierarchical orchestration: master coordinator → specialist agents (matches current architecture).
- Peer-to-peer consultation: agents can directly query each other without coordinator mediation.
- Consensus mechanisms: multiple agents vote on diagnosis for high-uncertainty cases.
- Task decomposition: complex clinical questions split into sub-tasks dispatched to specialized agents.

**6G and Edge AI Integration:**
- Ultra-low latency (sub-millisecond) of 6G enables real-time robotic surgery feedback.
- Edge AI deployment allows privacy-preserving computation at device level (no cloud round-trip).
- Federated learning over 6G networks enables continuous model improvement across institutions.

**SWOT Analysis:**

| | Internal | External |
|--|---------|----------|
| **Strengths** | Autonomous reasoning, multi-modal input, tool use, speed | |
| **Weaknesses** | Hallucination risk, bias, lack of common sense, no true understanding | |
| **Opportunities** | | Remote care, global access, personalized medicine, cost reduction |
| **Threats** | | Regulatory barriers, cybersecurity, over-reliance, liability gaps |

**Specific Recommendations from Authors:**
1. Implement governance frameworks with defined accountability for agent actions.
2. Build bias detection pipelines that run continuously on agent outputs.
3. Design privacy-preserving architectures (federated learning, differential privacy).
4. Close the feedback loop — agents must learn from outcomes, not just make predictions.
5. Integrate passive monitoring via wearables and IoT sensors for proactive care.

---

## 2. Cross-Paper Themes

Five themes recur consistently across all papers:

### Theme 1: Agent Evolution and Learning
Papers 2, 5 emphasize that static agents are insufficient. Systems must learn from interactions. Paper 2's SEAL paradigm demonstrates this concretely: simulated patient interactions drive agent improvement without human-labeled data. Paper 5's ACRF framework makes the Feedback phase a first-class architectural concern.

### Theme 2: Multi-Agent Coordination
Papers 2, 3, 5 all highlight that real clinical care is inherently multi-disciplinary. Single-specialist routing (the current Agentic Hospital model) is identified as a major limitation. Papers recommend simultaneous multi-specialist consultation for complex cases.

### Theme 3: Explainability and Trust
Papers 1, 3, 4 all flag explainability as the biggest barrier to clinical adoption. Clinicians will not act on "black-box" recommendations. XAI layers, audit trails, and confidence-annotated outputs are prerequisites.

### Theme 4: Proactive and Event-Driven Care
Paper 3 identifies event-triggered activation as missing in 92% of systems. Papers 1 and 5 emphasize continuous monitoring. Current systems are reactive (respond when asked); clinical AI should be proactive (alert when conditions change).

### Theme 5: Safety, Ethics, and Equity
All 5 papers treat safety and bias as non-optional. Paper 4 provides concrete metrics (performance parity across demographics). Paper 5 frames governance as a prerequisite, not an afterthought.

---

## 3. Gap Analysis

Current Agentic Hospital vs. research benchmarks:

| Research Requirement | Current Status | Gap |
|---------------------|---------------|-----|
| Agent evolution / SEAL | Static prompts only | High |
| Inter-agent consultation | Sequential routing only | High |
| Drift detection | Not implemented | High |
| Event-triggered activation | Not implemented | High |
| Episodic patient memory | Session-only context | High |
| Explainability / reasoning traces | Not implemented | High |
| Treatment planning depth | Diagnosis-focused | Medium |
| Feedback / learning loop | Not implemented | High |
| Administrative automation | SOAP notes added | Low-Medium |
| Drug interaction coverage | 143 entries | Low |
| Patient diversity | 10 patients | Medium |
| Bias auditing | Not implemented | High |
| Human-in-the-loop | Not implemented | Medium |

---

## 4. Improvement Recommendations

The following recommendations are ordered by clinical impact and implementation feasibility.

---

### R1. Multi-Specialist Consultation Mode
**Research basis:** Paper 2 (SEAL inter-department consultation), Paper 3 (67% of systems lack it), Paper 5 (consensus mechanisms)

**Problem:** The current coordinator routes to exactly one department. Complex cases (e.g., diabetic foot ulcer with vascular compromise + infection + renal failure) require simultaneous input from multiple specialists.

**Proposed Implementation:**
```python
# In agent.py or a new consultation_tools.py
def request_multi_specialist_consultation(
    patient_id: str,
    departments: list[str],
    clinical_question: str,
    urgency: str = "routine"
) -> dict:
    """Initiates a multi-disciplinary team (MDT) consultation.

    Dispatches the clinical question to multiple department agents
    in parallel and aggregates their responses into a unified report.
    """
```

The coordinator should recognize "complex case" signals (3+ organ systems, conflicting diagnoses, high-stakes treatment decisions) and invoke MDT mode rather than single routing.

---

### R2. Event-Triggered Alert System
**Research basis:** Paper 3 (92% of systems lack this), Papers 1 and 5 (proactive monitoring)

**Problem:** Agents only respond when a user asks a question. In real hospitals, critical lab values and deteriorating vitals require immediate autonomous alerts.

**Proposed Implementation:**
```python
# New file: tools/monitoring_tools.py

CRITICAL_THRESHOLDS = {
    "potassium": {"low": 2.5, "high": 6.5, "unit": "mEq/L"},
    "sodium": {"low": 120, "high": 160, "unit": "mEq/L"},
    "glucose": {"low": 40, "high": 500, "unit": "mg/dL"},
    "hemoglobin": {"low": 6.0, "unit": "g/dL"},
    "systolic_bp": {"low": 70, "high": 200, "unit": "mmHg"},
    "spo2": {"low": 88, "unit": "%"},
    "heart_rate": {"low": 40, "high": 150, "unit": "bpm"},
    "temperature": {"low": 35.0, "high": 39.5, "unit": "°C"},
}

def monitor_patient_vitals(patient_id: str, interval_seconds: int = 300) -> dict:
    """Continuously monitors patient vitals and triggers alerts on threshold breach."""

def check_critical_lab_values(patient_id: str) -> dict:
    """Scans latest lab results against AACC critical value thresholds."""

def generate_deterioration_alert(patient_id: str, trigger: str, value: float) -> dict:
    """Generates a structured clinical alert with recommended immediate actions."""
```

The pathology agent and critical_care agent should both receive these tools.

---

### R3. Episodic Patient Memory
**Research basis:** Paper 3 (71% of systems lack it), Paper 5 (ACRF Feedback phase)

**Problem:** Each conversation starts fresh with no memory of prior interactions. A patient who was seen last week for chest pain and returns with dyspnea should have their prior consultation available to the agent.

**Proposed Implementation:**
```python
# Enhancement to common_tools.py

_PATIENT_ENCOUNTERS = {}  # patient_id -> list of encounter dicts

def record_patient_encounter(
    patient_id: str,
    department: str,
    chief_complaint: str,
    diagnosis: str,
    plan: list[str],
    follow_up_date: str = None
) -> dict:
    """Records a clinical encounter to the patient's longitudinal history."""

def get_patient_encounter_history(
    patient_id: str,
    last_n: int = 5,
    department_filter: str = None
) -> dict:
    """Retrieves recent encounters for longitudinal context."""
```

Every department agent should call `get_patient_encounter_history` at the start of each consultation and `record_patient_encounter` at the end.

---

### R4. Reasoning Transparency / Explainability Layer
**Research basis:** Paper 1 (XAI recommendation), Paper 3 (63% lack explainability), Paper 4 (audit trails required)

**Problem:** Agents return diagnoses and recommendations without surfacing the reasoning chain. This is a barrier to clinical trust and fails regulatory standards (FDA AI/ML-based SaMD, EU AI Act).

**Proposed Implementation:**
Add a structured `reasoning_trace` field to all specialty tool return dicts:

```python
# Example: enhanced return from anemia_classification
return {
    "status": "classified",
    "hemoglobin": f"{hemoglobin} g/dL",
    "anemia_severity": severity,
    # ... existing fields ...
    "reasoning_trace": [
        {"step": 1, "finding": f"Hgb {hemoglobin} g/dL < threshold {threshold}", "conclusion": f"Anemia present ({severity})"},
        {"step": 2, "finding": f"MCV {mcv} fL < 80", "conclusion": "Microcytic pattern"},
        {"step": 3, "finding": f"Ferritin {ferritin} ng/mL < 30", "conclusion": "Iron deficiency confirmed"},
    ],
    "confidence": "HIGH",  # HIGH / MODERATE / LOW based on data completeness
    "evidence_quality": "Direct laboratory evidence",
    "clinical_guidelines_referenced": ["WHO Hemoglobin Thresholds 2011", "BCSH Guidelines 2017"],
}
```

Also add a new common tool:
```python
def generate_audit_trail(
    patient_id: str,
    agent_name: str,
    action_taken: str,
    reasoning: list[dict],
    tools_used: list[str],
    timestamp: str
) -> dict:
    """Creates a regulatory-compliant audit log entry for agent actions."""
```

---

### R5. SEAL-Inspired Agent Simulation Mode
**Research basis:** Paper 2 (SEAL paradigm — 52.5% → 96% accuracy, MedQA 92.22%)

**Problem:** Agents are static — their diagnostic quality is limited to what the initial prompt encodes. The SEAL paradigm shows that agents evolved through simulated clinical encounters achieve state-of-the-art performance.

**Proposed Implementation:**
Create a simulation module for stress-testing and improving agent prompts:

```python
# New file: simulation/patient_generator.py

DISEASE_LIBRARY = {
    "cardiology": [
        {
            "disease": "STEMI",
            "typical_presentation": {"chest_pain": True, "radiation_to_jaw": True, "diaphoresis": True},
            "lab_findings": {"troponin": 15.2, "ck_mb": 45},
            "ecg_findings": "ST elevation V1-V4",
            "correct_diagnosis": "ST-elevation myocardial infarction",
            "correct_immediate_action": "Activate cath lab, dual antiplatelet, anticoagulation"
        },
        # ... 50+ diseases per department
    ]
}

def generate_synthetic_patient(department: str, difficulty: str = "moderate") -> dict:
    """Generates a synthetic patient case for agent simulation."""

def evaluate_agent_response(agent_response: str, expected: dict) -> dict:
    """Scores agent diagnosis and management plan against gold standard."""

def run_simulation_batch(department: str, n_cases: int = 100) -> dict:
    """Runs n_cases through a department agent and returns accuracy metrics."""
```

This allows continuous benchmarking: run the simulation suite before and after any prompt change to verify improvement.

---

### R6. Drift Detection and Output Monitoring
**Research basis:** Paper 3 (98% of systems lack this — the most critical gap)

**Problem:** As LLM models update and patient data distributions shift, agent output quality can degrade silently. No mechanism currently detects this.

**Proposed Implementation:**
```python
# New file: tools/quality_tools.py

_BASELINE_METRICS = {}  # department -> {"accuracy": float, "confidence_mean": float}

def log_diagnostic_outcome(
    patient_id: str,
    department: str,
    agent_diagnosis: str,
    confirmed_diagnosis: str,
    confidence: str
) -> dict:
    """Logs diagnostic outcome for drift tracking."""

def compute_drift_metrics(
    department: str,
    window_days: int = 30
) -> dict:
    """Computes rolling accuracy, confidence calibration, and drift indicators.

    Returns drift_alert=True if accuracy drops >10pp from baseline
    or confidence-accuracy gap exceeds 0.15.
    """

def generate_quality_report(department: str = "all") -> dict:
    """Generates a quality and safety report for clinical governance review."""
```

---

### R7. Human-in-the-Loop (HITL) Checkpoints
**Research basis:** Paper 4 (HITL for high-stakes decisions), Paper 3 (Safety & Ethics dimension)

**Problem:** All agent actions are fully autonomous. For high-stakes actions (chemotherapy dose calculation, surgery planning, high-risk drug interactions), a clinician approval step should be required.

**Proposed Implementation:**
Add an `approval_required` flag to tools that carry high risk:

```python
# Enhancement to calculate_medication_dose and radiation dose tools
return {
    "status": "calculated",
    "dose": ...,
    # ... fields ...
    "approval_required": True,  # Flag for HITL
    "approval_reason": "High-risk medication requiring clinical verification",
    "approval_checklist": [
        "Verify patient weight independently",
        "Confirm renal function with latest creatinine",
        "Check for contraindications in allergy list",
        "Document indication and informed consent"
    ],
    "regulatory_class": "HIGH_RISK_MEDICATION"
}
```

The coordinator agent should be instructed to surface `approval_required=True` responses prominently and explicitly request clinician sign-off before proceeding.

---

### R8. Patient Outcome Tracking and Feedback Loop
**Research basis:** Paper 5 (ACRF Feedback phase), Paper 2 (SEAL learning loop), Paper 3 (Adaptation & Learning dimension)

**Problem:** The system generates plans but never learns whether they worked. Closing the loop would enable continuous quality improvement aligned with SEAL.

**Proposed Implementation:**
```python
# Enhancement to common_tools.py

_OUTCOME_REGISTRY = []

def record_treatment_outcome(
    patient_id: str,
    diagnosis: str,
    treatment_plan: list[str],
    outcome: str,           # "resolved", "improved", "unchanged", "deteriorated", "adverse_event"
    days_to_outcome: int,
    complications: list[str] = None
) -> dict:
    """Records treatment outcome for quality improvement analysis."""

def get_department_outcome_summary(department: str) -> dict:
    """Returns outcome statistics for a department: resolution rates,
    average time-to-improvement, adverse event rate."""
```

---

### R9. Enhanced Treatment Planning Depth
**Research basis:** Paper 3 (59% of systems lack adequate treatment planning), Paper 2 (full care pathway from onset through convalescence)

**Problem:** Most current tools are assessment-focused (diagnose the condition) but do not generate complete treatment plans with monitoring parameters, dose titration schedules, or follow-up protocols.

**Proposed Enhancement:**
Each specialty tool should return a `treatment_protocol` section:

```python
# Example: add to anemia_classification return dict
"treatment_protocol": {
    "iron_deficiency": {
        "first_line": "Ferrous sulfate 325mg TID with vitamin C",
        "duration": "3-6 months after Hgb normalizes to replete stores",
        "monitoring": ["CBC at 4 weeks (expect Hgb +1-2 g/dL/month)", "Ferritin at 3 months (target >50)"],
        "iv_iron_criteria": "Intolerance to oral, malabsorption, or Hgb <7 with symptoms",
        "transfusion_threshold": "Hgb <7 g/dL or <8 with cardiac disease",
        "follow_up": "Repeat CBC 4 weeks, then 3 months, then annually"
    }
}
```

Create a standalone treatment planning tool:
```python
def generate_treatment_plan(
    diagnosis: str,
    severity: str,
    patient_id: str,
    contraindications: list[str] = None
) -> dict:
    """Generates evidence-based treatment protocols with monitoring parameters,
    dose schedules, and follow-up timelines."""
```

---

### R10. Equity and Bias Monitoring
**Research basis:** Paper 4 (equity focus), Paper 5 (bias detection pipelines), Paper 3 (Safety & Ethics dimension)

**Problem:** Clinical algorithms (e.g., GFR calculation with race coefficient, Apgar scoring differences, cardiovascular risk scores) have known demographic biases. No monitoring exists.

**Proposed Implementation:**
```python
# New file: tools/equity_tools.py

KNOWN_BIASES = {
    "eGFR": "Historical race coefficient removed in CKD-EPI 2021; verify tool uses race-free equation",
    "pulmonary_function": "Spirometry reference equations differ by race; NHANES III vs GLI 2012",
    "pain_assessment": "Studies show Black patients receive less analgesia; flag for equitable treatment",
    "cardiovascular_risk": "Pooled Cohort Equations may overestimate risk in some populations",
}

def audit_tool_for_bias(tool_name: str, patient_demographics: dict) -> dict:
    """Checks if a clinical tool has known demographic biases relevant to this patient
    and surfaces them as warnings."""

def generate_equity_report(
    department: str,
    date_range_days: int = 90
) -> dict:
    """Analyzes whether treatment recommendations differ significantly
    by patient age, gender, or ethnicity."""
```

---

### R11. Federated Learning Architecture (Long-Term)
**Research basis:** Papers 1, 5 (federated learning for privacy), Paper 4 (multi-institutional collaboration)

**Problem:** All patient data is in a single in-memory store. Real deployment requires privacy-preserving data handling across multiple hospital systems.

**Architectural Vision:**
```
Hospital A ──► Local Model Update ──►┐
Hospital B ──► Local Model Update ──►├──► Federated Aggregation Server ──► Global Model Update
Hospital C ──► Local Model Update ──►┘
```

**Near-term steps:**
1. Separate the patient database into a proper data access layer (repository pattern).
2. Add data anonymization utilities (`anonymize_patient_record`).
3. Design the database interface to be swappable (mock → real EHR → federated).

```python
# New file: data/patient_repository.py
class PatientRepository:
    """Abstract interface — mock implementation today, federated tomorrow."""
    def get_patient(self, patient_id: str) -> dict: ...
    def get_lab_results(self, patient_id: str, test_type: str) -> dict: ...
    def record_vitals(self, patient_id: str, vitals: dict) -> dict: ...
    def anonymize(self, patient_record: dict) -> dict: ...
```

---

### R12. External Knowledge Integration via RAG
**Research basis:** Paper 3 (~24% of systems rely only on parametric knowledge — outdated guidelines)

**Problem:** The web_search tool is valuable but unstructured. Clinical guidelines change and agents should pull from authoritative, versioned sources.

**Proposed Enhancement:**
Create a structured clinical guidelines retrieval tool:

```python
# Enhancement to websearch_tools.py

GUIDELINE_SOURCES = {
    "cardiology": "ACC/AHA guidelines (latest year)",
    "oncology": "NCCN guidelines",
    "infectious_disease": "IDSA guidelines",
    "diabetes": "ADA Standards of Care",
    "hypertension": "JNC 8 / ACC AHA 2017",
    "anticoagulation": "CHEST guidelines",
}

def search_clinical_guidelines(
    topic: str,
    specialty: str,
    evidence_level: str = "A"
) -> dict:
    """Searches authoritative clinical guidelines with structured output including
    evidence grading, publication year, and recommendation strength."""
```

---

## 5. Implementation Roadmap

### Phase 1 — Quick Wins (1-2 weeks)
*Low complexity, high clinical impact:*
- **R4**: Add `reasoning_trace` and `confidence` fields to all specialty tools
- **R9**: Add `treatment_protocol` sections to existing assessment tools
- **R3**: Add `record_patient_encounter` and `get_patient_encounter_history` to `common_tools.py`
- **R7**: Add `approval_required` flags to `calculate_medication_dose` and `calculate_radiation_dose`

### Phase 2 — Core Intelligence (2-4 weeks)
*Medium complexity, foundational capabilities:*
- **R1**: Build `request_multi_specialist_consultation` tool + update coordinator instruction
- **R2**: Create `monitoring_tools.py` with event-triggered alerts
- **R8**: Build `record_treatment_outcome` and feedback analytics
- **R12**: Enhance web search with structured guideline retrieval

### Phase 3 — Advanced Capabilities (1-2 months)
*High complexity, research-grade features:*
- **R5**: Build `simulation/patient_generator.py` (SEAL-inspired) with 30+ disease cases per department
- **R6**: Create `quality_tools.py` with drift detection and rolling accuracy metrics
- **R10**: Build `equity_tools.py` with bias auditing for known clinical algorithm biases

### Phase 4 — Production Readiness (2-3 months)
*Architectural improvements for real-world deployment:*
- **R11**: Refactor to repository pattern + federated learning architecture
- Full audit trail system + governance dashboard
- Integration with real EHR systems (FHIR API)
- Regulatory compliance documentation (FDA SaMD pathway)

---

## Summary of Key Metrics to Achieve

Based on research paper benchmarks, target performance goals:

| Metric | Current | Target (Research-Grounded) | Source |
|--------|---------|---------------------------|--------|
| Diagnostic accuracy (post-simulation) | Unknown | >85% (vs 92.22% SEAL on MedQA) | Paper 2 |
| Departments with MDT consultation | 0/35 | 35/35 | Papers 2, 3 |
| Tools with reasoning traces | 0% | 100% | Papers 1, 3, 4 |
| Treatment protocol coverage | ~20% | >90% | Paper 3 |
| Drift monitoring | None | Rolling 30-day window | Paper 3 |
| Patient encounter memory | Session-only | Persistent longitudinal | Paper 3 |
| Equity audit coverage | None | All tools with demographic bias flags | Papers 4, 5 |
| Drug interactions database | 143 entries | 500+ entries (clinical completeness) | Clinical standard |

---

*Report compiled: 2026-02-19*
*Based on: 5 peer-reviewed papers (2025–2026), 49 empirical studies reviewed therein*
*Project: Agentic Hospital — Google ADK + Gemini 2.0 Flash*
