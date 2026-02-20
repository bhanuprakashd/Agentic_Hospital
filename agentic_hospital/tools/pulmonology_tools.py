"""Pulmonology-specific diagnostic and assessment tools."""


def spirometry_interpretation(
    fev1_actual: float,
    fev1_predicted: float,
    fvc_actual: float,
    fvc_predicted: float,
    age: int,
    smoker: bool,
) -> dict:
    """Interprets spirometry (pulmonary function test) results.

    Args:
        fev1_actual: Actual FEV1 in liters.
        fev1_predicted: Predicted FEV1 in liters for patient demographics.
        fvc_actual: Actual FVC in liters.
        fvc_predicted: Predicted FVC in liters for patient demographics.
        age: Patient age.
        smoker: Whether patient is a smoker.

    Returns:
        dict: Spirometry interpretation with obstruction/restriction pattern and severity.
    """
    fev1_pct = (fev1_actual / fev1_predicted) * 100 if fev1_predicted > 0 else 0
    fvc_pct = (fvc_actual / fvc_predicted) * 100 if fvc_predicted > 0 else 0
    fev1_fvc_ratio = (fev1_actual / fvc_actual) * 100 if fvc_actual > 0 else 0

    # Pattern determination
    if fev1_fvc_ratio < 70:
        # Obstructive pattern
        pattern = "OBSTRUCTIVE"
        if fev1_pct >= 80:
            severity = "MILD obstruction"
            gold_stage = "GOLD 1" if smoker else "Mild"
        elif fev1_pct >= 50:
            severity = "MODERATE obstruction"
            gold_stage = "GOLD 2" if smoker else "Moderate"
        elif fev1_pct >= 30:
            severity = "SEVERE obstruction"
            gold_stage = "GOLD 3" if smoker else "Severe"
        else:
            severity = "VERY SEVERE obstruction"
            gold_stage = "GOLD 4" if smoker else "Very Severe"
        possible_conditions = ["COPD", "Asthma", "Bronchiectasis"]
    elif fvc_pct < 80 and fev1_fvc_ratio >= 70:
        pattern = "RESTRICTIVE"
        severity = "Restrictive defect"
        gold_stage = "N/A"
        possible_conditions = ["Interstitial Lung Disease", "Pulmonary Fibrosis", "Chest Wall Disorders", "Neuromuscular Disease"]
    elif fev1_pct < 80 and fvc_pct < 80:
        pattern = "MIXED"
        severity = "Mixed obstructive and restrictive"
        gold_stage = "N/A"
        possible_conditions = ["Combined COPD + restriction", "Advanced lung disease"]
    else:
        pattern = "NORMAL"
        severity = "Normal spirometry"
        gold_stage = "N/A"
        possible_conditions = []

    recommendations = []
    if pattern == "OBSTRUCTIVE":
        recommendations.append("Post-bronchodilator testing to assess reversibility (asthma vs COPD)")
        if smoker:
            recommendations.append("Smoking cessation is the most important intervention")
        recommendations.append("Consider inhaler therapy based on symptom severity")
    if pattern == "RESTRICTIVE":
        recommendations.append("Full pulmonary function tests (lung volumes, DLCO)")
        recommendations.append("High-resolution CT chest recommended")
    if fev1_pct < 50:
        recommendations.append("Pulmonary rehabilitation referral")
        recommendations.append("Assess need for supplemental oxygen")

    return {
        "status": "interpreted",
        "pattern": pattern,
        "severity": severity,
        "gold_stage": gold_stage,
        "values": {
            "FEV1": f"{fev1_actual}L ({fev1_pct:.0f}% predicted)",
            "FVC": f"{fvc_actual}L ({fvc_pct:.0f}% predicted)",
            "FEV1/FVC": f"{fev1_fvc_ratio:.0f}%",
        },
        "possible_conditions": possible_conditions,
        "recommendations": recommendations,
    }


def asthma_control_score(
    daytime_symptoms_per_week: int,
    nighttime_awakenings_per_month: int,
    rescue_inhaler_use_per_week: int,
    activity_limitation: bool,
    fev1_percent_predicted: float,
    exacerbations_past_year: int,
) -> dict:
    """Assesses asthma control level based on GINA guidelines.

    Args:
        daytime_symptoms_per_week: Number of days with symptoms per week (0-7).
        nighttime_awakenings_per_month: Number of nighttime awakenings due to asthma per month.
        rescue_inhaler_use_per_week: Number of times rescue inhaler used per week.
        activity_limitation: Whether asthma limits physical activity.
        fev1_percent_predicted: FEV1 as percentage of predicted.
        exacerbations_past_year: Number of asthma exacerbations requiring oral steroids in past year.

    Returns:
        dict: Asthma control assessment with step therapy recommendations.
    """
    uncontrolled_criteria = 0

    if daytime_symptoms_per_week > 2:
        uncontrolled_criteria += 1
    if nighttime_awakenings_per_month > 0:
        uncontrolled_criteria += 1
    if rescue_inhaler_use_per_week > 2:
        uncontrolled_criteria += 1
    if activity_limitation:
        uncontrolled_criteria += 1

    # Control level
    if uncontrolled_criteria == 0:
        control_level = "WELL CONTROLLED"
        action = "Maintain current therapy. Consider step-down if controlled for 3+ months."
    elif uncontrolled_criteria <= 2:
        control_level = "PARTLY CONTROLLED"
        action = "Consider stepping up therapy. Review inhaler technique and adherence first."
    else:
        control_level = "UNCONTROLLED"
        action = "Step up therapy. Assess for modifiable risk factors. Consider specialist referral."

    # Step recommendation
    if uncontrolled_criteria == 0 and rescue_inhaler_use_per_week <= 2:
        step = "Step 1-2: Low-dose ICS or as-needed ICS-formoterol"
    elif uncontrolled_criteria <= 2:
        step = "Step 3: Low-dose ICS-LABA (e.g., budesonide-formoterol)"
    elif fev1_percent_predicted < 60:
        step = "Step 5: High-dose ICS-LABA + add-on therapy (tiotropium, biologic)"
    else:
        step = "Step 4: Medium/high-dose ICS-LABA"

    risk_assessment = []
    if exacerbations_past_year >= 2:
        risk_assessment.append("HIGH risk of future exacerbations (2+ in past year)")
    if fev1_percent_predicted < 60:
        risk_assessment.append("Low lung function increases exacerbation risk")
    if rescue_inhaler_use_per_week > 7:
        risk_assessment.append("Excessive rescue inhaler use - poor control indicator")

    return {
        "status": "assessed",
        "control_level": control_level,
        "uncontrolled_criteria_met": uncontrolled_criteria,
        "recommended_action": action,
        "step_therapy": step,
        "risk_assessment": risk_assessment,
        "current_indicators": {
            "daytime_symptoms": f"{daytime_symptoms_per_week}/week",
            "nighttime_awakenings": f"{nighttime_awakenings_per_month}/month",
            "rescue_inhaler_use": f"{rescue_inhaler_use_per_week}/week",
            "activity_limitation": activity_limitation,
            "FEV1_predicted": f"{fev1_percent_predicted}%",
            "exacerbations_past_year": exacerbations_past_year,
        },
        "general_measures": [
            "Verify inhaler technique at every visit",
            "Ensure medication adherence",
            "Written asthma action plan",
            "Avoid known triggers",
            "Annual flu vaccination",
        ],
    }
