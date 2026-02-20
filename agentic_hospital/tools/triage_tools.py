"""Emergency Severity Index v4 (ESI) triage tools for the nurse triage station.

Implements the full ESI v4 decision algorithm:
  Step 1 — Does the patient require an immediate life-saving intervention? → ESI 1
  Step 2 — Is this a high-risk situation / altered mentation / severe pain? → ESI 2
  Step 3 — How many resources are expected? 2+ → ESI 3, 1 → ESI 4, 0 → ESI 5
"""

from datetime import datetime

# ── In-memory state ───────────────────────────────────────────────────────────
_TRIAGE_LOG: dict[str, list[dict]] = {}   # patient_id → list of triage records
_WAITING_QUEUE: list[dict] = []           # priority-ordered waiting list
_TRIAGE_SEQ: dict[str, int] = {"n": 0}   # auto-increment for record IDs

# ── ESI level metadata ────────────────────────────────────────────────────────
_ESI_META: dict[int, dict] = {
    1: {
        "label": "IMMEDIATE",
        "colour": "Red",
        "target_physician_time": "Immediate (<1 min)",
        "area": "Resuscitation Bay",
        "description": "Requires immediate life-saving intervention (airway/breathing/circulation)",
    },
    2: {
        "label": "EMERGENT",
        "colour": "Orange",
        "target_physician_time": "<10 minutes",
        "area": "Acute Treatment Area",
        "description": "High-risk situation; new-onset confusion/lethargy; or severe uncontrolled pain",
    },
    3: {
        "label": "URGENT",
        "colour": "Yellow",
        "target_physician_time": "<30 minutes",
        "area": "Majors",
        "description": "Stable vitals; expected to need 2 or more ED resources",
    },
    4: {
        "label": "LESS URGENT",
        "colour": "Green",
        "target_physician_time": "<60 minutes",
        "area": "Minors / Fast Track",
        "description": "Stable; expected to need 1 ED resource",
    },
    5: {
        "label": "NON-URGENT",
        "colour": "Blue",
        "target_physician_time": "<120 minutes",
        "area": "Fast Track / Ambulatory",
        "description": "Stable; no resources expected — history and physical exam only",
    },
}

# ── Symptom keyword sets for ESI 1 / 2 ───────────────────────────────────────
_ESI1_KEYWORDS = frozenset({
    "cardiac arrest", "respiratory arrest", "not breathing", "no pulse",
    "pulseless", "unresponsive", "unconscious", "apnoeic", "apnea",
    "active seizure", "fitting", "choking", "complete airway obstruction",
    "agonal breathing", "no respiratory effort",
})

_ESI2_KEYWORDS = frozenset({
    "stemi", "heart attack", "crushing chest pain", "stroke", "facial droop",
    "arm weakness", "slurred speech", "facial asymmetry", "sudden weakness",
    "anaphylaxis", "throat swelling", "unable to swallow", "tongue swelling",
    "severe allergic reaction", "septic shock", "sepsis", "altered consciousness",
    "acutely confused", "new confusion", "disoriented", "lethargic",
    "suicidal with plan", "active haemorrhage", "massive bleeding",
    "major trauma", "polytrauma", "high-speed mvc", "ejected from vehicle",
    "penetrating trauma", "stab wound", "gunshot", "overdose altered",
    "eclampsia", "severe pre-eclampsia", "aortic dissection", "tearing chest",
    "tension pneumothorax", "pulmonary embolism", "massive pe",
    "epiglottitis", "meningococcal", "ruptured ectopic", "ectopic rupture",
    "status epilepticus",
})

# Keywords predicting ≥2 resources (ESI 3) or exactly 1 resource (ESI 4)
_ESI3_KEYWORDS = frozenset({
    "chest pain", "shortness of breath", "dyspnea", "difficulty breathing",
    "abdominal pain", "severe vomiting", "haematemesis", "vomiting blood",
    "head injury", "head trauma", "possible fracture", "closed fracture",
    "seizure", "post-ictal", "fever high", "infection", "cellulitis spreading",
    "acute back pain severe", "renal colic", "kidney stone", "hematuria",
    "blood in urine", "rectal bleeding", "melaena", "haemoptysis",
    "syncope", "fainted collapse", "diabetic emergency", "hyperglycaemia",
    "hypoglycaemia", "pregnancy complication", "vaginal bleeding pregnant",
    "eye injury", "sudden vision loss", "acute hearing loss", "vertigo severe",
    "psychiatric deterioration", "suicidal", "self harm", "altered mental",
    "severe dehydration", "urinary retention", "unable to pass urine",
    "deep laceration", "tendon injury", "dislocation",
})

_ESI4_KEYWORDS = frozenset({
    "minor cut", "superficial laceration", "sprain", "ankle sprain",
    "uti", "urinary symptoms", "dysuria", "ear pain", "earache",
    "sore throat", "tonsillitis", "mild rash", "minor burn", "dental pain",
    "toothache", "eye irritation", "conjunctivitis", "minor bruise",
    "nausea without vomiting", "mild diarrhoea", "mild abdominal cramp",
    "upper respiratory infection", "cough", "headache mild",
    "wrist injury minor", "finger injury", "toe injury",
})


def _check_vital_danger_zone(vitals: dict) -> tuple[bool, bool, list[str]]:
    """Checks vital signs against ESI danger zone thresholds.

    Returns:
        tuple: (esi1_triggered, esi2_triggered, list_of_findings)
    """
    esi1, esi2 = False, False
    findings: list[str] = []

    hr   = vitals.get("hr")
    sbp  = vitals.get("sbp")
    rr   = vitals.get("rr")
    spo2 = vitals.get("spo2")
    gcs  = vitals.get("gcs")
    temp = vitals.get("temp")

    if hr is not None:
        if hr < 30 or hr > 180:
            esi1 = True
            findings.append(f"HR {hr} bpm — life-threatening (arrhythmia / extreme bradycardia)")
        elif hr < 50 or hr > 120:
            esi2 = True
            findings.append(f"HR {hr} bpm — danger zone")

    if sbp is not None:
        if sbp < 60:
            esi1 = True
            findings.append(f"SBP {sbp} mmHg — profound shock (immediate intervention)")
        elif sbp < 90 or sbp > 220:
            esi2 = True
            findings.append(f"SBP {sbp} mmHg — haemodynamic concern")

    if rr is not None:
        if rr < 8 or rr > 36:
            esi1 = True
            findings.append(f"RR {rr}/min — respiratory failure threshold")
        elif rr < 10 or rr > 28:
            esi2 = True
            findings.append(f"RR {rr}/min — respiratory distress")

    if spo2 is not None:
        if spo2 < 85:
            esi1 = True
            findings.append(f"SpO₂ {spo2}% — critical hypoxia (immediate oxygenation)")
        elif spo2 < 92:
            esi2 = True
            findings.append(f"SpO₂ {spo2}% — danger zone hypoxia")

    if gcs is not None:
        if gcs <= 8:
            esi1 = True
            findings.append(f"GCS {gcs}/15 — severe impairment (intubation threshold)")
        elif gcs < 14:
            esi2 = True
            findings.append(f"GCS {gcs}/15 — altered consciousness")

    if temp is not None:
        if temp >= 41.5 or temp < 34.0:
            esi1 = True
            findings.append(f"Temperature {temp}°C — extreme thermoregulatory failure")
        elif temp >= 38.5 or temp < 35.5:
            esi2 = True
            findings.append(f"Temperature {temp}°C — fever / hypothermia concern")

    return esi1, esi2, findings


def _predict_resources(symptoms_lower: str, pain_score: int) -> int:
    """Predicts expected number of ED resources for ESI 3/4/5 discrimination.

    ED resources include: IV/IM medications, IV fluids, blood tests, imaging,
    ECG, urinalysis (lab), specialist consult, simple procedure (suture/splint).
    NOT counted: history, physical exam, prescription refill, urine dipstick, crutches.

    Symptom keywords take priority over pain score alone — a patient with chest pain
    and moderate pain (5/10) still requires ≥2 resources (bloods + ECG + imaging).
    """
    # Symptom keywords checked first — they drive resource prediction more reliably
    for kw in _ESI3_KEYWORDS:
        if kw in symptoms_lower:
            return 2  # clearly needs ≥2 resources regardless of pain score

    for kw in _ESI4_KEYWORDS:
        if kw in symptoms_lower:
            # Pain ≥7 on top of a 1-resource complaint → likely needs a second resource
            return 2 if pain_score >= 7 else 1

    # No keyword match — fall back to pain score alone
    if pain_score >= 7:
        return 2  # severe pain → IV analgesia + investigation
    if pain_score >= 4:
        return 1  # moderate pain → at least one intervention

    return 0


def calculate_esi_score(
    symptoms: str,
    vitals: dict,
    pain_score: int,
    arrival_mechanism: str = "walk-in",
) -> dict:
    """Calculates the Emergency Severity Index (ESI v4) triage level.

    Implements the three-step ESI v4 decision algorithm used in emergency
    departments worldwide to assign acuity levels 1 (most critical) to
    5 (least critical).

    Args:
        symptoms: Free-text chief complaint and presenting symptoms.
        vitals: Dict of recorded vital signs. Accepted keys:
                  hr (bpm), sbp (mmHg), dbp (mmHg), rr (/min),
                  spo2 (%), temp (°C), gcs (3–15).
                  Omit any that were not measured.
        pain_score: Patient self-reported pain 0–10
                    (0 = none, 10 = worst imaginable).
        arrival_mechanism: "walk-in" | "ambulance" | "wheelchair" |
                           "stretcher" | "police" | "gp-referral".

    Returns:
        dict: ESI level, colour, target physician time, area assignment,
              clinical rationale, and recommended immediate nursing actions.
    """
    s = symptoms.lower()
    rationale: list[str] = []

    # ── STEP 1: Immediate life-saving intervention required? ──────────────────
    for kw in _ESI1_KEYWORDS:
        if kw in s:
            rationale.append(f"Symptom '{kw}' → immediate life-saving intervention required")
            break

    vital_esi1, vital_esi2, vital_findings = _check_vital_danger_zone(vitals)

    if vital_esi1:
        rationale.extend(vital_findings)

    if rationale or vital_esi1:
        return {
            "status": "calculated",
            "esi_level": 1,
            **_ESI_META[1],
            "pain_score": pain_score,
            "arrival_mechanism": arrival_mechanism,
            "rationale": rationale or vital_findings,
            "immediate_actions": [
                "CALL resuscitation team IMMEDIATELY — do not leave patient",
                "Transfer patient to Resuscitation Bay NOW",
                "Initiate primary ABCDE survey",
                "Attach cardiac monitor, pulse oximetry, BP cuff continuously",
                "Establish 2× large-bore IV access; draw bloods simultaneously",
                "Notify attending physician STAT — stay at bedside",
            ],
            "calculated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

    # ── STEP 2: High-risk / danger zone / severe pain? ────────────────────────
    esi2_triggered = False

    for kw in _ESI2_KEYWORDS:
        if kw in s:
            esi2_triggered = True
            rationale.append(f"High-risk symptom identified: '{kw}'")
            break

    if vital_esi2:
        esi2_triggered = True
        rationale.extend(vital_findings)

    if pain_score >= 9:
        esi2_triggered = True
        rationale.append(f"Severe uncontrolled pain: {pain_score}/10")

    if arrival_mechanism in ("ambulance", "stretcher"):
        esi2_triggered = True
        rationale.append(f"Arrival by {arrival_mechanism} — elevated acuity assumed")

    if esi2_triggered:
        return {
            "status": "calculated",
            "esi_level": 2,
            **_ESI_META[2],
            "pain_score": pain_score,
            "arrival_mechanism": arrival_mechanism,
            "rationale": rationale if rationale else ["High-risk presentation — meets ESI 2 criteria"],
            "immediate_actions": [
                "Escort patient to Acute Treatment Area immediately",
                "Notify attending physician — patient must be seen within 10 minutes",
                "Attach continuous cardiac monitoring and pulse oximetry",
                "Establish IV access; draw routine bloods",
                "12-lead ECG if chest pain / palpitations / syncope",
                "Repeat vital signs every 5–10 minutes until physician assessment",
            ],
            "calculated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

    # ── STEP 3: Resource prediction → ESI 3 / 4 / 5 ─────────────────────────
    resources = _predict_resources(s, pain_score)

    if resources >= 2:
        esi_level = 3
        rationale.append("Presentation requires ≥2 ED resources (investigation + treatment likely)")
    elif resources == 1:
        esi_level = 4
        rationale.append("Presentation requires 1 ED resource (single test or minor procedure)")
    else:
        esi_level = 5
        rationale.append("No ED resources anticipated — history and physical examination only")

    actions_map = {
        3: [
            "Direct patient to Majors treatment area",
            "Initiate nurse-led protocol if applicable (sepsis screen, pain scale, IV access)",
            "Establish IV access if investigation likely to require it",
            "Advise patient: estimated wait approximately 30 minutes",
            "Reassess vitals within 30 minutes",
        ],
        4: [
            "Direct patient to Minors / Fast Track area",
            "Advise patient: estimated wait approximately 60 minutes",
            "Instruct patient to alert nurse immediately if symptoms worsen",
        ],
        5: [
            "Direct patient to Fast Track / Ambulatory area",
            "Advise patient: estimated wait up to 120 minutes",
            "Instruct patient to alert nurse if any change in condition",
        ],
    }

    return {
        "status": "calculated",
        "esi_level": esi_level,
        **_ESI_META[esi_level],
        "pain_score": pain_score,
        "arrival_mechanism": arrival_mechanism,
        "resources_expected": resources,
        "rationale": rationale,
        "immediate_actions": actions_map[esi_level],
        "calculated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def record_nurse_triage(
    patient_id: str,
    chief_complaint: str,
    vitals: dict,
    pain_score: int,
    esi_level: int,
    arrival_mechanism: str = "walk-in",
    allergies_verified: bool = False,
    wristband_applied: bool = True,
    additional_notes: str = "",
) -> dict:
    """Records the complete nurse triage assessment to the triage log.

    Creates a timestamped triage record including vital signs, ESI score,
    nursing observations, and area assignment. This is the legal triage
    documentation for the patient's visit.

    Args:
        patient_id: Patient identifier (e.g. "P001") or "NEW" for unregistered patients.
        chief_complaint: Brief chief complaint in patient's own words (1–2 sentences).
        vitals: Recorded vital signs dict — hr, sbp, dbp, rr, spo2, temp, gcs.
        pain_score: Pain score 0–10 as reported by patient.
        esi_level: ESI level 1–5 as returned by calculate_esi_score().
        arrival_mechanism: How the patient arrived — "walk-in", "ambulance", etc.
        allergies_verified: Whether known allergies were verbally confirmed with patient.
        wristband_applied: Whether ID wristband has been placed on patient's wrist.
        additional_notes: Additional nurse observations (e.g. diaphoretic, anxious, pale).

    Returns:
        dict: Triage record ID, full structured triage note, and formatted triage ticket.
    """
    _TRIAGE_SEQ["n"] += 1
    now = datetime.now()
    record_id = f"TR-{now.strftime('%Y%m%d')}-{_TRIAGE_SEQ['n']:04d}"
    timestamp  = now.strftime("%Y-%m-%d %H:%M")

    bp_str = (
        f"{vitals.get('sbp', '?')}/{vitals.get('dbp', '?')} mmHg"
        if vitals.get("sbp") else "Not recorded"
    )

    record = {
        "record_id":           record_id,
        "patient_id":          patient_id,
        "timestamp":           timestamp,
        "chief_complaint":     chief_complaint,
        "arrival_mechanism":   arrival_mechanism,
        "vitals": {
            "hr":          f"{vitals.get('hr', 'NR')} bpm",
            "bp":          bp_str,
            "rr":          f"{vitals.get('rr', 'NR')} /min",
            "spo2":        f"{vitals.get('spo2', 'NR')} %",
            "temp":        f"{vitals.get('temp', 'NR')} °C",
            "gcs":         f"{vitals.get('gcs', 'NR')} /15",
            "pain_score":  f"{pain_score} / 10",
        },
        "esi_level":           esi_level,
        "esi_label":           _ESI_META[esi_level]["label"],
        "esi_colour":          _ESI_META[esi_level]["colour"],
        "target_physician_time": _ESI_META[esi_level]["target_physician_time"],
        "area_assigned":       _ESI_META[esi_level]["area"],
        "allergies_verified":  allergies_verified,
        "wristband_applied":   wristband_applied,
        "additional_notes":    additional_notes,
        "nurse_triage_note": (
            f"Patient presents via {arrival_mechanism} with: {chief_complaint}. "
            f"Vitals — HR: {vitals.get('hr', 'NR')} bpm, "
            f"BP: {bp_str}, "
            f"RR: {vitals.get('rr', 'NR')}/min, "
            f"SpO₂: {vitals.get('spo2', 'NR')}%, "
            f"Temp: {vitals.get('temp', 'NR')}°C, "
            f"GCS: {vitals.get('gcs', 'NR')}/15, "
            f"Pain: {pain_score}/10. "
            f"Allergies verified: {'Yes' if allergies_verified else 'Not yet confirmed'}. "
            f"Wristband: {'Applied' if wristband_applied else 'Pending'}. "
            f"ESI Level {esi_level} — {_ESI_META[esi_level]['label']} "
            f"({_ESI_META[esi_level]['colour']}). "
            f"Assigned to: {_ESI_META[esi_level]['area']}. "
            f"Target physician time: {_ESI_META[esi_level]['target_physician_time']}."
            + (f" Nurse notes: {additional_notes}." if additional_notes else "")
        ),
    }

    _TRIAGE_LOG.setdefault(patient_id, []).append(record)

    # Formatted triage ticket for display
    w = 46
    sep = "─" * w
    ticket_lines = [
        f"┌{sep}┐",
        f"│{'NURSE TRIAGE TICKET':^{w}}│",
        f"│{sep}│",
        f"│  Record  : {record_id:<{w-12}}│",
        f"│  Patient : {patient_id:<{w-12}}│",
        f"│  Time    : {timestamp:<{w-12}}│",
        f"│{sep}│",
        f"│  ESI {esi_level}  : {_ESI_META[esi_level]['label']:<{w-12}}│",
        f"│  Colour  : {_ESI_META[esi_level]['colour']:<{w-12}}│",
        f"│  Area    : {_ESI_META[esi_level]['area']:<{w-12}}│",
        f"│  MD time : {_ESI_META[esi_level]['target_physician_time']:<{w-12}}│",
        f"│{sep}│",
        f"│  HR      : {str(vitals.get('hr', 'NR')) + ' bpm':<{w-12}}│",
        f"│  BP      : {bp_str:<{w-12}}│",
        f"│  RR      : {str(vitals.get('rr', 'NR')) + ' /min':<{w-12}}│",
        f"│  SpO₂    : {str(vitals.get('spo2', 'NR')) + ' %':<{w-12}}│",
        f"│  Temp    : {str(vitals.get('temp', 'NR')) + ' °C':<{w-12}}│",
        f"│  Pain    : {str(pain_score) + '/10':<{w-12}}│",
        f"│{sep}│",
        f"│  Allergies verified : {'✓ Yes' if allergies_verified else '✗ Not confirmed':<{w-23}}│",
        f"│  Wristband applied  : {'✓ Yes' if wristband_applied else '✗ Pending':<{w-23}}│",
        f"└{sep}┘",
    ]

    return {
        "status":       "recorded",
        "record_id":    record_id,
        "patient_id":   patient_id,
        "timestamp":    timestamp,
        "triage_record": record,
        "triage_ticket": "\n".join(ticket_lines),
    }


def assign_waiting_priority(patient_id: str, esi_level: int) -> dict:
    """Places the patient in the ED waiting queue based on ESI level.

    Queue is ordered by ESI level ascending (1 = highest priority),
    then by arrival time within the same ESI group.
    ESI 1 patients bypass the queue entirely and go straight to resuscitation.

    Args:
        patient_id: Patient identifier.
        esi_level: ESI level 1–5 from calculate_esi_score().

    Returns:
        dict: Queue position, estimated wait time (minutes), area assigned,
              and patient instruction message.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ESI 1 — bypass queue entirely
    if esi_level == 1:
        return {
            "status":                  "bypassed_queue",
            "patient_id":              patient_id,
            "esi_level":               1,
            "queue_position":          "IMMEDIATE — NO WAIT",
            "estimated_wait_minutes":  0,
            "area_assigned":           "Resuscitation Bay",
            "physician_notified":      True,
            "timestamp":               timestamp,
            "patient_instruction":     (
                "IMMEDIATE ATTENTION REQUIRED. "
                "Patient transferred directly to Resuscitation Bay. "
                "Attending physician and resuscitation team alerted STAT."
            ),
        }

    # Add to priority queue
    entry = {
        "patient_id":   patient_id,
        "esi_level":    esi_level,
        "arrived_at":   timestamp,
        "area_assigned": _ESI_META[esi_level]["area"],
    }

    # Insert maintaining ESI order (lower ESI = higher priority), then FIFO within level
    insert_index = len(_WAITING_QUEUE)
    for i, existing in enumerate(_WAITING_QUEUE):
        if esi_level < existing["esi_level"]:
            insert_index = i
            break
    _WAITING_QUEUE.insert(insert_index, entry)

    overall_position = insert_index + 1
    same_level_ahead = sum(
        1 for e in _WAITING_QUEUE[:insert_index]
        if e["esi_level"] == esi_level
    )

    # Estimated wait = base time for ESI level + per-patient delay for same-level queue
    base_wait   = {2: 10, 3: 30, 4: 60, 5: 120}
    per_patient = {2:  5, 3: 15, 4: 20, 5:  25}
    estimated_wait = base_wait[esi_level] + same_level_ahead * per_patient[esi_level]

    return {
        "status":                  "queued",
        "patient_id":              patient_id,
        "esi_level":               esi_level,
        "esi_label":               _ESI_META[esi_level]["label"],
        "queue_position":          overall_position,
        "patients_ahead_same_level": same_level_ahead,
        "estimated_wait_minutes":  estimated_wait,
        "area_assigned":           _ESI_META[esi_level]["area"],
        "physician_notified":      esi_level <= 2,
        "timestamp":               timestamp,
        "patient_instruction": (
            f"Please take a seat in the {_ESI_META[esi_level]['area']}. "
            f"You are number {overall_position} in the queue. "
            f"Estimated wait: approximately {estimated_wait} minutes. "
            "Please alert a nurse immediately if your condition changes or gets worse."
        ),
    }


def get_triage_queue() -> dict:
    """Returns the current ED waiting queue ordered by priority.

    Returns:
        dict: Full waiting queue with ESI breakdown, wait times, and queue summary.
    """
    if not _WAITING_QUEUE:
        return {
            "status":         "empty",
            "total_waiting":  0,
            "queue":          [],
            "by_esi_level":   {str(i): 0 for i in range(1, 6)},
            "message":        "No patients currently waiting.",
        }

    by_level = {str(i): 0 for i in range(1, 6)}
    for entry in _WAITING_QUEUE:
        by_level[str(entry["esi_level"])] += 1

    queue_display = []
    for pos, entry in enumerate(_WAITING_QUEUE, start=1):
        lvl = entry["esi_level"]
        base_wait   = {2: 10, 3: 30, 4: 60, 5: 120}
        per_patient = {2:  5, 3: 15, 4: 20, 5:  25}
        ahead_same  = sum(
            1 for e in _WAITING_QUEUE[:pos - 1]
            if e["esi_level"] == lvl
        )
        wait = base_wait.get(lvl, 0) + ahead_same * per_patient.get(lvl, 0)
        queue_display.append({
            "position":     pos,
            "patient_id":   entry["patient_id"],
            "esi_level":    lvl,
            "esi_label":    _ESI_META[lvl]["label"],
            "esi_colour":   _ESI_META[lvl]["colour"],
            "area":         entry["area_assigned"],
            "arrived_at":   entry["arrived_at"],
            "est_wait_min": wait,
        })

    return {
        "status":        "active",
        "total_waiting": len(_WAITING_QUEUE),
        "by_esi_level": {
            "ESI-2 Emergent":    by_level["2"],
            "ESI-3 Urgent":      by_level["3"],
            "ESI-4 Less Urgent": by_level["4"],
            "ESI-5 Non-Urgent":  by_level["5"],
        },
        "queue": queue_display,
    }
