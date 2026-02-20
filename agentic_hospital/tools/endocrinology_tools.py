"""Endocrinology-specific diagnostic and assessment tools."""


def diabetes_management_assessment(
    hba1c: float,
    fasting_glucose: float,
    current_medications: list[str],
    age: int,
    diabetes_type: str,
    kidney_function_egfr: float = 90,
    cardiovascular_disease: bool = False,
) -> dict:
    """Assesses diabetes control and recommends treatment adjustments.

    Args:
        hba1c: Hemoglobin A1c percentage (normal < 5.7%, diabetes ≥ 6.5%).
        fasting_glucose: Fasting blood glucose in mg/dL (normal < 100).
        current_medications: List of current diabetes medications.
        age: Patient age in years.
        diabetes_type: Type of diabetes ('type1', 'type2', or 'gestational').
        kidney_function_egfr: Estimated GFR in mL/min/1.73m².
        cardiovascular_disease: Whether patient has established CVD.

    Returns:
        dict: Diabetes control assessment with treatment recommendations.
    """
    control_status = "UNKNOWN"
    if hba1c < 7.0:
        control_status = "WELL CONTROLLED"
    elif hba1c < 8.0:
        control_status = "SUBOPTIMAL"
    elif hba1c < 9.0:
        control_status = "POOR"
    else:
        control_status = "VERY POOR"

    recommendations = []
    medication_changes = []

    # Determine treatment intensification
    on_metformin = any("metformin" in m.lower() for m in current_medications)
    on_sulfonylurea = any("sulfonylurea" in m.lower() or "glipizide" in m.lower() or "glyburide" in m.lower() for m in current_medications)
    on_insulin = any("insulin" in m.lower() for m in current_medications)
    on_glp1 = any("glp1" in m.lower() or "semaglutide" in m.lower() or "liraglutide" in m.lower() or "ozempic" in m.lower() for m in current_medications)
    on_sglt2 = any("sglt2" in m.lower() or "empagliflozin" in m.lower() or "dapagliflozin" in m.lower() for m in current_medications)

    if hba1c >= 7.0:
        if not on_metformin and diabetes_type == "type2":
            medication_changes.append("Start Metformin (first-line therapy)")
        elif on_metformin and hba1c >= 7.5:
            if kidney_function_egfr >= 30:
                if cardiovascular_disease and not on_sglt2:
                    medication_changes.append("Add SGLT2 inhibitor (cardioprotective benefit)")
                if not on_glp1:
                    medication_changes.append("Consider GLP-1 agonist (weight loss + glycemic benefit)")
            if hba1c >= 9.0 and not on_insulin:
                medication_changes.append("Consider initiating basal insulin")

    recommendations.append(f"Target A1c: < 7.0% (individualize based on age and comorbidities)")
    if diabetes_type == "type1":
        recommendations.append("Type 1 DM: Insulin is essential - multiple daily injections or pump")

    # Screening recommendations
    screenings = []
    if diabetes_type == "type2":
        screenings.append("Annual comprehensive metabolic panel")
        screenings.append("Annual urine albumin-to-creatinine ratio")
        screenings.append("Annual dilated eye exam")
        screenings.append("Annual foot exam")
    if kidney_function_egfr < 60:
        screenings.append("More frequent kidney function monitoring (every 3-6 months)")

    return {
        "status": "assessed",
        "diabetes_type": diabetes_type,
        "hba1c": f"{hba1c}%",
        "fasting_glucose": f"{fasting_glucose} mg/dL",
        "control_status": control_status,
        "current_medications": current_medications,
        "medication_adjustments": medication_changes,
        "recommendations": recommendations,
        "screening_reminders": screenings,
        "risk_factors": {
            "age": age,
            "kidney_function_egfr": kidney_function_egfr,
            "cardiovascular_disease": cardiovascular_disease,
        },
    }


def thyroid_nodule_assessment(
    nodule_size_cm: float,
    tsh_level: float,
    ultrasound_features: list[str],
    age: int,
    radiation_exposure_history: bool = False,
    family_history_thyroid_cancer: bool = False,
) -> dict:
    """Assesses thyroid nodule risk and recommends workup based on TI-RADS criteria.

    Args:
        nodule_size_cm: Size of thyroid nodule in centimeters.
        tsh_level: Thyroid stimulating hormone level in mIU/L (normal 0.4-4.0).
        ultrasound_features: List of ultrasound features (e.g., ['solid', 'microcalcifications', 'hypoechoic']).
        age: Patient age in years.
        radiation_exposure_history: History of head/neck radiation exposure.
        family_history_thyroid_cancer: Family history of thyroid cancer.

    Returns:
        dict: Thyroid nodule assessment with TI-RADS category and FNA recommendation.
    """
    # TI-RADS scoring
    tirads_score = 0

    # Composition
    if "cystic" in [f.lower() for f in ultrasound_features]:
        tirads_score += 0
    elif "spongiform" in [f.lower() for f in ultrasound_features]:
        tirads_score += 0
    elif "mixed" in [f.lower() for f in ultrasound_features]:
        tirads_score += 1
    elif "solid" in [f.lower() for f in ultrasound_features]:
        tirads_score += 2

    # Echogenicity
    if "anechoic" in [f.lower() for f in ultrasound_features]:
        tirads_score += 0
    elif "hyperechoic" in [f.lower() for f in ultrasound_features]:
        tirads_score += 1
    elif "isoechoic" in [f.lower() for f in ultrasound_features]:
        tirads_score += 1
    elif "hypoechoic" in [f.lower() for f in ultrasound_features]:
        tirads_score += 2
    elif "very hypoechoic" in [f.lower() for f in ultrasound_features]:
        tirads_score += 3

    # Shape
    if "taller-than-wide" in [f.lower() for f in ultrasound_features]:
        tirads_score += 3

    # Margin
    if "lobulated" in [f.lower() for f in ultrasound_features]:
        tirads_score += 2
    elif "irregular" in [f.lower() for f in ultrasound_features] or "infiltrative" in [f.lower() for f in ultrasound_features]:
        tirads_score += 3
    elif "extra-thyroidal" in [f.lower() for f in ultrasound_features]:
        tirads_score += 3

    # Echogenic foci
    if "macrocalcifications" in [f.lower() for f in ultrasound_features]:
        tirads_score += 1
    if "microcalcifications" in [f.lower() for f in ultrasound_features]:
        tirads_score += 3
    if "peripheral_calcifications" in [f.lower() for f in ultrasound_features]:
        tirads_score += 0

    # TI-RADS category
    if tirads_score <= 1:
        tirads_category = "TR1 - Benign"
        fna_threshold_cm = 999  # No FNA recommended
    elif tirads_score == 2:
        tirads_category = "TR2 - Not Suspicious"
        fna_threshold_cm = 999
    elif tirads_score == 3:
        tirads_category = "TR3 - Mildly Suspicious"
        fna_threshold_cm = 2.5
    elif tirads_score <= 6:
        tirads_category = "TR4 - Moderately Suspicious"
        fna_threshold_cm = 1.5
    else:
        tirads_category = "TR5 - Highly Suspicious"
        fna_threshold_cm = 1.0

    # FNA recommendation
    fna_recommended = nodule_size_cm >= fna_threshold_cm

    # High-risk history lowers threshold
    if radiation_exposure_history or family_history_thyroid_cancer:
        if tirads_category in ["TR3", "TR4", "TR5"]:
            fna_recommended = nodule_size_cm >= 1.0

    # TSH interpretation
    tsh_interpretation = "Normal"
    if tsh_level < 0.4:
        tsh_interpretation = "Low - consider checking free T4, T3; may need thyroid scan for hyperfunctioning nodule"
    elif tsh_level > 4.0:
        tsh_interpretation = "High - consistent with hypothyroidism; check thyroid antibodies"

    return {
        "status": "assessed",
        "nodule_size_cm": nodule_size_cm,
        "tirads_score": tirads_score,
        "tirads_category": tirads_category,
        "tsh_level": f"{tsh_level} mIU/L",
        "tsh_interpretation": tsh_interpretation,
        "fna_recommended": fna_recommended,
        "fna_reason": f"Nodule {nodule_size_cm}cm ≥ threshold {fna_threshold_cm}cm for {tirads_category}" if fna_recommended else "Below FNA threshold for this TI-RADS category",
        "risk_factors": {
            "radiation_exposure": radiation_exposure_history,
            "family_history_thyroid_cancer": family_history_thyroid_cancer,
        },
        "next_steps": [
            "Fine needle aspiration biopsy" if fna_recommended else "Ultrasound surveillance in 12 months",
            "Check thyroid function tests if not done recently",
            "Consider thyroid scan if TSH suppressed",
        ],
    }