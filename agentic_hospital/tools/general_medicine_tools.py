"""General Medicine diagnostic and assessment tools."""


def bmi_calculator(weight_kg: float, height_cm: float, age: int, gender: str) -> dict:
    """Calculates BMI and provides health assessment.

    Args:
        weight_kg: Weight in kilograms.
        height_cm: Height in centimeters.
        age: Patient age in years.
        gender: Patient gender ('male' or 'female').

    Returns:
        dict: BMI calculation with classification and health recommendations.
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 1)

    if bmi < 18.5:
        category = "UNDERWEIGHT"
        health_risk = "Increased risk of nutritional deficiency, osteoporosis, decreased immunity"
        recommendations = [
            "Nutritional assessment and counseling",
            "Screen for eating disorders if applicable",
            "Check thyroid function, CBC",
            "Calorie-dense nutritious diet",
        ]
    elif bmi < 25:
        category = "NORMAL WEIGHT"
        health_risk = "Low risk"
        recommendations = [
            "Maintain healthy diet and regular exercise",
            "Annual preventive health screening",
        ]
    elif bmi < 30:
        category = "OVERWEIGHT"
        health_risk = "Increased risk of cardiovascular disease, Type 2 diabetes, hypertension"
        recommendations = [
            "Lifestyle modifications: diet and exercise",
            "Target 5-10% weight reduction",
            "Screen for metabolic syndrome",
            "Check fasting glucose, lipid panel, blood pressure",
        ]
    elif bmi < 35:
        category = "OBESITY CLASS I"
        health_risk = "High risk of obesity-related comorbidities"
        recommendations = [
            "Structured weight management program",
            "Consider dietitian referral",
            "Screen for diabetes (HbA1c), dyslipidemia, sleep apnea",
            "Regular exercise: 150-300 min/week",
            "Consider pharmacotherapy if lifestyle measures insufficient",
        ]
    elif bmi < 40:
        category = "OBESITY CLASS II"
        health_risk = "Very high risk of obesity-related comorbidities"
        recommendations = [
            "Multidisciplinary weight management (diet, exercise, behavioral therapy)",
            "Pharmacotherapy recommended",
            "Screen for sleep apnea, NAFLD, joint problems",
            "Consider bariatric surgery evaluation if BMI >= 35 with comorbidities",
        ]
    else:
        category = "OBESITY CLASS III (MORBID)"
        health_risk = "Extremely high risk - significant mortality risk"
        recommendations = [
            "Bariatric surgery evaluation strongly recommended",
            "Comprehensive metabolic workup",
            "Multidisciplinary team management",
            "Screen for all obesity-related comorbidities",
        ]

    ideal_bmi = 22
    ideal_weight = ideal_bmi * (height_m ** 2)

    return {
        "status": "calculated",
        "bmi": bmi,
        "category": category,
        "health_risk": health_risk,
        "measurements": {
            "weight": f"{weight_kg} kg",
            "height": f"{height_cm} cm",
            "ideal_weight_range": f"{round(18.5 * height_m**2, 1)} - {round(24.9 * height_m**2, 1)} kg",
        },
        "recommendations": recommendations,
    }


def vaccination_schedule(age: int, gender: str, conditions: list[str], vaccinations_received: list[str]) -> dict:
    """Provides recommended vaccination schedule based on age, gender, and conditions.

    Args:
        age: Patient age in years.
        gender: Patient gender ('male' or 'female').
        conditions: List of medical conditions (e.g., ['diabetes', 'asthma', 'immunocompromised']).
        vaccinations_received: List of vaccinations already received (e.g., ['flu_2024', 'covid_booster', 'tdap']).

    Returns:
        dict: Recommended vaccinations with schedule and rationale.
    """
    recommended = []
    received_lower = [v.lower() for v in vaccinations_received]

    # Annual flu vaccine (everyone 6+ months)
    if not any("flu" in v for v in received_lower):
        recommended.append({
            "vaccine": "Influenza (Flu)",
            "schedule": "Annually (every fall/winter)",
            "rationale": "Annual flu vaccination recommended for all adults",
        })

    # COVID-19 booster
    if not any("covid" in v for v in received_lower):
        recommended.append({
            "vaccine": "COVID-19 Updated Vaccine",
            "schedule": "Annually or per CDC recommendations",
            "rationale": "Updated COVID vaccination for current variants",
        })

    # Tdap/Td
    if not any("tdap" in v or "td " in v for v in received_lower):
        recommended.append({
            "vaccine": "Tdap/Td (Tetanus, Diphtheria, Pertussis)",
            "schedule": "Tdap once, then Td booster every 10 years",
            "rationale": "Tetanus protection and pertussis prevention",
        })

    # Shingles (50+)
    if age >= 50 and not any("shingrix" in v or "shingles" in v for v in received_lower):
        recommended.append({
            "vaccine": "Shingrix (Recombinant Zoster)",
            "schedule": "2 doses, 2-6 months apart",
            "rationale": "Shingles prevention for adults 50+",
        })

    # Pneumococcal (65+ or high-risk)
    high_risk_pneumo = any(c.lower() in ["diabetes", "copd", "asthma", "heart disease", "immunocompromised", "kidney disease"] for c in conditions)
    if (age >= 65 or high_risk_pneumo) and not any("pneumo" in v or "prevnar" in v for v in received_lower):
        recommended.append({
            "vaccine": "PCV20 (Prevnar 20) or PCV15 + PPSV23",
            "schedule": "Per CDC pneumococcal vaccine guidelines",
            "rationale": "Pneumococcal disease prevention" + (" (high-risk condition)" if high_risk_pneumo else " (age 65+)"),
        })

    # HPV (through age 26, catch-up through 45)
    if age <= 45 and not any("hpv" in v or "gardasil" in v for v in received_lower):
        recommended.append({
            "vaccine": "HPV (Gardasil 9)",
            "schedule": "2-3 dose series depending on age at first dose",
            "rationale": "Cancer prevention (cervical, oropharyngeal, anal, others)",
        })

    # Hepatitis B
    if age <= 59 and not any("hep b" in v or "hepatitis b" in v for v in received_lower):
        recommended.append({
            "vaccine": "Hepatitis B",
            "schedule": "2 or 3 dose series",
            "rationale": "Hepatitis B prevention for adults under 60",
        })

    # RSV (60+ or pregnant 32-36 weeks)
    if age >= 60 and not any("rsv" in v for v in received_lower):
        recommended.append({
            "vaccine": "RSV Vaccine",
            "schedule": "Single dose (shared decision with provider)",
            "rationale": "RSV prevention for adults 60+",
        })

    # High-risk: Hepatitis A
    if any(c.lower() in ["liver disease", "hepatitis c", "travel"] for c in conditions):
        if not any("hep a" in v or "hepatitis a" in v for v in received_lower):
            recommended.append({
                "vaccine": "Hepatitis A",
                "schedule": "2 dose series, 6 months apart",
                "rationale": "Hepatitis A prevention (high-risk condition/travel)",
            })

    return {
        "status": "generated",
        "patient_profile": {
            "age": age,
            "gender": gender,
            "conditions": conditions,
        },
        "already_received": vaccinations_received,
        "recommended_vaccinations": recommended,
        "total_recommended": len(recommended),
        "note": "Vaccine recommendations based on CDC/ACIP guidelines. Discuss with provider for personalized schedule.",
    }
