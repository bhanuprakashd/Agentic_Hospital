"""General Surgery-specific diagnostic and assessment tools."""


def appendicitis_scoring(
    right_lower_quadrant_pain: bool,
    migration_pain: bool,
    anorexia: bool,
    nausea_vomiting: bool,
    tenderness_rlq: bool,
    rebound_tenderness: bool,
    elevated_temperature: bool,
    wbc_elevated: bool,
    crp_elevated: bool = None,
) -> dict:
    """Scores appendicitis likelihood using Alvarado score.

    Args:
        right_lower_quadrant_pain: Pain localized to right lower quadrant.
        migration_pain: Pain migrated from periumbilical to RLQ.
        anorexia: Patient has anorexia.
        nausea_vomiting: Patient has nausea or vomiting.
        tenderness_rlq: Tenderness in right lower quadrant.
        rebound_tenderness: Rebound tenderness present.
        elevated_temperature: Temperature > 37.3°C (99.1°F).
        wbc_elevated: White blood cell count > 10,000.
        crp_elevated: C-reactive protein elevated (optional).

    Returns:
        dict: Appendicitis likelihood score with recommendations.
    """
    # Alvarado score
    alvarado_score = 0
    features_present = []

    # Symptoms
    if migration_pain:
        alvarado_score += 2
        features_present.append("Migratory pain (+2)")
    if anorexia:
        alvarado_score += 1
        features_present.append("Anorexia (+1)")
    if nausea_vomiting:
        alvarado_score += 1
        features_present.append("Nausea/vomiting (+1)")

    # Signs
    if right_lower_quadrant_pain:
        alvarado_score += 1
        features_present.append("RLQ pain (+1)")
    if tenderness_rlq:
        alvarado_score += 2
        features_present.append("RLQ tenderness (+2)")
    if rebound_tenderness:
        alvarado_score += 1
        features_present.append("Rebound tenderness (+1)")
    if elevated_temperature:
        alvarado_score += 1
        features_present.append("Fever (+1)")

    # Labs
    if wbc_elevated:
        alvarado_score += 2
        features_present.append("Leukocytosis (+2)")

    # Interpretation
    if alvarado_score >= 9:
        likelihood = "HIGH"
        probability = "> 90%"
        recommendation = "Proceed to surgery - appendicitis highly likely"
        imaging = "CT not mandatory if clinical picture clear; proceed to OR"
    elif alvarado_score >= 7:
        likelihood = "PROBABLE"
        probability = "70-90%"
        recommendation = "Strong consideration for surgery; imaging recommended to confirm"
        imaging = "CT abdomen/pelvis with contrast or ultrasound (children/pregnant)"
    elif alvarado_score >= 5:
        likelihood = "POSSIBLE"
        probability = "30-70%"
        recommendation = "Imaging recommended; serial examination if discharged"
        imaging = "CT abdomen/pelvis with contrast"
    elif alvarado_score >= 3:
        likelihood = "UNLIKELY"
        probability = "< 30%"
        recommendation = "Consider other diagnoses; imaging if concern persists"
        imaging = "CT if clinical concern remains; consider observation"
    else:
        likelihood = "VERY LOW"
        probability = "< 10%"
        recommendation = "Look for alternative diagnosis"
        imaging = "Not indicated for appendicitis"

    # Add CRP consideration
    if crp_elevated is not None:
        if crp_elevated and alvarado_score >= 5:
            likelihood = "PROBABLE" if likelihood == "POSSIBLE" else likelihood
            features_present.append("Elevated CRP (+supports inflammation)")

    # Differential diagnoses
    differentials = [
        "Mesenteric adenitis (especially in children)",
        "Gastroenteritis",
        "Crohn's disease / terminal ileitis",
        "Ovarian pathology (females)",
        "Ectopic pregnancy (females of childbearing age)",
        "Right-sided diverticulitis",
        "Urinary tract infection / pyelonephritis",
    ]

    return {
        "status": "scored",
        "alvarado_score": alvarado_score,
        "features_present": features_present,
        "appendicitis_likelihood": likelihood,
        "estimated_probability": probability,
        "recommendation": recommendation,
        "imaging_recommendation": imaging,
        "differential_diagnoses": differentials,
        "clinical_features": {
            "rlq_pain": right_lower_quadrant_pain,
            "pain_migration": migration_pain,
            "anorexia": anorexia,
            "nausea_vomiting": nausea_vomiting,
            "tenderness": tenderness_rlq,
            "rebound": rebound_tenderness,
            "fever": elevated_temperature,
            "leukocytosis": wbc_elevated,
        },
    }


def surgical_risk_assessment(
    age: int,
    procedure_type: str,
    asa_class: int,
    functional_status: str,
    emergency: bool = False,
    weight_loss_6_months: float = 0,
    serum_albumin: float = None,
    hematocrit: float = None,
    creatinine: float = None,
) -> dict:
    """Assesses surgical risk using multiple indices.

    Args:
        age: Patient age in years.
        procedure_type: Type of procedure ('minor', 'intermediate', 'major', 'complex').
        asa_class: ASA physical status class (1-5).
        functional_status: 'independent', 'partially_dependent', or 'totally_dependent'.
        emergency: Whether procedure is emergency.
        weight_loss_6_months: Weight loss in past 6 months in kg.
        serum_albumin: Serum albumin in g/dL (normal 3.5-5.0).
        hematocrit: Hematocrit percentage (normal 36-48).
        creatinine: Serum creatinine in mg/dL (normal 0.6-1.2).

    Returns:
        dict: Surgical risk assessment with recommendations.
    """
    risk_score = 0
    risk_factors = []

    # Age contribution
    if age >= 80:
        risk_score += 4
        risk_factors.append(f"Age ≥ 80 ({age} years)")
    elif age >= 70:
        risk_score += 3
        risk_factors.append(f"Age 70-79 ({age} years)")
    elif age >= 60:
        risk_score += 2
        risk_factors.append(f"Age 60-69 ({age} years)")
    elif age >= 50:
        risk_score += 1
        risk_factors.append(f"Age 50-59 ({age} years)")

    # ASA class
    if asa_class >= 4:
        risk_score += 4
        risk_factors.append(f"ASA Class {asa_class} (severe systemic disease)")
    elif asa_class == 3:
        risk_score += 2
        risk_factors.append(f"ASA Class 3 (systemic disease)")
    elif asa_class == 2:
        risk_score += 1
        risk_factors.append(f"ASA Class 2 (mild systemic disease)")

    # Functional status
    if functional_status == "totally_dependent":
        risk_score += 3
        risk_factors.append("Totally dependent functional status")
    elif functional_status == "partially_dependent":
        risk_score += 2
        risk_factors.append("Partially dependent functional status")

    # Emergency
    if emergency:
        risk_score += 2
        risk_factors.append("Emergency procedure")

    # Procedure type
    procedure_scores = {"minor": 1, "intermediate": 2, "major": 3, "complex": 4}
    risk_score += procedure_scores.get(procedure_type, 2)
    risk_factors.append(f"Procedure: {procedure_type}")

    # Nutritional status
    if weight_loss_6_months > 10:
        risk_score += 3
        risk_factors.append(f"Severe weight loss (>10 kg in 6 months)")
    elif weight_loss_6_months > 5:
        risk_score += 1
        risk_factors.append(f"Significant weight loss ({weight_loss_6_months} kg in 6 months)")

    if serum_albumin is not None and serum_albumin < 3.0:
        risk_score += 2
        risk_factors.append(f"Low albumin ({serum_albumin} g/dL) - malnutrition marker")

    # Anemia
    if hematocrit is not None and hematocrit < 30:
        risk_score += 2
        risk_factors.append(f"Severe anemia (Hct {hematocrit}%)")

    # Renal function
    if creatinine is not None and creatinine > 2.0:
        risk_score += 2
        risk_factors.append(f"Renal insufficiency (Cr {creatinine} mg/dL)")

    # Risk stratification
    if risk_score >= 12:
        risk_level = "VERY HIGH"
        mortality_estimate = "> 10%"
        morbidity_estimate = "> 30%"
        recommendation = "Consider non-surgical alternatives if possible; if surgery necessary, optimize medical conditions first"
    elif risk_score >= 8:
        risk_level = "HIGH"
        mortality_estimate = "5-10%"
        morbidity_estimate = "20-30%"
        recommendation = "Medical optimization required; ICU bed availability confirmed; consider preoperative cardiac evaluation"
    elif risk_score >= 5:
        risk_level = "MODERATE"
        mortality_estimate = "1-5%"
        morbidity_estimate = "10-20%"
        recommendation = "Standard preoperative workup; consider risk reduction strategies"
    else:
        risk_level = "LOW"
        mortality_estimate = "< 1%"
        morbidity_estimate = "< 10%"
        recommendation = "Standard perioperative care"

    # Preoperative optimization
    optimization = []
    if serum_albumin is not None and serum_albumin < 3.5:
        optimization.append("Nutritional optimization - consider oral supplements or enteral nutrition")
    if hematocrit is not None and hematocrit < 30:
        optimization.append("Anemia workup and treatment - consider iron supplementation or transfusion")
    if creatinine is not None and creatinine > 1.5:
        optimization.append("Renal protective measures - avoid nephrotoxins, maintain hydration")
    if asa_class >= 3:
        optimization.append("Medical optimization per anesthesia recommendations")

    return {
        "status": "assessed",
        "risk_score": risk_score,
        "risk_level": risk_level,
        "estimated_mortality": mortality_estimate,
        "estimated_morbidity": morbidity_estimate,
        "risk_factors": risk_factors,
        "recommendation": recommendation,
        "preoperative_optimization": optimization if optimization else ["No specific optimization needed beyond standard care"],
        "patient_factors": {
            "age": age,
            "asa_class": asa_class,
            "functional_status": functional_status,
            "procedure_type": procedure_type,
            "emergency": emergency,
        },
        "perioperative_considerations": [
            "DVT prophylaxis unless contraindicated",
            "Antibiotic prophylaxis within 60 minutes of incision",
            "Blood glucose control if diabetic",
            "Pain management planning",
            "Early mobilization post-operatively",
        ],
    }