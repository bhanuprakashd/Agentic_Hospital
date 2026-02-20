"""Pediatrics-specific diagnostic and assessment tools."""


def pediatric_growth_assessment(
    age_months: int,
    weight_kg: float,
    height_cm: float,
    head_circumference_cm: float = None,
    gender: str = "male",
) -> dict:
    """Assesses pediatric growth using percentiles and identifies concerns.

    Args:
        age_months: Age in months (0-240 for birth to 20 years).
        weight_kg: Weight in kilograms.
        height_cm: Height/length in centimeters.
        head_circumference_cm: Head circumference in cm (for children ≤ 36 months).
        gender: Gender ('male' or 'female').

    Returns:
        dict: Growth assessment with percentiles and recommendations.
    """
    # Simplified percentile estimation (approximations for common ranges)
    # In practice, these would use actual WHO/CDC growth charts

    def estimate_percentile(value, median, sd):
        """Estimate percentile based on standard deviations from median."""
        import math
        z_score = (value - median) / sd if sd > 0 else 0
        percentile = round(50 * (1 + math.erf(z_score / math.sqrt(2))), 1)
        return max(0.1, min(99.9, percentile))

    # Approximate medians and SDs by age (simplified)
    # For weight (kg)
    if age_months <= 12:
        wt_median = 3.5 + (age_months * 0.6)
        wt_sd = 0.8 + (age_months * 0.1)
    elif age_months <= 36:
        wt_median = 9 + ((age_months - 12) * 0.25)
        wt_sd = 1.2
    elif age_months <= 144:
        wt_median = 14 + ((age_months - 36) * 0.3)
        wt_sd = 3 + (age_months * 0.02)
    else:
        wt_median = 50 + ((age_months - 144) * 0.1)
        wt_sd = 8

    # For height (cm)
    if age_months <= 12:
        ht_median = 50 + (age_months * 2.5)
        ht_sd = 2.5
    elif age_months <= 36:
        ht_median = 75 + ((age_months - 12) * 0.8)
        ht_sd = 3
    elif age_months <= 144:
        ht_median = 95 + ((age_months - 36) * 0.5)
        ht_sd = 5
    else:
        ht_median = 160 + ((age_months - 144) * 0.08)
        ht_sd = 8

    # Adjust for gender
    if gender.lower() == "male":
        wt_median *= 1.02
        ht_median *= 1.01
    else:
        wt_median *= 0.98
        ht_median *= 0.99

    wt_percentile = estimate_percentile(weight_kg, wt_median, wt_sd)
    ht_percentile = estimate_percentile(height_cm, ht_median, ht_sd)

    # BMI calculation for children > 24 months
    bmi = None
    bmi_percentile = None
    if age_months > 24:
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        # BMI percentile estimation (age-dependent)
        if age_months <= 60:
            bmi_median = 15 + (age_months * 0.02)
        elif age_months <= 144:
            bmi_median = 15.5 + ((age_months - 60) * 0.03)
        else:
            bmi_median = 20 + ((age_months - 144) * 0.02)
        bmi_sd = 2
        bmi_percentile = estimate_percentile(bmi, bmi_median, bmi_sd)

    # Head circumference (for ≤ 36 months)
    hc_percentile = None
    if head_circumference_cm and age_months <= 36:
        hc_median = 35 + (age_months * 0.5)
        hc_sd = 1.5
        if gender.lower() == "male":
            hc_median += 0.5
        hc_percentile = estimate_percentile(head_circumference_cm, hc_median, hc_sd)

    # Identify concerns
    concerns = []
    if wt_percentile < 3:
        concerns.append(f"Weight < 3rd percentile - failure to thrive evaluation needed")
    elif wt_percentile < 10:
        concerns.append(f"Weight < 10th percentile - monitor growth closely")
    elif wt_percentile > 97:
        concerns.append(f"Weight > 97th percentile - assess for overweight/obesity")

    if ht_percentile < 3:
        concerns.append(f"Height < 3rd percentile - evaluate for growth disorder")
    elif ht_percentile > 97:
        concerns.append(f"Height > 97th percentile - consider constitutional tall stature")

    if bmi_percentile:
        if bmi_percentile >= 95:
            concerns.append(f"BMI ≥ 95th percentile - OBESITY")
        elif bmi_percentile >= 85:
            concerns.append(f"BMI ≥ 85th percentile - OVERWEIGHT")

    if hc_percentile:
        if hc_percentile < 3:
            concerns.append(f"Head circumference < 3rd percentile - microcephaly evaluation")
        elif hc_percentile > 97:
            concerns.append(f"Head circumference > 97th percentile - macrocephaly evaluation")

    # Recommendations
    recommendations = []
    if wt_percentile < 10 or ht_percentile < 10:
        recommendations.append("Plot on growth chart at each visit")
        recommendations.append("Assess caloric intake and feeding practices")
        recommendations.append("Consider lab work: CBC, CMP, thyroid, celiac panel")
    if bmi_percentile and bmi_percentile >= 85:
        recommendations.append("Nutrition counseling and physical activity guidance")
        recommendations.append("Screen for comorbidities: lipids, glucose, liver function")
    if not concerns:
        recommendations.append("Growth parameters within normal range")
        recommendations.append("Continue routine well-child visits")

    return {
        "status": "assessed",
        "age_months": age_months,
        "gender": gender,
        "weight": {
            "value_kg": weight_kg,
            "percentile": wt_percentile,
        },
        "height": {
            "value_cm": height_cm,
            "percentile": ht_percentile,
        },
        "bmi": {
            "value": round(bmi, 1) if bmi else None,
            "percentile": bmi_percentile,
        } if bmi else None,
        "head_circumference": {
            "value_cm": head_circumference_cm,
            "percentile": hc_percentile,
        } if head_circumference_cm else None,
        "concerns": concerns if concerns else ["No growth concerns identified"],
        "recommendations": recommendations,
    }


def vaccination_tracker(
    age_months: int,
    vaccines_received: list[str],
    high_risk: bool = False,
) -> dict:
    """Tracks vaccination status and recommends catch-up schedule.

    Args:
        age_months: Child's age in months.
        vaccines_received: List of vaccines already received (e.g., ['DTaP1', 'DTaP2', 'MMR1']).
        high_risk: Whether child is high-risk (premature, immunocompromised, etc.).

    Returns:
        dict: Vaccination status and recommended catch-up schedule.
    """
    received_lower = [v.lower() for v in vaccines_received]

    # Standard CDC immunization schedule
    schedule = {
        "Hepatitis B": {
            "doses": 3,
            "ages": [0, 1, 6],  # months
            "min_intervals": [0, 4, 8],  # weeks between doses
        },
        "DTaP": {
            "doses": 5,
            "ages": [2, 4, 6, 15, 48],  # months
            "min_intervals": [0, 4, 4, 26, 26],  # weeks
        },
        "Hib": {
            "doses": 4,
            "ages": [2, 4, 6, 12],
            "min_intervals": [0, 4, 4, 8],
        },
        "IPV (Polio)": {
            "doses": 4,
            "ages": [2, 4, 6, 48],
            "min_intervals": [0, 4, 4, 26],
        },
        "PCV (Pneumococcal)": {
            "doses": 4,
            "ages": [2, 4, 6, 12],
            "min_intervals": [0, 4, 4, 8],
        },
        "Rotavirus": {
            "doses": 3,
            "ages": [2, 4, 6],
            "min_intervals": [0, 4, 4],
            "max_age": 32,  # weeks - cannot start after 15 weeks, must complete by 8 months
        },
        "MMR": {
            "doses": 2,
            "ages": [12, 48],
            "min_intervals": [0, 28],  # days
        },
        "Varicella": {
            "doses": 2,
            "ages": [12, 48],
            "min_intervals": [0, 84],  # days
        },
        "Hepatitis A": {
            "doses": 2,
            "ages": [12, 18],
            "min_intervals": [0, 24],  # weeks
        },
        "Influenza": {
            "doses": 1,  # annually
            "ages": [6],  # can start at 6 months
            "min_intervals": [0],
        },
    }

    due_now = []
    overdue = []
    up_to_date = []
    future = []

    for vaccine, info in schedule.items():
        doses_needed = info["doses"]
        vaccine_lower = vaccine.lower()

        # Count received doses for this vaccine
        doses_received = sum(1 for v in received_lower if vaccine_lower in v or any(
            abbrev in v for abbrev in vaccine_lower.split()[0][:3].lower()
        ))
        doses_remaining = doses_needed - doses_received

        if doses_remaining <= 0:
            up_to_date.append(f"{vaccine}: Complete ({doses_needed}/{doses_needed})")
            continue

        # Check if next dose is due
        next_dose = doses_received + 1
        ages = info["ages"]

        if next_dose <= len(ages):
            age_due = ages[next_dose - 1]
            if age_months >= age_due:
                if age_months > age_due + 2:  # More than 2 months overdue
                    overdue.append(f"{vaccine}: Dose {next_dose} (was due at {age_due} months)")
                else:
                    due_now.append(f"{vaccine}: Dose {next_dose} (due at {age_due} months)")
            else:
                future.append(f"{vaccine}: Dose {next_dose} (due at {age_due} months)")

    # High-risk additions
    high_risk_vaccines = []
    if high_risk:
        if age_months >= 6:
            high_risk_vaccines.append("Consider: Pneumococcal 23 (PPSV23)")
        if age_months >= 24:
            high_risk_vaccines.append("Consider: Meningococcal conjugate (MenACWY)")

    return {
        "status": "assessed",
        "age_months": age_months,
        "vaccines_received": vaccines_received,
        "due_now": due_now if due_now else ["No vaccines currently due"],
        "overdue": overdue if overdue else ["No vaccines overdue"],
        "up_to_date": up_to_date,
        "future_vaccines": future,
        "high_risk_additions": high_risk_vaccines if high_risk else None,
        "catch_up_guidance": [
            "Catch-up vaccination can be done at any visit",
            "Multiple vaccines can be given at the same visit",
            "Use minimum intervals for catch-up schedules",
            "Document all vaccines in state immunization registry",
        ],
    }