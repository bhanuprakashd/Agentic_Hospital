"""Anesthesiology-specific pre-operative assessment tools."""


def asa_physical_status_classification(
    conditions: list[str],
    emergency: bool = False,
) -> dict:
    """Assigns ASA Physical Status Classification based on patient conditions.

    Uses American Society of Anesthesiologists (ASA) classification system.

    Args:
        conditions: List of patient medical conditions (e.g., ['hypertension', 'diabetes', 'COPD']).
        emergency: Whether the procedure is an emergency (appends 'E' to classification).

    Returns:
        dict: ASA class, definition, anesthetic implications, and monitoring requirements.
    """
    conditions_lower = [c.lower() for c in conditions]

    # Scoring criteria
    asa_class = 1  # Default: healthy patient

    # ASA II indicators (mild systemic disease)
    asa2_keywords = [
        "controlled hypertension", "mild hypertension", "diabetes type 2", "diabetes",
        "mild asthma", "asthma", "obesity", "bmi 30", "smoking", "social alcohol",
        "pregnancy", "mild liver disease", "hyperthyroidism", "hypothyroidism",
        "controlled thyroid",
    ]
    # ASA III indicators (severe systemic disease)
    asa3_keywords = [
        "copd", "poorly controlled diabetes", "uncontrolled hypertension", "morbid obesity",
        "active hepatitis", "alcohol dependence", "implanted pacemaker", "moderate heart failure",
        "pvd", "peripheral vascular", "end stage renal", "ckd stage 3", "ckd stage 4",
        "cancer", "dialysis", "cvd", "history of mi", "stroke", "tia", "cabg",
        "heart failure", "ejection fraction < 50", "severe valve disease",
        "chronic kidney disease",
    ]
    # ASA IV indicators (life-threatening disease)
    asa4_keywords = [
        "recent mi", "acute mi", "recent stroke", "severe valve", "sepsis",
        "severe copd", "severe heart failure", "ejection fraction < 25",
        "ongoing cardiac ischemia", "recent coronary stent", "hepatic failure",
        "respiratory failure", "coagulopathy", "severe sepsis",
    ]

    for cond in conditions_lower:
        if any(k in cond for k in asa4_keywords):
            asa_class = max(asa_class, 4)
        elif any(k in cond for k in asa3_keywords):
            asa_class = max(asa_class, 3)
        elif any(k in cond for k in asa2_keywords):
            asa_class = max(asa_class, 2)

    asa_definitions = {
        1: "Normal healthy patient with no systemic disease.",
        2: "Patient with mild systemic disease and no functional limitations.",
        3: "Patient with severe systemic disease with functional limitations (not incapacitating).",
        4: "Patient with severe systemic disease that is a constant threat to life.",
        5: "Moribund patient not expected to survive without the operation.",
        6: "Brain-dead patient declared for organ donation.",
    }

    mortality_risk = {1: "<0.1%", 2: "0.2%", 3: "1.8%", 4: "7.8%", 5: "9.4%", 6: "N/A"}

    monitoring = {
        1: ["Standard ASA monitoring (pulse oximetry, capnography, ECG, NIBP, temperature)"],
        2: ["Standard ASA monitoring", "Consider arterial line if BP liability expected"],
        3: [
            "Standard ASA monitoring",
            "Arterial line for continuous BP monitoring",
            "Consider central venous access",
            "Preoperative optimization of systemic disease",
        ],
        4: [
            "Standard ASA monitoring",
            "Arterial line (mandatory)",
            "Central venous access",
            "Pulmonary artery catheter or TEE if indicated",
            "ICU availability post-operatively",
            "Multidisciplinary pre-op discussion required",
        ],
    }

    asa_label = f"ASA {asa_class}" + ("E" if emergency else "")

    return {
        "status": "classified",
        "asa_class": asa_class,
        "asa_label": asa_label,
        "definition": asa_definitions.get(asa_class, "N/A"),
        "estimated_mortality_risk": mortality_risk.get(asa_class, "N/A"),
        "anesthetic_implications": monitoring.get(asa_class, monitoring[3]),
        "is_emergency": emergency,
        "emergency_note": "Emergency designation increases anesthetic risk. Expedite pre-op workup." if emergency else None,
        "conditions_assessed": conditions,
    }


def calculate_anesthesia_risk(
    asa_class: int,
    procedure_type: str,
    patient_age: int,
    bmi: float,
    anticipated_blood_loss_ml: int = 0,
    duration_hours: float = 1.0,
) -> dict:
    """Calculates overall anesthetic risk and recommends management strategy.

    Args:
        asa_class: ASA physical status class (1-5).
        procedure_type: Type of procedure ('minor', 'intermediate', 'major', 'cardiac', 'neurosurgical').
        patient_age: Patient age in years.
        bmi: Body mass index in kg/m².
        anticipated_blood_loss_ml: Expected blood loss in milliliters.
        duration_hours: Estimated procedure duration in hours.

    Returns:
        dict: Overall risk level, anesthesia type recommendation, and perioperative care plan.
    """
    risk_score = asa_class  # Start with ASA class

    # Procedure risk contribution
    procedure_risk = {
        "minor": 0,
        "intermediate": 1,
        "major": 2,
        "cardiac": 3,
        "neurosurgical": 3,
        "vascular": 3,
        "thoracic": 3,
    }
    proc_score = procedure_risk.get(procedure_type.lower(), 1)
    risk_score += proc_score

    # Age risk
    if patient_age >= 80:
        risk_score += 2
    elif patient_age >= 70:
        risk_score += 1
    elif patient_age < 1:
        risk_score += 2  # Neonates

    # BMI risk
    if bmi >= 40:
        risk_score += 2  # Morbid obesity: difficult airway, OSA risk
    elif bmi >= 35:
        risk_score += 1

    # Blood loss risk
    if anticipated_blood_loss_ml >= 2000:
        risk_score += 2
    elif anticipated_blood_loss_ml >= 500:
        risk_score += 1

    # Duration risk
    if duration_hours >= 6:
        risk_score += 1

    # Classify overall risk
    if risk_score <= 3:
        overall_risk = "LOW"
        anesthesia_type = "General or regional/neuraxial anesthesia"
        care_level = "Standard post-anesthesia care unit (PACU)"
    elif risk_score <= 6:
        overall_risk = "MODERATE"
        anesthesia_type = "General anesthesia with enhanced monitoring; consider regional techniques"
        care_level = "PACU with possible overnight admission"
    else:
        overall_risk = "HIGH"
        anesthesia_type = "General anesthesia with arterial line, consider central access; ICU post-op"
        care_level = "ICU admission post-operatively"

    complications = []
    if bmi >= 35:
        complications.append("Difficult airway / obstructive sleep apnea risk — have video laryngoscope available")
    if patient_age >= 70:
        complications.append("Post-operative delirium risk — use BIS monitoring; minimize benzodiazepines")
    if anticipated_blood_loss_ml >= 500:
        complications.append("Blood conservation strategy — cell saver, transfusion triggers pre-defined")
    if asa_class >= 3:
        complications.append("Hemodynamic instability risk — vasopressors on standby")

    return {
        "status": "calculated",
        "overall_risk": overall_risk,
        "risk_score": risk_score,
        "asa_class": asa_class,
        "procedure_type": procedure_type,
        "recommended_anesthesia_type": anesthesia_type,
        "post_op_care": care_level,
        "special_considerations": complications,
        "preoperative_workup": [
            "ECG if age > 50 or cardiac history",
            "CBC, BMP, coagulation studies if major surgery",
            "Chest X-ray if pulmonary disease or major surgery",
            "Echocardiogram if cardiac dysfunction suspected",
            "Type and screen for blood loss > 500 mL anticipated",
        ],
    }
