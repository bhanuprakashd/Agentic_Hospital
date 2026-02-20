"""Neurology-specific diagnostic and assessment tools."""


def assess_stroke_risk(
    symptoms: list[str],
    onset_time: str,
    age: int,
    has_atrial_fibrillation: bool,
    has_hypertension: bool,
    has_diabetes: bool,
    previous_stroke: bool,
) -> dict:
    """Assesses stroke risk using FAST criteria and BE-FAST screening, plus CHA2DS2-VASc scoring.

    Args:
        symptoms: List of current symptoms (e.g., ['face drooping', 'arm weakness', 'speech difficulty']).
        onset_time: When symptoms started (e.g., '2 hours ago', '30 minutes ago').
        age: Patient age in years.
        has_atrial_fibrillation: Whether patient has atrial fibrillation.
        has_hypertension: Whether patient has hypertension.
        has_diabetes: Whether patient has diabetes.
        previous_stroke: Whether patient has had a previous stroke or TIA.

    Returns:
        dict: Stroke risk assessment with urgency level and recommendations.
    """
    fast_signs = {
        "face drooping": False,
        "arm weakness": False,
        "speech difficulty": False,
        "balance loss": False,
        "vision changes": False,
    }

    symptom_text = " ".join(s.lower() for s in symptoms)
    for sign in fast_signs:
        if sign in symptom_text or any(sign in s.lower() for s in symptoms):
            fast_signs[sign] = True

    fast_positive = sum(fast_signs.values())

    # CHA2DS2-VASc score (for AF patients)
    cha2ds2_vasc = 0
    if has_atrial_fibrillation:
        if age >= 75: cha2ds2_vasc += 2
        elif age >= 65: cha2ds2_vasc += 1
        if has_hypertension: cha2ds2_vasc += 1
        if has_diabetes: cha2ds2_vasc += 1
        if previous_stroke: cha2ds2_vasc += 2

    # Determine urgency
    if fast_positive >= 2:
        urgency = "EMERGENCY"
        action = "CALL 911 IMMEDIATELY. Possible acute stroke. Time is brain - every minute matters."
    elif fast_positive == 1:
        urgency = "URGENT"
        action = "Immediate emergency department evaluation needed. Possible stroke or TIA."
    elif previous_stroke and len(symptoms) > 0:
        urgency = "URGENT"
        action = "History of prior stroke with new symptoms. Immediate evaluation needed."
    else:
        urgency = "ROUTINE"
        action = "Schedule neurology consultation for evaluation."

    return {
        "status": "assessed",
        "urgency": urgency,
        "action": action,
        "fast_screening": fast_signs,
        "fast_signs_positive": fast_positive,
        "onset_time": onset_time,
        "cha2ds2_vasc_score": cha2ds2_vasc if has_atrial_fibrillation else "N/A (no AF)",
        "risk_factors": {
            "age": age,
            "atrial_fibrillation": has_atrial_fibrillation,
            "hypertension": has_hypertension,
            "diabetes": has_diabetes,
            "previous_stroke": previous_stroke,
        },
        "note": "Stroke treatment window is typically within 4.5 hours for IV tPA.",
    }


def evaluate_consciousness(
    eye_response: int,
    verbal_response: int,
    motor_response: int,
) -> dict:
    """Evaluates level of consciousness using Glasgow Coma Scale (GCS).

    Args:
        eye_response: Eye opening response (1-4): 1=None, 2=To pressure, 3=To voice, 4=Spontaneous.
        verbal_response: Verbal response (1-5): 1=None, 2=Sounds, 3=Words, 4=Confused, 5=Oriented.
        motor_response: Motor response (1-6): 1=None, 2=Extension, 3=Flexion, 4=Withdrawal, 5=Localizing, 6=Obeys commands.

    Returns:
        dict: GCS score with interpretation and recommended actions.
    """
    eye_response = max(1, min(4, eye_response))
    verbal_response = max(1, min(5, verbal_response))
    motor_response = max(1, min(6, motor_response))

    gcs_total = eye_response + verbal_response + motor_response

    # Classification
    if gcs_total >= 13:
        severity = "MILD"
        interpretation = "Mild brain injury / Minor impairment"
        action = "Monitor closely, neurological checks every 1-2 hours"
    elif gcs_total >= 9:
        severity = "MODERATE"
        interpretation = "Moderate brain injury"
        action = "Urgent neuroimaging (CT head), ICU monitoring recommended"
    else:
        severity = "SEVERE"
        interpretation = "Severe brain injury - comatose state"
        action = "EMERGENCY: Secure airway, urgent CT, neurosurgical consultation"

    # Intubation recommendation
    intubation_needed = gcs_total <= 8

    eye_descriptions = {1: "None", 2: "To pressure", 3: "To voice", 4: "Spontaneous"}
    verbal_descriptions = {1: "None", 2: "Sounds", 3: "Words", 4: "Confused", 5: "Oriented"}
    motor_descriptions = {1: "None", 2: "Extension", 3: "Abnormal flexion", 4: "Withdrawal", 5: "Localizing", 6: "Obeys commands"}

    return {
        "status": "evaluated",
        "gcs_total": gcs_total,
        "severity": severity,
        "interpretation": interpretation,
        "recommended_action": action,
        "components": {
            "eye": f"E{eye_response} - {eye_descriptions.get(eye_response, 'Unknown')}",
            "verbal": f"V{verbal_response} - {verbal_descriptions.get(verbal_response, 'Unknown')}",
            "motor": f"M{motor_response} - {motor_descriptions.get(motor_response, 'Unknown')}",
        },
        "intubation_recommended": intubation_needed,
        "note": "GCS should be reassessed regularly. Document best response observed.",
    }
