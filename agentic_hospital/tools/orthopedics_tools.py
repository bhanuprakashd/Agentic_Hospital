"""Orthopedics-specific diagnostic and assessment tools."""


def fracture_risk_assessment(
    age: int,
    gender: str,
    bone_density_t_score: float,
    previous_fracture: bool,
    fall_history: bool,
    steroid_use: bool,
    smoking: bool,
    alcohol_heavy: bool,
    rheumatoid_arthritis: bool,
) -> dict:
    """Assesses fracture risk using FRAX-like scoring factors.

    Args:
        age: Patient age in years.
        gender: Patient gender ('male' or 'female').
        bone_density_t_score: DEXA scan T-score (normal >= -1.0, osteopenia -1.0 to -2.5, osteoporosis < -2.5).
        previous_fracture: Whether patient has had a previous fragility fracture.
        fall_history: Whether patient has a history of falls.
        steroid_use: Whether patient uses glucocorticoids.
        smoking: Whether patient currently smokes.
        alcohol_heavy: Whether patient consumes 3+ units of alcohol daily.
        rheumatoid_arthritis: Whether patient has rheumatoid arthritis.

    Returns:
        dict: Fracture risk assessment with recommendations.
    """
    risk_score = 0
    risk_factors = []

    # Age
    if age >= 70:
        risk_score += 3
        risk_factors.append(f"Advanced age ({age})")
    elif age >= 50:
        risk_score += 1

    # Gender
    if gender.lower() == "female" and age >= 50:
        risk_score += 1
        risk_factors.append("Post-menopausal female")

    # Bone density
    if bone_density_t_score <= -2.5:
        risk_score += 4
        risk_factors.append(f"Osteoporosis (T-score: {bone_density_t_score})")
    elif bone_density_t_score <= -1.0:
        risk_score += 2
        risk_factors.append(f"Osteopenia (T-score: {bone_density_t_score})")

    if previous_fracture:
        risk_score += 3
        risk_factors.append("Previous fragility fracture")
    if fall_history:
        risk_score += 2
        risk_factors.append("History of falls")
    if steroid_use:
        risk_score += 2
        risk_factors.append("Glucocorticoid use")
    if smoking:
        risk_score += 1
        risk_factors.append("Current smoker")
    if alcohol_heavy:
        risk_score += 1
        risk_factors.append("Heavy alcohol use")
    if rheumatoid_arthritis:
        risk_score += 1
        risk_factors.append("Rheumatoid arthritis")

    # Risk level
    if risk_score >= 8:
        risk_level = "HIGH"
        ten_year_risk = "20%+"
    elif risk_score >= 4:
        risk_level = "MODERATE"
        ten_year_risk = "10-20%"
    else:
        risk_level = "LOW"
        ten_year_risk = "<10%"

    recommendations = []
    if bone_density_t_score <= -2.5:
        recommendations.append("Consider bisphosphonate therapy (alendronate, risedronate)")
    if bone_density_t_score <= -1.0:
        recommendations.append("Calcium (1200mg/day) and Vitamin D (800-1000 IU/day) supplementation")
    if fall_history:
        recommendations.append("Fall prevention program: balance exercises, home safety assessment")
    recommendations.append("Weight-bearing exercise (walking, light resistance training)")
    if risk_score >= 4:
        recommendations.append("Repeat DEXA scan in 1-2 years")
    else:
        recommendations.append("Repeat DEXA scan in 2-5 years")

    return {
        "status": "assessed",
        "risk_level": risk_level,
        "risk_score": risk_score,
        "estimated_10_year_fracture_risk": ten_year_risk,
        "bone_density_classification": "Osteoporosis" if bone_density_t_score <= -2.5 else "Osteopenia" if bone_density_t_score <= -1.0 else "Normal",
        "risk_factors": risk_factors,
        "recommendations": recommendations,
    }


def joint_mobility_score(
    joint: str,
    flexion: int,
    extension: int,
    pain_with_movement: int,
    swelling: bool,
    crepitus: bool,
    instability: bool,
) -> dict:
    """Evaluates joint range of motion and functional status.

    Args:
        joint: Joint being assessed (e.g., 'knee', 'shoulder', 'hip', 'elbow', 'ankle').
        flexion: Flexion angle in degrees.
        extension: Extension angle in degrees (use negative for hyperextension).
        pain_with_movement: Pain level during movement (0-10).
        swelling: Whether joint swelling is present.
        crepitus: Whether crepitus (grinding/cracking) is noted.
        instability: Whether joint instability is detected.

    Returns:
        dict: Joint assessment with functional status and recommendations.
    """
    # Normal ranges by joint (approximate)
    normal_ranges = {
        "knee": {"flexion": 135, "extension": 0},
        "shoulder": {"flexion": 180, "extension": 60},
        "hip": {"flexion": 120, "extension": 30},
        "elbow": {"flexion": 150, "extension": 0},
        "ankle": {"flexion": 50, "extension": 20},
        "wrist": {"flexion": 80, "extension": 70},
    }

    joint_lower = joint.lower()
    normal = normal_ranges.get(joint_lower, {"flexion": 120, "extension": 30})

    flexion_deficit = max(0, normal["flexion"] - flexion)
    extension_deficit = max(0, abs(extension) - normal["extension"]) if extension < 0 else max(0, normal["extension"] - extension)

    # Functional score (0-100)
    flex_pct = min(100, (flexion / normal["flexion"]) * 100)
    functional_score = flex_pct

    if pain_with_movement >= 7: functional_score -= 30
    elif pain_with_movement >= 4: functional_score -= 15

    if swelling: functional_score -= 10
    if instability: functional_score -= 15
    if crepitus: functional_score -= 5

    functional_score = max(0, round(functional_score))

    findings = []
    if flexion_deficit > 20:
        findings.append(f"Significant flexion limitation ({flexion}° vs normal {normal['flexion']}°)")
    if pain_with_movement >= 7:
        findings.append(f"Severe pain with movement ({pain_with_movement}/10)")
    if swelling:
        findings.append("Joint effusion/swelling present")
    if crepitus:
        findings.append("Crepitus noted - suggestive of degenerative changes")
    if instability:
        findings.append("Joint instability detected - ligamentous injury possible")

    if functional_score >= 80:
        status = "GOOD"
    elif functional_score >= 60:
        status = "FAIR"
    elif functional_score >= 40:
        status = "POOR"
    else:
        status = "SEVERELY IMPAIRED"

    recommendations = []
    if pain_with_movement >= 4:
        recommendations.append("Pain management: NSAIDs, ice/heat therapy")
    if functional_score < 80:
        recommendations.append("Physical therapy referral for range of motion exercises")
    if instability:
        recommendations.append("MRI recommended to evaluate ligamentous structures")
    if crepitus and pain_with_movement >= 4:
        recommendations.append("X-ray to evaluate for osteoarthritis")
    if functional_score < 40:
        recommendations.append("Consider surgical consultation")

    return {
        "status": "evaluated",
        "joint": joint,
        "functional_score": functional_score,
        "functional_status": status,
        "range_of_motion": {
            "flexion": f"{flexion}° (normal: {normal['flexion']}°)",
            "extension": f"{extension}° (normal: {normal['extension']}°)",
        },
        "findings": findings,
        "recommendations": recommendations,
    }
