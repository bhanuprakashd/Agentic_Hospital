"""Cardiology-specific diagnostic and assessment tools."""


def analyze_ecg(
    heart_rate: int,
    rhythm: str,
    pr_interval: int,
    qrs_duration: int,
    qt_interval: int,
    st_segment: str,
) -> dict:
    """Analyzes ECG/EKG readings and provides interpretation.

    Args:
        heart_rate: Heart rate in bpm from ECG.
        rhythm: Rhythm description (e.g., 'regular', 'irregular', 'irregularly_irregular').
        pr_interval: PR interval in milliseconds (normal: 120-200ms).
        qrs_duration: QRS complex duration in milliseconds (normal: 80-120ms).
        qt_interval: QT interval in milliseconds (normal: 350-450ms).
        st_segment: ST segment finding (e.g., 'normal', 'elevated', 'depressed').

    Returns:
        dict: ECG interpretation with findings and recommendations.
    """
    findings = []
    abnormalities = []

    # Heart rate analysis
    if heart_rate > 100:
        abnormalities.append(f"Tachycardia ({heart_rate} bpm)")
    elif heart_rate < 60:
        findings.append(f"Bradycardia ({heart_rate} bpm) - may be normal in athletes")
    else:
        findings.append(f"Normal heart rate ({heart_rate} bpm)")

    # Rhythm
    if rhythm.lower() == "irregularly_irregular":
        abnormalities.append("Irregularly irregular rhythm - suggestive of Atrial Fibrillation")
    elif rhythm.lower() == "irregular":
        abnormalities.append("Irregular rhythm - further evaluation needed")
    else:
        findings.append("Regular sinus rhythm")

    # PR interval
    if pr_interval > 200:
        abnormalities.append(f"Prolonged PR interval ({pr_interval}ms) - suggestive of 1st degree AV block")
    elif pr_interval < 120:
        abnormalities.append(f"Short PR interval ({pr_interval}ms) - consider pre-excitation (WPW syndrome)")
    else:
        findings.append(f"Normal PR interval ({pr_interval}ms)")

    # QRS duration
    if qrs_duration > 120:
        abnormalities.append(f"Wide QRS ({qrs_duration}ms) - consider bundle branch block or ventricular origin")
    else:
        findings.append(f"Normal QRS duration ({qrs_duration}ms)")

    # QT interval
    if qt_interval > 470:
        abnormalities.append(f"Prolonged QT ({qt_interval}ms) - risk of Torsades de Pointes")
    elif qt_interval < 350:
        abnormalities.append(f"Short QT ({qt_interval}ms) - associated with arrhythmia risk")
    else:
        findings.append(f"Normal QT interval ({qt_interval}ms)")

    # ST segment
    if st_segment.lower() == "elevated":
        abnormalities.append("ST elevation - URGENT: Consider acute MI (STEMI). Immediate cardiology consult needed.")
    elif st_segment.lower() == "depressed":
        abnormalities.append("ST depression - suggestive of ischemia or NSTEMI. Further evaluation needed.")
    else:
        findings.append("Normal ST segment")

    overall = "ABNORMAL - Review findings" if abnormalities else "NORMAL"

    return {
        "status": "analyzed",
        "overall_interpretation": overall,
        "normal_findings": findings,
        "abnormalities": abnormalities,
        "recommendations": [
            "Compare with prior ECGs if available",
            "Correlate with clinical symptoms",
        ] + (["URGENT: Consider emergent cardiac catheterization"] if "elevated" in st_segment.lower() else []),
    }


def assess_cardiac_risk(
    age: int,
    gender: str,
    systolic_bp: int,
    total_cholesterol: int,
    hdl_cholesterol: int,
    smoker: bool,
    diabetic: bool,
    on_bp_medication: bool,
) -> dict:
    """Calculates 10-year cardiovascular risk score based on Framingham-like risk factors.

    Args:
        age: Patient age in years.
        gender: Patient gender ('male' or 'female').
        systolic_bp: Systolic blood pressure in mmHg.
        total_cholesterol: Total cholesterol in mg/dL.
        hdl_cholesterol: HDL cholesterol in mg/dL.
        smoker: Whether the patient currently smokes.
        diabetic: Whether the patient has diabetes.
        on_bp_medication: Whether the patient is on blood pressure medication.

    Returns:
        dict: Risk assessment with score, category, and recommendations.
    """
    risk_score = 0

    # Age scoring
    if gender.lower() == "male":
        if age >= 70: risk_score += 12
        elif age >= 60: risk_score += 10
        elif age >= 50: risk_score += 8
        elif age >= 40: risk_score += 5
        else: risk_score += 2
    else:
        if age >= 70: risk_score += 10
        elif age >= 60: risk_score += 8
        elif age >= 50: risk_score += 6
        elif age >= 40: risk_score += 3
        else: risk_score += 1

    # Cholesterol scoring
    if total_cholesterol >= 280: risk_score += 4
    elif total_cholesterol >= 240: risk_score += 3
    elif total_cholesterol >= 200: risk_score += 1

    # HDL scoring (protective)
    if hdl_cholesterol >= 60: risk_score -= 2
    elif hdl_cholesterol < 40: risk_score += 3
    elif hdl_cholesterol < 50: risk_score += 1

    # Blood pressure
    if on_bp_medication:
        if systolic_bp >= 160: risk_score += 5
        elif systolic_bp >= 140: risk_score += 4
        elif systolic_bp >= 130: risk_score += 3
        else: risk_score += 2
    else:
        if systolic_bp >= 160: risk_score += 4
        elif systolic_bp >= 140: risk_score += 3
        elif systolic_bp >= 130: risk_score += 2

    # Smoking
    if smoker: risk_score += 4

    # Diabetes
    if diabetic: risk_score += 3

    # Calculate approximate 10-year risk percentage
    if risk_score <= 5:
        risk_percent = 2
        category = "LOW"
    elif risk_score <= 10:
        risk_percent = 8
        category = "MODERATE"
    elif risk_score <= 15:
        risk_percent = 15
        category = "HIGH"
    elif risk_score <= 20:
        risk_percent = 25
        category = "VERY HIGH"
    else:
        risk_percent = 35
        category = "CRITICAL"

    recommendations = []
    if smoker:
        recommendations.append("Smoking cessation is the single most impactful lifestyle change")
    if total_cholesterol >= 200:
        recommendations.append("Discuss statin therapy for cholesterol management")
    if systolic_bp >= 130:
        recommendations.append("Optimize blood pressure control")
    if diabetic:
        recommendations.append("Tight glycemic control to reduce cardiovascular risk")
    if hdl_cholesterol < 40:
        recommendations.append("Increase HDL through exercise and dietary changes")
    recommendations.append("Regular exercise (150 min/week moderate intensity)")
    recommendations.append("Heart-healthy diet (Mediterranean or DASH diet)")

    return {
        "status": "assessed",
        "risk_score": risk_score,
        "estimated_10_year_risk": f"{risk_percent}%",
        "risk_category": category,
        "risk_factors": {
            "age": age,
            "gender": gender,
            "systolic_bp": systolic_bp,
            "total_cholesterol": total_cholesterol,
            "hdl_cholesterol": hdl_cholesterol,
            "smoker": smoker,
            "diabetic": diabetic,
            "on_bp_medication": on_bp_medication,
        },
        "recommendations": recommendations,
    }
