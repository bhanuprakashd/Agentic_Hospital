"""Physical Medicine and Rehabilitation-specific assessment tools."""


def functional_independence_assessment(
    self_care_score: int,
    mobility_score: int,
    cognition_score: int,
    communication_score: int,
    psychosocial_score: int,
) -> dict:
    """Assesses functional independence using FIM-like scoring.

    Args:
        self_care_score: Self-care ability score (1-7 scale, 1=totally dependent, 7=independent).
        mobility_score: Mobility/transfers ability score (1-7).
        cognition_score: Cognitive function score (1-7).
        communication_score: Communication ability score (1-7).
        psychosocial_score: Psychosocial adjustment score (1-7).

    Returns:
        dict: Functional independence assessment with recommendations.
    """
    # Score interpretation
    def interpret_score(score):
        if score == 7:
            return "Independent", "No assistance needed"
        elif score == 6:
            return "Modified Independence", "Device needed but no helper"
        elif score == 5:
            return "Supervision", "Helper for safety/setup only"
        elif score == 4:
            return "Minimal Assist", "Performs 75%+ of task"
        elif score == 3:
            return "Moderate Assist", "Performs 50-74% of task"
        elif score == 2:
            return "Maximal Assist", "Performs 25-49% of task"
        else:
            return "Total Assist", "Performs < 25% of task"

    domains = {
        "self_care": {"score": self_care_score, "interpret": interpret_score(self_care_score)},
        "mobility": {"score": mobility_score, "interpret": interpret_score(mobility_score)},
        "cognition": {"score": cognition_score, "interpret": interpret_score(cognition_score)},
        "communication": {"score": communication_score, "interpret": interpret_score(communication_score)},
        "psychosocial": {"score": psychosocial_score, "interpret": interpret_score(psychosocial_score)},
    }

    total_score = self_care_score + mobility_score + cognition_score + communication_score + psychosocial_score
    max_score = 35

    # Overall independence level
    independence_percent = (total_score / max_score) * 100

    if independence_percent >= 90:
        overall_level = "INDEPENDENT"
        disposition = "Can live independently with minimal support"
    elif independence_percent >= 75:
        overall_level = "MOSTLY INDEPENDENT"
        disposition = "Can live independently with some assistance"
    elif independence_percent >= 50:
        overall_level = "PARTIALLY INDEPENDENT"
        disposition = "Requires moderate assistance, consider assisted living or home health"
    elif independence_percent >= 25:
        overall_level = "SIGNIFICANTLY DEPENDENT"
        disposition = "Requires substantial assistance, consider skilled nursing facility"
    else:
        overall_level = "TOTALLY DEPENDENT"
        disposition = "Requires 24-hour care"

    # Recommendations by domain
    recommendations = []

    if self_care_score < 5:
        recommendations.append("Occupational therapy: ADL training, adaptive equipment")
        if self_care_score < 3:
            recommendations.append("Consider home health aide for personal care assistance")

    if mobility_score < 5:
        recommendations.append("Physical therapy: gait training, transfer techniques")
        if mobility_score < 3:
            recommendations.append("Consider wheelchair/mobility device evaluation")
            recommendations.append("Home safety evaluation for modifications")

    if cognition_score < 5:
        recommendations.append("Cognitive rehabilitation therapy")
        if cognition_score < 3:
            recommendations.append("24-hour supervision recommended for safety")

    if communication_score < 5:
        recommendations.append("Speech-language therapy evaluation")
        if communication_score < 3:
            recommendations.append("Consider augmentative communication devices")

    if psychosocial_score < 5:
        recommendations.append("Psychology/counseling services")
        recommendations.append("Social work for support resources")

    return {
        "status": "assessed",
        "domain_scores": {
            "self_care": {
                "score": self_care_score,
                "level": domains["self_care"]["interpret"][0],
                "description": domains["self_care"]["interpret"][1],
            },
            "mobility": {
                "score": mobility_score,
                "level": domains["mobility"]["interpret"][0],
                "description": domains["mobility"]["interpret"][1],
            },
            "cognition": {
                "score": cognition_score,
                "level": domains["cognition"]["interpret"][0],
                "description": domains["cognition"]["interpret"][1],
            },
            "communication": {
                "score": communication_score,
                "level": domains["communication"]["interpret"][0],
                "description": domains["communication"]["interpret"][1],
            },
            "psychosocial": {
                "score": psychosocial_score,
                "level": domains["psychosocial"]["interpret"][0],
                "description": domains["psychosocial"]["interpret"][1],
            },
        },
        "total_score": total_score,
        "max_score": max_score,
        "independence_percentage": round(independence_percent, 1),
        "overall_level": overall_level,
        "disposition_recommendation": disposition,
        "therapy_recommendations": recommendations if recommendations else ["Continue current level of functioning"],
    }


def stroke_rehabilitation_prognosis(
    days_since_stroke: int,
    initial_nihss: int,
    current_nihss: int,
    age: int,
    stroke_type: str,
    comorbidities: list[str],
    social_support: str,
) -> dict:
    """Assesses stroke rehabilitation prognosis and recovery potential.

    Args:
        days_since_stroke: Days since stroke onset.
        initial_nihss: Initial NIH Stroke Scale score (0-42, higher = worse).
        current_nihss: Current NIH Stroke Scale score.
        age: Patient age in years.
        stroke_type: Type of stroke ('ischemic', 'hemorrhagic').
        comorbidities: List of comorbidities (e.g., ['diabetes', 'atrial_fibrillation']).
        social_support: Level of social support ('strong', 'moderate', 'limited', 'none').

    Returns:
        dict: Stroke rehabilitation prognosis with therapy recommendations.
    """
    # NIHSS improvement
    nihss_improvement = initial_nihss - current_nihss
    improvement_rate = nihss_improvement / days_since_stroke if days_since_stroke > 0 else 0

    # Severity classification
    if current_nihss <= 4:
        severity = "Mild"
    elif current_nihss <= 15:
        severity = "Moderate"
    elif current_nihss <= 25:
        severity = "Severe"
    else:
        severity = "Very Severe"

    # Recovery phase
    if days_since_stroke <= 7:
        phase = "Acute"
        recovery_window = "Rapid recovery expected in first 3 months"
    elif days_since_stroke <= 90:
        phase = "Subacute"
        recovery_window = "Active recovery continues; neuroplasticity window"
    elif days_since_stroke <= 180:
        phase = "Early Chronic"
        recovery_window = "Slower recovery but improvement still possible"
    else:
        phase = "Chronic"
        recovery_window = "Maintenance phase; focus on compensation strategies"

    # Prognostic factors
    positive_factors = []
    negative_factors = []

    if current_nihss <= 10:
        positive_factors.append("Mild to moderate deficit")
    else:
        negative_factors.append("Severe initial deficit")

    if age < 65:
        positive_factors.append("Younger age")
    elif age > 80:
        negative_factors.append("Advanced age")

    if nihss_improvement > 4:
        positive_factors.append("Good early improvement")
    elif nihss_improvement < 2:
        negative_factors.append("Limited early improvement")

    if stroke_type == "ischemic":
        positive_factors.append("Ischemic stroke (better prognosis than hemorrhagic)")
    else:
        negative_factors.append("Hemorrhagic stroke")

    if social_support in ["strong", "moderate"]:
        positive_factors.append(f"{social_support.capitalize()} social support")
    else:
        negative_factors.append(f"Limited social support")

    high_risk_comorbidities = ["dementia", "heart_failure", "end_stage_renal_disease", "cancer"]
    for comorbidity in comorbidities:
        if comorbidity.lower() in high_risk_comorbidities:
            negative_factors.append(f"Comorbidity: {comorbidity}")

    # Prognosis determination
    if len(positive_factors) >= 3 and len(negative_factors) <= 1:
        prognosis = "GOOD"
        expected_outcome = "Likely to achieve independent ambulation and ADLs with therapy"
    elif len(negative_factors) >= 3:
        prognosis = "GUARDED"
        expected_outcome = "May require long-term assistance; focus on maximizing function"
    else:
        prognosis = "MODERATE"
        expected_outcome = "Expected to make functional gains with intensive rehabilitation"

    # Therapy recommendations
    therapies = [
        "Physical therapy: gait training, balance, strength",
        "Occupational therapy: ADL training, upper extremity function",
        "Speech therapy: communication, swallowing evaluation",
    ]

    if current_nihss > 10:
        therapies.append("Consider inpatient rehabilitation facility (IRF)")
    elif current_nihss > 5:
        therapies.append("Consider acute rehabilitation or intensive outpatient")
    else:
        therapies.append("Outpatient therapy may be appropriate")

    if social_support in ["limited", "none"]:
        therapies.append("Social work: arrange home health services, support resources")

    return {
        "status": "assessed",
        "recovery_phase": phase,
        "days_since_stroke": days_since_stroke,
        "stroke_severity": severity,
        "nihss": {
            "initial": initial_nihss,
            "current": current_nihss,
            "improvement": nihss_improvement,
            "improvement_rate_per_day": round(improvement_rate, 2),
        },
        "prognosis": prognosis,
        "expected_outcome": expected_outcome,
        "positive_prognostic_factors": positive_factors if positive_factors else ["None identified"],
        "negative_prognostic_factors": negative_factors if negative_factors else ["None identified"],
        "recovery_window": recovery_window,
        "recommended_therapies": therapies,
        "follow_up": f"Reassess functional status in {14 if phase == 'Acute' else 30} days",
    }