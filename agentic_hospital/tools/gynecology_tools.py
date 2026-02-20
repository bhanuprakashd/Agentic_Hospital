"""Gynecology-specific diagnostic and assessment tools."""


def pregnancy_risk_assessment(
    age: int,
    gestational_weeks: int,
    previous_pregnancies: int,
    previous_complications: list[str],
    current_conditions: list[str],
    blood_pressure: str,
    blood_sugar: float,
) -> dict:
    """Assesses pregnancy risk factors and provides recommendations.

    Args:
        age: Maternal age in years.
        gestational_weeks: Current weeks of gestation.
        previous_pregnancies: Number of previous pregnancies.
        previous_complications: List of past pregnancy complications (e.g., ['preeclampsia', 'gestational diabetes']).
        current_conditions: Current medical conditions (e.g., ['hypertension', 'diabetes', 'obesity']).
        blood_pressure: Current blood pressure reading (e.g., '130/85').
        blood_sugar: Fasting blood glucose in mg/dL.

    Returns:
        dict: Risk assessment with category, risk factors, and management recommendations.
    """
    risk_factors = []
    risk_score = 0

    # Age risk
    if age >= 35:
        risk_factors.append(f"Advanced maternal age ({age})")
        risk_score += 2
    elif age < 18:
        risk_factors.append(f"Adolescent pregnancy ({age})")
        risk_score += 2

    # BP assessment
    try:
        systolic, diastolic = map(int, blood_pressure.split("/"))
        if systolic >= 140 or diastolic >= 90:
            risk_factors.append(f"Hypertension in pregnancy ({blood_pressure})")
            risk_score += 3
        elif systolic >= 130 or diastolic >= 80:
            risk_factors.append(f"Elevated blood pressure ({blood_pressure})")
            risk_score += 1
    except ValueError:
        pass

    # Blood sugar
    if blood_sugar >= 126:
        risk_factors.append(f"Diabetic range glucose ({blood_sugar} mg/dL)")
        risk_score += 3
    elif blood_sugar >= 92:
        risk_factors.append(f"Gestational diabetes range ({blood_sugar} mg/dL)")
        risk_score += 2

    # Previous complications
    high_risk_complications = ["preeclampsia", "eclampsia", "placental abruption", "preterm birth", "stillbirth"]
    for comp in previous_complications:
        if comp.lower() in high_risk_complications:
            risk_factors.append(f"History of {comp}")
            risk_score += 2

    # Current conditions
    for condition in current_conditions:
        condition_lower = condition.lower()
        if condition_lower in ["hypertension", "diabetes", "autoimmune disease", "kidney disease"]:
            risk_factors.append(f"Pre-existing {condition}")
            risk_score += 2
        elif condition_lower in ["obesity", "thyroid disorder"]:
            risk_factors.append(f"Current {condition}")
            risk_score += 1

    # Risk categorization
    if risk_score >= 7:
        category = "HIGH RISK"
        monitoring = "Weekly visits, specialist care recommended"
    elif risk_score >= 4:
        category = "MODERATE RISK"
        monitoring = "Bi-weekly visits, additional monitoring recommended"
    else:
        category = "LOW RISK"
        monitoring = "Standard prenatal visit schedule"

    recommendations = [
        f"Gestational age: {gestational_weeks} weeks",
        f"Monitoring frequency: {monitoring}",
    ]
    if gestational_weeks >= 24 and gestational_weeks <= 28:
        recommendations.append("Glucose tolerance test (GTT) recommended at this gestational age")
    if gestational_weeks >= 36:
        recommendations.append("Group B Streptococcus (GBS) screening recommended")
    if risk_score >= 4:
        recommendations.append("Consider referral to Maternal-Fetal Medicine specialist")

    return {
        "status": "assessed",
        "risk_category": category,
        "risk_score": risk_score,
        "risk_factors": risk_factors,
        "gestational_weeks": gestational_weeks,
        "monitoring_plan": monitoring,
        "recommendations": recommendations,
    }


def menstrual_cycle_analysis(
    cycle_length: int,
    period_duration: int,
    flow_intensity: str,
    pain_level: int,
    irregular: bool,
    missed_periods: int,
    associated_symptoms: list[str],
) -> dict:
    """Analyzes menstrual cycle patterns and identifies potential issues.

    Args:
        cycle_length: Average cycle length in days (normal: 21-35).
        period_duration: Duration of menstrual bleeding in days (normal: 2-7).
        flow_intensity: Flow description ('light', 'moderate', 'heavy', 'very_heavy').
        pain_level: Menstrual pain severity 0-10.
        irregular: Whether cycles are irregular.
        missed_periods: Number of missed periods in last 6 months.
        associated_symptoms: Other symptoms (e.g., ['bloating', 'mood swings', 'acne', 'hair growth']).

    Returns:
        dict: Menstrual analysis with potential conditions and recommendations.
    """
    findings = []
    possible_conditions = []
    recommendations = []

    # Cycle length analysis
    if cycle_length < 21:
        findings.append(f"Short cycle ({cycle_length} days) - polymenorrhea")
        possible_conditions.append("Thyroid dysfunction")
        possible_conditions.append("Anovulatory cycles")
    elif cycle_length > 35:
        findings.append(f"Long cycle ({cycle_length} days) - oligomenorrhea")
        possible_conditions.append("Polycystic Ovary Syndrome (PCOS)")
        possible_conditions.append("Thyroid dysfunction")
    else:
        findings.append(f"Normal cycle length ({cycle_length} days)")

    # Period duration
    if period_duration > 7:
        findings.append(f"Prolonged bleeding ({period_duration} days) - menorrhagia")
        possible_conditions.append("Uterine fibroids")
        possible_conditions.append("Endometrial polyps")
        recommendations.append("Check hemoglobin and iron levels")

    # Flow intensity
    if flow_intensity.lower() in ["heavy", "very_heavy"]:
        findings.append(f"Heavy menstrual flow ({flow_intensity})")
        possible_conditions.append("Uterine fibroids")
        recommendations.append("Iron supplementation may be needed")
        if flow_intensity.lower() == "very_heavy":
            recommendations.append("Pelvic ultrasound recommended")

    # Pain
    if pain_level >= 7:
        findings.append(f"Severe dysmenorrhea (pain: {pain_level}/10)")
        possible_conditions.append("Endometriosis")
        possible_conditions.append("Adenomyosis")
        recommendations.append("NSAIDs for pain management")
        recommendations.append("Consider laparoscopy for endometriosis evaluation")
    elif pain_level >= 4:
        findings.append(f"Moderate dysmenorrhea (pain: {pain_level}/10)")

    # Missed periods
    if missed_periods >= 3:
        findings.append(f"Amenorrhea ({missed_periods} missed periods)")
        possible_conditions.append("Pregnancy (must be ruled out first)")
        possible_conditions.append("PCOS")
        possible_conditions.append("Hypothalamic amenorrhea")
        recommendations.append("Pregnancy test as first step")
        recommendations.append("Hormone panel (FSH, LH, Estradiol, Prolactin, TSH)")

    # Associated symptoms analysis
    pcos_symptoms = ["acne", "hair growth", "weight gain", "hair loss"]
    pcos_matches = [s for s in associated_symptoms if s.lower() in pcos_symptoms]
    if len(pcos_matches) >= 2:
        findings.append(f"Multiple PCOS-associated symptoms: {', '.join(pcos_matches)}")
        if "PCOS" not in possible_conditions:
            possible_conditions.append("Polycystic Ovary Syndrome (PCOS)")
        recommendations.append("Pelvic ultrasound to check for polycystic ovaries")
        recommendations.append("Check testosterone, DHEA-S, insulin levels")

    return {
        "status": "analyzed",
        "findings": findings,
        "possible_conditions": list(set(possible_conditions)),
        "recommendations": recommendations,
        "cycle_summary": {
            "cycle_length": cycle_length,
            "period_duration": period_duration,
            "flow": flow_intensity,
            "pain_level": pain_level,
            "irregular": irregular,
            "missed_periods": missed_periods,
        },
    }
