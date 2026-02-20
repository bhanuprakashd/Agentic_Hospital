"""Cardiothoracic Surgery-specific risk assessment tools."""


def cardiac_surgery_risk_score(
    age: int,
    gender: str,
    lvef: float,
    creatinine: float,
    diabetes: bool,
    prior_cardiac_surgery: bool,
    urgent: bool = False,
    pulmonary_hypertension: bool = False,
) -> dict:
    """Estimates operative mortality risk for cardiac surgery (EuroSCORE II-based model).

    Args:
        age: Patient age in years.
        gender: Patient gender ('male' or 'female').
        lvef: Left ventricular ejection fraction as percentage (normal ≥ 55%).
        creatinine: Serum creatinine level in mg/dL (normal 0.6–1.2).
        diabetes: Whether the patient has insulin-dependent diabetes.
        prior_cardiac_surgery: Whether the patient has had a previous cardiac operation (redo surgery).
        urgent: Whether the surgery is urgent (unplanned, before next working day).
        pulmonary_hypertension: Whether significant pulmonary hypertension is present (PAP > 55 mmHg).

    Returns:
        dict: Estimated surgical mortality risk, risk category, and perioperative recommendations.
    """
    score = 0.0

    # Age
    if age >= 80:
        score += 12.0
    elif age >= 75:
        score += 8.0
    elif age >= 70:
        score += 5.0
    elif age >= 65:
        score += 3.0
    elif age >= 60:
        score += 1.5

    # Gender (female higher risk)
    if gender.lower() == "female":
        score += 1.5

    # Creatinine (renal function)
    if creatinine >= 2.26:
        score += 5.0  # On dialysis equivalent
    elif creatinine >= 1.70:
        score += 3.5
    elif creatinine > 1.40:
        score += 1.5

    # LVEF
    if lvef < 20:
        score += 6.0
    elif lvef < 30:
        score += 4.0
    elif lvef < 50:
        score += 2.0
    # LVEF ≥ 50%: no additional points

    # Diabetes (insulin-dependent)
    if diabetes:
        score += 2.0

    # Redo surgery
    if prior_cardiac_surgery:
        score += 4.5

    # Urgency
    if urgent:
        score += 4.0

    # Pulmonary hypertension
    if pulmonary_hypertension:
        score += 2.5

    # Convert score to mortality estimate
    if score < 3:
        mortality_estimate = "<2%"
        risk_category = "LOW"
    elif score < 6:
        mortality_estimate = "2–5%"
        risk_category = "MODERATE"
    elif score < 10:
        mortality_estimate = "5–12%"
        risk_category = "HIGH"
    else:
        mortality_estimate = ">12%"
        risk_category = "VERY HIGH"

    recommendations = []
    if lvef < 30:
        recommendations.append("Consider pre-op inotropic support or IABP if hemodynamically unstable")
    if creatinine >= 1.7:
        recommendations.append("Nephrology consultation for renal protection strategy; avoid nephrotoxins")
    if prior_cardiac_surgery:
        recommendations.append("Redo sternotomy: have cardiac surgery team and perfusion ready for emergent bypass")
    if risk_category in ("HIGH", "VERY HIGH"):
        recommendations.append("Multidisciplinary Heart Team discussion required")
        recommendations.append("Consider percutaneous alternatives (TAVI, PCI) if applicable")

    return {
        "status": "assessed",
        "total_risk_score": round(score, 1),
        "estimated_operative_mortality": mortality_estimate,
        "risk_category": risk_category,
        "risk_factors_identified": {
            "age": age,
            "gender": gender,
            "lvef_percent": lvef,
            "creatinine_mg_dl": creatinine,
            "insulin_dependent_diabetes": diabetes,
            "redo_surgery": prior_cardiac_surgery,
            "urgent_operation": urgent,
            "pulmonary_hypertension": pulmonary_hypertension,
        },
        "recommendations": recommendations,
    }


def thoracic_surgery_feasibility(
    procedure: str,
    fev1_percent: int,
    dlco_percent: int,
    ppo_fev1_percent: int = 0,
) -> dict:
    """Assesses pulmonary function fitness for thoracic surgery.

    Uses predicted post-operative (ppo) lung function to determine surgical feasibility.

    Args:
        procedure: Planned surgical procedure ('pneumonectomy', 'lobectomy', 'segmentectomy', 'wedge_resection').
        fev1_percent: Pre-operative FEV1 as % of predicted (normal ≥ 80%).
        dlco_percent: Diffusing capacity (DLCO) as % of predicted (normal ≥ 80%).
        ppo_fev1_percent: Predicted post-operative FEV1 % (calculated from number of segments removed).

    Returns:
        dict: Surgical feasibility, risk level, and alternative options if high risk.
    """
    # If ppo_fev1 not provided, estimate conservatively
    if ppo_fev1_percent == 0:
        reduction_map = {
            "pneumonectomy": 0.45,  # Removes ~45% of function
            "lobectomy": 0.25,
            "segmentectomy": 0.10,
            "wedge_resection": 0.05,
        }
        reduction = reduction_map.get(procedure.lower(), 0.25)
        ppo_fev1_percent = int(fev1_percent * (1 - reduction))

    # Standard criteria
    issues = []
    feasible = True

    # FEV1 criteria
    if fev1_percent >= 80 and dlco_percent >= 80:
        fev1_status = "Normal — proceed without further testing"
    elif fev1_percent >= 60:
        fev1_status = "Mildly reduced — low risk if ppo FEV1 adequate"
    elif fev1_percent >= 40:
        fev1_status = "Moderately reduced — ppo FEV1 and exercise testing required"
        issues.append("FEV1 40–60%: cardiopulmonary exercise test (CPET) recommended")
    else:
        fev1_status = "Severely reduced — high surgical risk"
        issues.append("FEV1 < 40%: High risk of post-operative respiratory failure")
        feasible = False if procedure.lower() in ("pneumonectomy", "lobectomy") else True

    # ppo FEV1 criteria (predicted post-operative)
    if ppo_fev1_percent >= 40:
        ppo_status = "Acceptable (≥ 40%)"
    elif ppo_fev1_percent >= 30:
        ppo_status = "Borderline (30–40%) — CPET mandatory"
        issues.append("ppo FEV1 30–40%: Cardiopulmonary exercise testing required. Proceed if VO2max > 10 mL/kg/min")
    else:
        ppo_status = "Prohibitive (< 30%) — very high risk of respiratory failure"
        issues.append("ppo FEV1 < 30%: Surgery contraindicated unless CPET VO2max > 15 mL/kg/min")
        feasible = False

    # DLCO criteria
    if dlco_percent < 40:
        issues.append("DLCO < 40%: Very high risk of post-operative respiratory failure")
        feasible = False
    elif dlco_percent < 60:
        issues.append("DLCO 40–60%: Increased risk — CPET recommended")

    risk_level = "LOW" if feasible and not issues else "HIGH" if not feasible else "MODERATE"
    alternatives = []
    if not feasible:
        alternatives = [
            "Consider stereotactic body radiation therapy (SBRT) as curative alternative",
            "Evaluate for lesser resection (segmentectomy or wedge resection)",
            "Pulmonary rehabilitation to improve pre-operative function",
        ]

    return {
        "status": "assessed",
        "procedure": procedure,
        "surgical_feasibility": "Feasible" if feasible else "High Risk / May be Contraindicated",
        "risk_level": risk_level,
        "pre_op_fev1_percent": fev1_percent,
        "pre_op_dlco_percent": dlco_percent,
        "predicted_post_op_fev1_percent": ppo_fev1_percent,
        "fev1_interpretation": fev1_status,
        "ppo_fev1_interpretation": ppo_status,
        "identified_concerns": issues,
        "alternative_options": alternatives,
        "recommendation": (
            "Proceed with surgery." if risk_level == "LOW"
            else "CPET testing required before surgical decision." if risk_level == "MODERATE"
            else "High risk: multidisciplinary discussion and consider non-surgical alternatives."
        ),
    }
