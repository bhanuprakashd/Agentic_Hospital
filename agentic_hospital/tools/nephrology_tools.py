"""Nephrology-specific diagnostic and assessment tools."""


def calculate_gfr(creatinine: float, age: int, gender: str, race: str = "other") -> dict:
    """Calculates estimated Glomerular Filtration Rate (eGFR) using the CKD-EPI equation.

    Args:
        creatinine: Serum creatinine level in mg/dL.
        age: Patient age in years.
        gender: Patient gender ('male' or 'female').
        race: Patient race for adjustment (note: 2021 CKD-EPI removes race adjustment).

    Returns:
        dict: eGFR value with CKD stage classification and recommendations.
    """
    # Simplified CKD-EPI calculation (2021 equation without race adjustment)
    if gender.lower() == "female":
        if creatinine <= 0.7:
            gfr = 142 * (creatinine / 0.7) ** (-0.241) * (0.9938 ** age) * 1.012
        else:
            gfr = 142 * (creatinine / 0.7) ** (-1.200) * (0.9938 ** age) * 1.012
    else:
        if creatinine <= 0.9:
            gfr = 142 * (creatinine / 0.9) ** (-0.302) * (0.9938 ** age)
        else:
            gfr = 142 * (creatinine / 0.9) ** (-1.200) * (0.9938 ** age)

    gfr = round(gfr, 1)

    # CKD staging
    if gfr >= 90:
        stage = "G1 - Normal or High"
        action = "Monitor annually if risk factors present"
    elif gfr >= 60:
        stage = "G2 - Mildly Decreased"
        action = "Monitor annually, assess progression"
    elif gfr >= 45:
        stage = "G3a - Mildly to Moderately Decreased"
        action = "Monitor every 6 months, assess complications"
    elif gfr >= 30:
        stage = "G3b - Moderately to Severely Decreased"
        action = "Monitor every 3-6 months, nephrology referral recommended"
    elif gfr >= 15:
        stage = "G4 - Severely Decreased"
        action = "Monitor every 3 months, prepare for renal replacement therapy"
    else:
        stage = "G5 - Kidney Failure"
        action = "Dialysis or transplant evaluation needed"

    return {
        "status": "calculated",
        "eGFR": gfr,
        "unit": "mL/min/1.73m²",
        "ckd_stage": stage,
        "recommended_action": action,
        "input_parameters": {
            "creatinine": creatinine,
            "age": age,
            "gender": gender,
        },
    }


def assess_kidney_stage(
    gfr: float,
    albuminuria: float,
    blood_pressure: str,
    diabetes: bool,
    proteinuria: bool,
) -> dict:
    """Comprehensive kidney disease staging and risk assessment.

    Args:
        gfr: Estimated GFR value in mL/min/1.73m².
        albuminuria: Urine albumin-to-creatinine ratio (UACR) in mg/g.
        blood_pressure: Current blood pressure reading (e.g., '140/90').
        diabetes: Whether patient has diabetes.
        proteinuria: Whether protein is detected in urine.

    Returns:
        dict: Comprehensive CKD assessment with staging, risk level, and management plan.
    """
    # GFR category
    if gfr >= 90: g_category = "G1"
    elif gfr >= 60: g_category = "G2"
    elif gfr >= 45: g_category = "G3a"
    elif gfr >= 30: g_category = "G3b"
    elif gfr >= 15: g_category = "G4"
    else: g_category = "G5"

    # Albuminuria category
    if albuminuria < 30:
        a_category = "A1 - Normal to mildly increased"
    elif albuminuria < 300:
        a_category = "A2 - Moderately increased (microalbuminuria)"
    else:
        a_category = "A3 - Severely increased (macroalbuminuria)"

    # Risk matrix
    high_risk = gfr < 30 or albuminuria >= 300
    moderate_risk = (30 <= gfr < 60 and albuminuria >= 30) or gfr < 45

    if high_risk:
        risk_level = "HIGH"
        prognosis = "High risk of progression to kidney failure"
    elif moderate_risk:
        risk_level = "MODERATE"
        prognosis = "Moderate risk of progression - close monitoring needed"
    else:
        risk_level = "LOW"
        prognosis = "Low risk of progression with appropriate management"

    management = []
    if diabetes:
        management.append("Optimize glycemic control (HbA1c < 7%)")
        management.append("Consider SGLT2 inhibitor for renal protection")
    management.append("Blood pressure target: < 130/80 mmHg")
    if albuminuria >= 30:
        management.append("Start ACE inhibitor or ARB for albuminuria reduction")
    if gfr < 45:
        management.append("Monitor calcium, phosphorus, PTH, vitamin D")
        management.append("Adjust medication doses for renal function")
    if gfr < 30:
        management.append("Discuss renal replacement therapy options")
        management.append("Avoid nephrotoxic medications (NSAIDs, aminoglycosides)")
    if gfr < 15:
        management.append("URGENT: Evaluate for dialysis initiation or transplant listing")

    return {
        "status": "assessed",
        "gfr_category": g_category,
        "albuminuria_category": a_category,
        "overall_risk": risk_level,
        "prognosis": prognosis,
        "management_plan": management,
        "monitoring_frequency": "Every 3 months" if high_risk else "Every 6 months" if moderate_risk else "Annually",
    }
