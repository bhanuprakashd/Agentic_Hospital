"""Emergency Medicine-specific triage and risk stratification tools."""


def chest_pain_risk_stratification(
    age: int,
    symptoms: list[str],
    ecg_changes: bool,
    troponin_elevated: bool,
    diaphoresis: bool = False,
    radiation_to_arm_jaw: bool = False,
    known_cad: bool = False,
    hypertension: bool = False,
    diabetes: bool = False,
    hyperlipidemia: bool = False,
    smoking: bool = False,
) -> dict:
    """Stratifies chest pain risk using the HEART score methodology.

    HEART Score: History, ECG, Age, Risk factors, Troponin.

    Args:
        age: Patient age in years.
        symptoms: List of symptoms described (e.g., ['chest pressure', 'shortness of breath']).
        ecg_changes: Whether new ST-T wave changes or LBBB are present on ECG.
        troponin_elevated: Whether troponin is above normal limit.
        diaphoresis: Whether diaphoresis (sweating) is present.
        radiation_to_arm_jaw: Whether pain radiates to arm or jaw.
        known_cad: Whether patient has known coronary artery disease, prior MI, or PCI/CABG.
        hypertension: Whether patient has hypertension.
        diabetes: Whether patient has diabetes mellitus.
        hyperlipidemia: Whether patient has hyperlipidemia.
        smoking: Whether patient is a current or recent smoker.

    Returns:
        dict: HEART score, risk category, and recommended disposition.
    """
    heart_score = 0
    score_breakdown = {}

    # H - History (0-2)
    high_risk_symptoms = ["pressure", "squeezing", "radiating", "crushing", "tightness", "typical"]
    low_risk_symptoms = ["sharp", "pleuritic", "positional", "reproducible", "musculoskeletal"]
    symptoms_lower = [s.lower() for s in symptoms]

    history_score = 0
    if radiation_to_arm_jaw or diaphoresis or any(k in s for s in symptoms_lower for k in high_risk_symptoms):
        history_score = 2
    elif any(k in s for s in symptoms_lower for k in low_risk_symptoms):
        history_score = 0
    else:
        history_score = 1
    heart_score += history_score
    score_breakdown["history"] = f"{history_score}/2"

    # E - ECG (0-2)
    ecg_score = 2 if ecg_changes else 0
    heart_score += ecg_score
    score_breakdown["ecg"] = f"{ecg_score}/2"

    # A - Age (0-2)
    if age >= 65:
        age_score = 2
    elif age >= 45:
        age_score = 1
    else:
        age_score = 0
    heart_score += age_score
    score_breakdown["age"] = f"{age_score}/2"

    # R - Risk factors (0-2)
    risk_count = sum([known_cad, hypertension, diabetes, hyperlipidemia, smoking])
    if known_cad:
        risk_score = 2  # Known CAD → highest
    elif risk_count >= 3:
        risk_score = 2
    elif risk_count >= 1:
        risk_score = 1
    else:
        risk_score = 0
    heart_score += risk_score
    score_breakdown["risk_factors"] = f"{risk_score}/2"

    # T - Troponin (0-2)
    troponin_score = 2 if troponin_elevated else 0
    heart_score += troponin_score
    score_breakdown["troponin"] = f"{troponin_score}/2"

    # Classification
    if heart_score <= 3:
        risk_category = "LOW"
        mace_risk = "<2%"
        disposition = "Safe for discharge with outpatient stress test follow-up within 72 hours"
        actions = [
            "Repeat troponin at 0h and 3h (if not done)",
            "Aspirin 325 mg if no contraindications",
            "Outpatient cardiology or stress test within 72 hours",
            "Clear return precautions given to patient",
        ]
    elif heart_score <= 6:
        risk_category = "MODERATE"
        mace_risk = "12–17%"
        disposition = "Observation / hospital admission for further evaluation"
        actions = [
            "Serial troponins (0h, 3h, 6h)",
            "Serial ECGs",
            "Cardiology consultation",
            "Stress test or coronary CT angiography (CCTA)",
            "Antiplatelet therapy",
        ]
    else:
        risk_category = "HIGH"
        mace_risk = ">50%"
        disposition = "Emergent cardiology consultation — likely ACS, consider immediate intervention"
        actions = [
            "EMERGENT cardiology consultation",
            "Immediate heparin anticoagulation",
            "Dual antiplatelet therapy (aspirin + P2Y12 inhibitor)",
            "Prepare for cardiac catheterization",
            "Continuous cardiac monitoring in monitored bed or CCU",
        ]

    return {
        "status": "stratified",
        "heart_score": heart_score,
        "score_breakdown": score_breakdown,
        "risk_category": risk_category,
        "major_adverse_cardiac_event_risk": mace_risk,
        "recommended_disposition": disposition,
        "immediate_actions": actions,
    }


def trauma_triage_assessment(
    mechanism: str,
    vital_signs: dict,
    injured_areas: list[str],
    gcs: int = 15,
    age: int = 30,
) -> dict:
    """Performs trauma triage using Revised Trauma Score (RTS) and mechanism criteria.

    Args:
        mechanism: Injury mechanism (e.g., 'motor vehicle collision', 'fall from height', 'gunshot wound').
        vital_signs: Dict with 'systolic_bp', 'heart_rate', 'respiratory_rate' keys.
        injured_areas: List of body areas injured (e.g., ['head', 'chest', 'abdomen']).
        gcs: Glasgow Coma Scale score (3–15).
        age: Patient age in years.

    Returns:
        dict: Trauma level activation, Revised Trauma Score, and immediate management priorities.
    """
    sbp = vital_signs.get("systolic_bp", 120)
    hr = vital_signs.get("heart_rate", 80)
    rr = vital_signs.get("respiratory_rate", 16)

    # Revised Trauma Score (RTS) calculation
    # Glasgow Coma Scale
    if gcs >= 13:
        gcs_coded = 4
    elif gcs >= 9:
        gcs_coded = 3
    elif gcs >= 6:
        gcs_coded = 2
    elif gcs >= 4:
        gcs_coded = 1
    else:
        gcs_coded = 0

    # Systolic BP
    if sbp >= 90:
        sbp_coded = 4
    elif sbp >= 76:
        sbp_coded = 3
    elif sbp >= 50:
        sbp_coded = 2
    elif sbp >= 1:
        sbp_coded = 1
    else:
        sbp_coded = 0

    # Respiratory Rate
    if 10 <= rr <= 29:
        rr_coded = 4
    elif rr >= 30:
        rr_coded = 3
    elif 6 <= rr <= 9:
        rr_coded = 2
    elif 1 <= rr <= 5:
        rr_coded = 1
    else:
        rr_coded = 0

    rts = (0.9368 * gcs_coded) + (0.7326 * sbp_coded) + (0.2908 * rr_coded)
    rts_rounded = round(rts, 2)

    # Mechanism criteria for level 1 activation
    high_energy_mechanisms = [
        "gunshot", "penetrating", "stabbing", "ejection", "fatality at scene",
        "fall > 20 feet", "fall > 6 meters", "motorcycle > 20 mph", "pedestrian",
        "high speed", "rollover",
    ]
    mechanism_lower = mechanism.lower()
    high_energy = any(k in mechanism_lower for k in high_energy_mechanisms)

    # Anatomic criteria
    critical_areas = ["head", "neck", "chest", "abdomen", "pelvis", "spine"]
    critical_injuries = [a for a in injured_areas if any(c in a.lower() for c in critical_areas)]

    # Activation level
    if rts < 11 or gcs < 14 or sbp < 90 or (len(critical_injuries) >= 2):
        activation_level = "LEVEL 1 — Full trauma team activation"
        survival_probability = f"{round(rts_rounded / 7.84 * 100, 1)}% estimated (RTS-based)"
    elif high_energy or critical_injuries:
        activation_level = "LEVEL 2 — Trauma team notification"
        survival_probability = "Good — monitor closely"
    else:
        activation_level = "LEVEL 3 — Trauma assessment only"
        survival_probability = "Good prognosis"

    immediate_priorities = []
    if gcs < 9:
        immediate_priorities.append("AIRWAY: GCS < 9 — definitive airway (RSI intubation) immediately")
    if sbp < 90:
        immediate_priorities.append("CIRCULATION: Hemorrhagic shock — activate massive transfusion protocol (1:1:1 pRBC:FFP:Plt)")
    if "chest" in [a.lower() for a in injured_areas]:
        immediate_priorities.append("CHEST: Tension pneumothorax or hemothorax — CXR / needle decompression / chest tube")
    if "abdomen" in [a.lower() for a in injured_areas] and sbp < 90:
        immediate_priorities.append("ABDOMEN: FAST exam — if positive with hemodynamic instability → OR emergently")
    if "head" in [a.lower() for a in injured_areas] and gcs < 15:
        immediate_priorities.append("HEAD: TBI concern — CT head without contrast; neurosurgery consultation")
    if "pelvis" in [a.lower() for a in injured_areas]:
        immediate_priorities.append("PELVIS: Pelvic ring fracture — pelvic binder, angiography if hemodynamically unstable")

    if not immediate_priorities:
        immediate_priorities.append("Primary and secondary survey per ATLS protocol")

    return {
        "status": "triaged",
        "mechanism": mechanism,
        "revised_trauma_score": rts_rounded,
        "trauma_activation_level": activation_level,
        "survival_probability_estimate": survival_probability,
        "critical_anatomic_injuries": critical_injuries,
        "high_energy_mechanism": high_energy,
        "immediate_priorities": immediate_priorities,
        "vital_signs": vital_signs,
        "gcs": gcs,
        "age_consideration": "High risk" if age >= 65 or age <= 5 else "Standard",
    }
