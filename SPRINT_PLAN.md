# Agentic Hospital — Sprint Plan

**Created:** 2026-02-20
**Baseline:** 38 agents · 101 tools · 325 beds · 20 wards
**Goal:** Close the gap between current simulation and a real-world hospital workflow

---

## Gap Summary (Current vs. Real Hospital)

| Phase | Real Hospital | Current System | Status |
|-------|--------------|----------------|--------|
| Pre-hospital | EMS, GP referral, ambulance pre-notify | Walk-in only | ❌ Missing |
| Registration | Admin, insurance, wristband, consent | Patient ID lookup | ⚠️ Partial |
| Nurse triage | ESI/MTS score, vitals, risk screens — before doctor | triage_nurse_agent performs ESI v4 | ✅ Complete (Sprint 1) |
| Waiting room | Queue by acuity, wait time display | Implemented in triage_tools | ✅ Complete (Sprint 1) |
| Nursing assessment | Full nursing Hx, VTE/falls/skin risk | None | ❌ Missing |
| Physical examination | Documented exam findings | Symptom history only | ❌ Missing |
| Diagnostic ordering | Order → phlebotomy → result → notify chain | order_investigation() workflow | ✅ Complete (Sprint 4) |
| Radiology workflow | Request → scan → radiologist report | AI image analysis only | ⚠️ Partial |
| Specialist consultation | Formal referral letter, documented response | Direct routing | ⚠️ Partial |
| Disposition decision | Formal admit/discharge/transfer tool | Implicit in specialist response | ❌ Missing |
| Admission orders | Diagnosis, meds, diet, monitoring, VTE prophylaxis | `assign_bed` only | ❌ Missing |
| Medication reconciliation | Home meds vs. new prescriptions at admission + discharge | pharmacy_agent reconciliation | ✅ Complete (Sprint 2) |
| Pharmacy | Pharmacist verify, dispense, counsel | pharmacy_agent verification & dispensing | ✅ Complete (Sprint 2) |
| Inpatient nursing | 4-hourly vitals, care plan, med rounds, nursing notes | None after admission | ❌ Missing |
| Ward rounds | Daily consultant + team round, progress notes | None | ❌ Missing |
| MDT | Structured meeting with case presentations | Stub only | ⚠️ Partial |
| Theatre/procedure | OR booking, safety checklist, post-op orders | None | ❌ Missing |
| Discharge process | Criteria, summary, TTA meds, GP letter, community | discharge_planning_agent | ✅ Complete (Sprint 3) |
| Post-discharge | GP informed, rehab, community nursing, readmission tracking | None | ❌ Missing |

---

## Sprint Overview

| Sprint | Focus | New Agents | New Tools | Status |
|--------|-------|-----------|-----------|--------|
| Sprint 1 | Nurse Triage | `triage_nurse_agent` | 3 | ✅ Complete |
| Sprint 2 | Pharmacy | `pharmacy_agent` | 4 | ✅ Complete |
| Sprint 3 | Discharge Planning | `discharge_planning_agent` | 4 | ✅ Complete |
| Sprint 4 | Diagnostic Ordering | — (extend existing) | 3 | ✅ Complete |
| Sprint 5 | Inpatient Nursing + Ward Rounds | `ward_nurse_agent` | 5 | 🔲 Planned |
| Sprint 6 | Theatre & Procedures | `theatre_scheduling_agent` | 4 | 🔲 Planned |
| Sprint 7 | Risk Assessments | — (add to existing) | 5 | 🟡 Medium |
| Sprint 8 | GP Referral & Pre-hospital | `gp_referral_agent`, `ems_agent` | 3 | 🟡 Medium |
| Sprint 9 | Infection Control & Safety | — (extend existing) | 4 | 🟢 Lower |
| Sprint 10 | Data Persistence & EHR | — (infrastructure) | — | 🟢 Lower |

---

## Sprint 1 — Nurse Triage Agent

**Why first:** In every real hospital, a triage nurse assesses the patient *before* any doctor.
The ESI/MTS score determines queue position and urgency. Currently the AI coordinator skips
this step entirely — the most fundamental gap in the clinical workflow.

**Status:** ✅ Complete (2026-02-20)

### New Agent

| Agent | Variable | Role |
|-------|----------|------|
| Triage Nurse | `triage_nurse_agent` | First point of clinical contact. Performs ESI scoring, records vitals, applies risk screens, assigns waiting priority before physician sees patient. |

### New Tools — `tools/triage_tools.py`

| Function | Description |
|----------|-------------|
| `calculate_esi_score(symptoms, vitals, arrival_mechanism)` | Returns ESI level 1–5 with colour, target time-to-physician, and rationale using Emergency Severity Index v4 |
| `record_nurse_triage(patient_id, vitals, pain_score, chief_complaint, esi_level)` | Documents full nurse triage assessment including allergy verification and wristband flag |
| `assign_waiting_priority(patient_id, esi_level)` | Places patient in acuity queue; ESI 1–2 bypass waiting room to resuscitation bay |

### Updated Workflow After Sprint 1

```
Patient arrives
     │
     ▼
Registration (coordinator — existing)
     │
     ▼
triage_nurse_agent  ← NEW
  ├─ calculate_esi_score()       → ESI 1–5
  ├─ record_nurse_triage()       → vitals, pain, allergy check
  └─ assign_waiting_priority()   → queue or direct to resus bay
     │
     ├─ ESI 1–2 → resuscitation bay → emergency_medicine_agent (immediate)
     └─ ESI 3–5 → waiting room queue → coordinator routes to specialist
```

### Files to Create / Modify

```
agentic_hospital/
├── tools/triage_tools.py                  (new)
├── departments/triage_nurse.py            (new)
├── prompts/triage_nurse.py                (new)
└── agent.py                               (register triage_nurse_agent)
```

---

## Sprint 2 — Pharmacy Agent

**Why second:** Medications are recommended by specialist agents but never verified or dispensed.
Pharmacist reconciliation at admission and discharge is a legal and clinical safety requirement
in every real hospital. Drug errors are the most common preventable adverse event.

**Status:** 🔲 Planned

### New Agent

| Agent | Variable | Role |
|-------|----------|------|
| Pharmacy | `pharmacy_agent` | Verifies all medication orders, checks formulary, performs medication reconciliation at admission and discharge, dispenses TTA (To Take Away) medications. |

### New Tools — `tools/pharmacy_tools.py`

| Function | Description |
|----------|-------------|
| `verify_medication_order(patient_id, medication, dose, route, frequency)` | Validates against formulary, checks allergies, renal/hepatic dose adjustment, flags contraindications |
| `dispense_medication(patient_id, medication, dose, quantity, instructions)` | Records dispensing event with batch number, expiry, pharmacist sign-off |
| `medication_reconciliation(patient_id, stage)` | Compares home medications vs. current inpatient orders; stage = `"admission"` or `"discharge"` — flags omissions, duplications, interactions |
| `generate_tta_prescription(patient_id, discharge_medications)` | Generates To Take Away prescription with dose, duration, administration instructions, warning signs |

### Updated Workflow After Sprint 2

```
Specialist recommends medication
     │
     ▼
pharmacy_agent  ← NEW
  ├─ verify_medication_order()       → allergy + formulary + renal adjustment check
  ├─ dispense_medication()           → dispensing record
  └─ medication_reconciliation()     → admission: home meds vs. prescribed
                                        discharge: TTA vs. inpatient orders
```

### Files to Create / Modify

```
agentic_hospital/
├── tools/pharmacy_tools.py                (new)
├── departments/pharmacy.py                (new)
├── prompts/pharmacy.py                    (new)
└── agent.py                               (register pharmacy_agent)
```

---

## Sprint 3 — Discharge Planning Agent

**Why third:** Currently patients have no formal exit pathway. There is no discharge summary,
no GP letter, no TTA medications, no community referral. In a real hospital, discharge planning
begins on day 1 of admission and involves coordination across clinical, social, and community teams.

**Status:** 🔲 Planned

### New Agent

| Agent | Variable | Role |
|-------|----------|------|
| Discharge Planning | `discharge_planning_agent` | Manages the full discharge process: criteria assessment, discharge summary, TTA medications, GP letter, community service referrals, follow-up booking, transport. |

### New Tools — `tools/discharge_tools.py`

| Function | Description |
|----------|-------------|
| `generate_discharge_summary(patient_id, admitting_diagnosis, final_diagnosis, investigations, treatment, tta_medications, follow_up_plan)` | Structured discharge summary covering: admission Hx, clinical course, investigations + results, procedures, discharge medications, follow-up plan |
| `send_gp_letter(patient_id, gp_name, summary, urgent_actions)` | Generates and sends discharge letter to GP with key findings, medication changes, and actions required |
| `arrange_community_services(patient_id, services_required)` | Refers to district nursing, physiotherapy, occupational therapy, social work, palliative care, mental health community team |
| `check_discharge_criteria(patient_id, clinical_criteria)` | Validates patient meets discharge criteria: haemodynamically stable, pain controlled, safe to mobilise, appropriate home support |

### Updated Workflow After Sprint 3

```
Inpatient stay complete
     │
     ▼
discharge_planning_agent  ← NEW
  ├─ check_discharge_criteria()          → clinical sign-off
  ├─ generate_discharge_summary()        → structured document
  ├─ pharmacy_agent.generate_tta()       → TTA medications
  ├─ send_gp_letter()                    → notify primary care
  ├─ arrange_community_services()        → rehab, nursing, social
  └─ schedule_appointment()             → outpatient follow-up
     │
     ▼
discharge_patient_from_bed()  →  bed status: cleaning
     │
     ▼
🏠 Patient discharged
```

### Files to Create / Modify

```
agentic_hospital/
├── tools/discharge_tools.py              (new)
├── departments/discharge_planning.py     (new)
├── prompts/discharge_planning.py         (new)
└── agent.py                              (register discharge_planning_agent)
```

---

## Sprint 4 — Diagnostic Ordering Workflow

**Why fourth:** Lab results and imaging are currently retrieved as if they already exist.
There is no order → processing → result chain. A real diagnostic workflow has discrete states
and a critical value notification chain tied to the ordering clinician.

**Status:** 🔲 Planned

### Approach
Extend `common_tools.py` and `monitoring_tools.py` — no new agent required.
Add order management layer on top of existing `get_lab_results` and `analyze_medical_image`.

### New Tools — extend `tools/common_tools.py`

| Function | Description |
|----------|-------------|
| `order_investigation(patient_id, investigation_type, clinical_indication, urgency)` | Places investigation order with status `"ordered"`. Types: blood panel, imaging, ECG, urine, cultures, biopsy |
| `get_pending_results(patient_id)` | Returns all ordered investigations with current status: `ordered → processing → resulted → reviewed` |
| `acknowledge_critical_result(patient_id, investigation_id, clinician_id)` | Records that ordering clinician has acknowledged a critical value — closes the notification loop |

### Order State Machine

```
ordered  →  processing  →  resulted  →  reviewed
                               │
                    critical value detected?
                               │
                    generate_deterioration_alert()
                    notify ordering clinician
                    require acknowledge_critical_result()
```

### Files to Modify

```
agentic_hospital/
├── tools/common_tools.py                  (add 3 order management functions)
├── tools/monitoring_tools.py              (tie critical alerts to order IDs)
└── prompts/shared.py                      (update _TOOL_PROTOCOL with ordering step)
```

---

## Sprint 5 — Inpatient Nursing Agent & Ward Rounds

**Why fifth:** After admission, the current system goes silent. No vitals are recorded,
no nursing care occurs, no medications are given, no progress notes are written, and no
ward round happens. In reality, inpatient nursing is continuous and ward rounds happen daily.

**Status:** 🔲 Planned

### New Agent

| Agent | Variable | Role |
|-------|----------|------|
| Ward Nurse | `ward_nurse_agent` | Provides continuous inpatient nursing: 4-hourly vitals, nursing care plan, medication rounds, wound care, nursing notes, shift handover (SBAR). |

### New Tools — `tools/nursing_tools.py`

| Function | Description |
|----------|-------------|
| `record_nursing_assessment(patient_id, assessment_type, findings)` | Documents admission nursing assessment, daily assessment, and focused assessments |
| `create_care_plan(patient_id, nursing_diagnoses, goals, interventions)` | Creates structured nursing care plan with measurable goals and nursing interventions |
| `record_nursing_note(patient_id, shift, note_type, content)` | Documents nursing observations, patient response to treatment, concerns |
| `generate_sbar_handover(patient_id, from_nurse, to_nurse, shift)` | Structured Situation-Background-Assessment-Recommendation handover between nursing shifts |
| `record_medication_administration(patient_id, medication, dose, time, route, nurse_id)` | Documents medication administration event with verification and patient response |

### Ward Round Simulation

Add `conduct_ward_round(ward, date)` to `bed_management_tools.py`:
- Iterates over occupied beds
- For each patient: retrieves current status, outstanding results, nursing notes
- Generates daily progress note per patient
- Flags deteriorating patients for escalation

### Files to Create / Modify

```
agentic_hospital/
├── tools/nursing_tools.py                 (new — 5 functions)
├── departments/ward_nurse.py              (new)
├── prompts/ward_nurse.py                  (new)
├── tools/bed_management_tools.py          (add conduct_ward_round)
└── agent.py                               (register ward_nurse_agent)
```

---

## Sprint 6 — Theatre & Procedure Scheduling Agent

**Why:** Surgical patients currently have no pathway after a surgical specialist recommends
an operation. Theatre booking, pre-op assessment, consent, surgical safety checklist, and
post-op orders are all absent.

**Status:** 🔲 Planned

### New Agent

| Agent | Variable | Role |
|-------|----------|------|
| Theatre Scheduling | `theatre_scheduling_agent` | Manages the full surgical pathway: pre-op assessment, theatre booking, consent documentation, surgical safety checklist (WHO), post-op orders, recovery room, post-op review. |

### New Tools — `tools/theatre_tools.py`

| Function | Description |
|----------|-------------|
| `book_theatre(patient_id, procedure, surgeon, urgency, estimated_duration)` | Books operating theatre slot; urgency: `"emergency"`, `"urgent"`, `"elective"` |
| `record_consent(patient_id, procedure, risks_discussed, patient_signature, clinician)` | Documents informed consent with risks, benefits, alternatives discussed |
| `surgical_safety_checklist(patient_id, procedure, stage)` | WHO Surgical Safety Checklist: `"sign_in"`, `"time_out"`, `"sign_out"` |
| `generate_postop_orders(patient_id, procedure, anaesthetic_type, surgeon_instructions)` | Creates post-operative orders: monitoring, analgesia, diet, activity, wound care, DVT prophylaxis |

### Files to Create / Modify

```
agentic_hospital/
├── tools/theatre_tools.py                 (new — 4 functions)
├── departments/theatre_scheduling.py      (new)
├── prompts/theatre_scheduling.py          (new)
└── agent.py                               (register theatre_scheduling_agent)
```

---

## Sprint 7 — Risk Assessment Tools

**Why:** Every inpatient admission triggers mandatory risk assessments in a real hospital.
These are clinically validated tools that drive preventive interventions (anticoagulation,
falls prevention, pressure care, nutritional support).

**Status:** 🔲 Planned

### Approach
Add to existing department tools or create `tools/risk_assessment_tools.py`.
No new agent required — add to `ward_nurse_agent` and relevant specialist tools.

### New Tools — `tools/risk_assessment_tools.py`

| Function | Validated Score | Description |
|----------|----------------|-------------|
| `calculate_vte_risk(patient_id, procedure_type, mobility)` | Caprini / NICE NG89 | VTE risk: low/moderate/high → prophylaxis recommendation |
| `falls_risk_assessment(patient_id, mobility, medications, history)` | Morse Falls Scale | Falls risk score → prevention interventions |
| `pressure_injury_risk(patient_id, mobility, nutrition, skin_condition)` | Braden Scale | Pressure injury risk → turning schedule, mattress type |
| `malnutrition_screening(patient_id, bmi, weight_loss, appetite)` | MUST Score | Malnutrition risk → dietitian referral, nutritional support |
| `delirium_screening(patient_id, age, cognitive_baseline, acute_change)` | 4AT / CAM | Delirium risk/detection → intervention and monitoring |

### Files to Create / Modify

```
agentic_hospital/
├── tools/risk_assessment_tools.py         (new — 5 functions)
├── prompts/ward_nurse.py                  (add risk assessment protocol)
└── prompts/shared.py                      (add risk screens to admission workflow)
```

---

## Sprint 8 — GP Referral & Pre-hospital Pathways

**Why:** Most non-emergency specialist visits begin with a GP referral letter.
Emergency ambulance cases arrive with a paramedic handover. Both pathways are
entirely absent — the system currently only handles walk-in presentations.

**Status:** 🔲 Planned

### New Agents

| Agent | Variable | Role |
|-------|----------|------|
| GP Referral | `gp_referral_agent` | Receives GP referral letters, triages urgency, books outpatient appointment or direct admission, sends acknowledgement to GP |
| EMS / Pre-hospital | `ems_agent` | Receives ambulance pre-notification (ATMIST handover), prepares receiving team, fast-tracks registration and triage |

### New Tools — `tools/referral_tools.py`

| Function | Description |
|----------|-------------|
| `receive_gp_referral(patient_id, referring_gp, reason, urgency, clinical_summary)` | Logs GP referral with 2-week-wait flag for urgent cancer referrals |
| `triage_referral(referral_id)` | Triages referral: routine outpatient / urgent outpatient / direct admission |
| `receive_atmist_handover(patient_id, age, time_of_incident, mechanism, injuries, signs, treatment)` | EMS pre-notification using ATMIST format; activates receiving team |

### Files to Create / Modify

```
agentic_hospital/
├── tools/referral_tools.py                (new — 3 functions)
├── departments/gp_referral.py             (new)
├── departments/ems.py                     (new)
├── prompts/gp_referral.py                 (new)
├── prompts/ems.py                         (new)
└── agent.py                               (register both agents)
```

---

## Sprint 9 — Infection Control & Patient Safety

**Why:** Isolation criteria, contact precautions, and outbreak management are critical
patient safety functions. Partly covered by the Infectious_Diseases ward but no formal
protocol or enforcement exists. Drug errors and patient misidentification are also absent.

**Status:** 🔲 Planned

### New Tools — `tools/safety_tools.py`

| Function | Description |
|----------|-------------|
| `assess_isolation_requirement(patient_id, diagnosis, organism)` | Determines isolation type: standard / contact / droplet / airborne — enforces bed assignment to appropriate ward/room |
| `record_adverse_event(patient_id, event_type, description, severity, action_taken)` | Incident reporting: medication error, fall, pressure injury, wrong patient, near miss |
| `check_patient_identity(patient_id, name, dob, wristband_scan)` | Two-point patient identification before any medication/procedure — mimics real bedside safety check |
| `thirty_day_readmission_flag(patient_id)` | Flags if patient was admitted for same condition within 30 days — triggers root cause review |

### Files to Create / Modify

```
agentic_hospital/
├── tools/safety_tools.py                  (new — 4 functions)
├── prompts/shared.py                      (add safety checks to admission protocol)
└── prompts/hospital_admission.py          (add isolation enforcement to bed assignment)
```

---

## Sprint 10 — Data Persistence & EHR Foundation

**Why:** All patient data, lab results, bed occupancy, and encounter history are
in-memory mocks that reset on every restart. A real hospital runs on a persistent
EHR (Electronic Health Record). This sprint replaces in-memory dicts with a
lightweight database to enable longitudinal data, cohort queries, and readmission tracking.

**Status:** 🔲 Planned

### Approach

Replace `_PATIENT_DB`, `_LAB_DB`, `_BED_DB`, `_WAITLIST`, `_ENCOUNTER_LOG` with
SQLite (via `sqlite3` stdlib — no new dependency). Provide a migration script to
seed the database from current in-memory data.

### Key Changes

| Component | Current | Target |
|-----------|---------|--------|
| Patient records | `_PATIENT_DB` dict | `patients` table (SQLite) |
| Lab results | `_LAB_DB` dict | `lab_results` table with `order_id`, `status`, `resulted_at` |
| Bed state | `_BED_DB` dict | `beds` + `admissions` tables |
| Encounter log | List in memory | `encounters` table with timestamps |
| Waitlist | `_WAITLIST` dict | `waitlist` table with priority queue |

### New Capabilities Unlocked

- Query all patients on a specific medication
- 30-day readmission rate calculation
- Cohort analytics (all diabetic patients admitted this month)
- Persistent bed state across restarts
- Audit trail for all clinical actions

### Files to Create / Modify

```
agentic_hospital/
├── tools/db.py                            (new — SQLite connection + schema)
├── tools/common_tools.py                  (migrate from dict to DB calls)
├── tools/bed_management_tools.py          (migrate from dict to DB calls)
└── scripts/seed_db.py                     (new — seed from current mock data)
```

---

## Full Agent Roster After All Sprints

| # | Agent | Category | Sprint |
|---|-------|----------|--------|
| 1 | `hospital_coordinator` | Root | Existing |
| 2–36 | 35 specialist departments | Medical/Surgical/Diagnostic | Existing |
| 37 | `hospital_admission_agent` | Operations | Existing |
| 38 | `triage_nurse_agent` | Clinical | Sprint 1 |
| 39 | `pharmacy_agent` | Clinical | Sprint 2 |
| 40 | `discharge_planning_agent` | Clinical | Sprint 3 |
| 41 | `ward_nurse_agent` | Clinical | Sprint 5 |
| 42 | `theatre_scheduling_agent` | Operations | Sprint 6 |
| 43 | `gp_referral_agent` | Administrative | Sprint 8 |
| 44 | `ems_agent` | Pre-hospital | Sprint 8 |

**Currently implemented: 40 agents** (38 baseline + 2 new from Sprints 1-3)
**Total after all sprints: 44 agents**

---

## Tool Count Projection

| Sprint | New Tools | Cumulative Total |
|--------|-----------|-----------------|
| Sprint 1 (baseline) | 94 | 94 |
| Sprint 1 | +3 | 97 |
| Sprint 2 | +4 | 101 |
| Sprint 3 | +4 | 105 |
| Sprint 4 | +3 | 108 |
| Sprint 3 | +4 | 105 |
| Sprint 4 | +3 | 108 |
| Sprint 5 | +5 | 113 |
| Sprint 6 | +4 | 117 |
| Sprint 7 | +5 | 122 |
| Sprint 8 | +3 | 125 |
| Sprint 9 | +4 | 129 |
| Sprint 10 | 0 (refactor) | 129 |

---

## Realistic Hospital Score Progression

| Milestone | Score / 100 | Key Unlocks |
|-----------|------------|-------------|
| Baseline (pre-sprints) | 28 | Triage, routing, bed management, image analysis |
| After Sprint 1 | ~32 | ESI v4 triage, waiting queue |
| After Sprint 2 | ~36 | Pharmacy verification, dispensing, reconciliation |
| After Sprint 3 | ~40 | Discharge planning, GP letters, community referrals |
| After Sprint 4 | ~44 | Diagnostic ordering workflow (order → result → review) |
| After Sprint 5 | ~55 | Inpatient nursing, ward rounds |
| After Sprint 6–7 | ~65 | Theatre, risk assessments |
| After Sprint 8–9 | ~72 | Pre-hospital pathways, infection control, safety |
| After Sprint 10 | ~78 | Data persistence, longitudinal EHR, cohort analytics |
| Beyond (FHIR, RBAC, HL7) | 85–90 | Interoperability, auth, regulatory compliance |
