"""Critical Care Medicine-specific severity scoring and organ dysfunction tools."""


def calculate_severity_score(
    age: int,
    temperature: float,
    heart_rate: int,
    respiratory_rate: int,
    spo2: int,
    systolic_bp: int,
    gcs: int,
    urine_output_ml_per_hr: float = 50.0,
) -> dict:
    """Calculates a composite ICU severity score (NEWS2 + qSOFA combined approach).

    Args:
        age: Patient age in years.
        temperature: Body temperature in Fahrenheit.
        heart_rate: Heart rate in beats per minute.
        respiratory_rate: Respiratory rate in breaths per minute.
        spo2: Oxygen saturation percentage.
        systolic_bp: Systolic blood pressure in mmHg.
        gcs: Glasgow Coma Scale score (3–15).
        urine_output_ml_per_hr: Urine output in mL/hour (normal > 0.5 mL/kg/hr).

    Returns:
        dict: Severity score, risk level, immediate interventions, and level of care recommendation.
    """
    score = 0
    alerts = []

    # Temperature (convert F to C for scoring)
    temp_c = (temperature - 32) * 5 / 9
    if temp_c <= 35.0:
        score += 3
        alerts.append("Hypothermia (< 35°C)")
    elif temp_c <= 36.0:
        score += 1
    elif temp_c >= 39.1:
        score += 2
        alerts.append("High fever (> 39.1°C)")
    elif temp_c >= 38.1:
        score += 1
        alerts.append("Fever (38.1–39°C)")

    # Heart rate
    if heart_rate <= 40:
        score += 3
        alerts.append("CRITICAL: Severe bradycardia (≤ 40 bpm)")
    elif heart_rate <= 50:
        score += 1
    elif heart_rate >= 131:
        score += 3
        alerts.append("CRITICAL: Severe tachycardia (≥ 131 bpm)")
    elif heart_rate >= 111:
        score += 2
        alerts.append("Tachycardia (111–130 bpm)")
    elif heart_rate >= 91:
        score += 1

    # Respiratory rate
    if respiratory_rate <= 8:
        score += 3
        alerts.append("CRITICAL: Respiratory depression (≤ 8/min) — risk of respiratory arrest")
    elif respiratory_rate <= 11:
        score += 1
    elif respiratory_rate >= 25:
        score += 3
        alerts.append("CRITICAL: Severe tachypnea (≥ 25/min)")
    elif respiratory_rate >= 21:
        score += 2
        alerts.append("Tachypnea (21–24/min)")

    # SpO2
    if spo2 <= 91:
        score += 3
        alerts.append("CRITICAL: Severe hypoxemia (SpO2 ≤ 91%)")
    elif spo2 <= 93:
        score += 2
        alerts.append("Hypoxemia (SpO2 92–93%)")
    elif spo2 <= 95:
        score += 1

    # Systolic BP
    if systolic_bp <= 90:
        score += 3
        alerts.append("CRITICAL: Hypotension (SBP ≤ 90 mmHg) — shock concern")
    elif systolic_bp <= 100:
        score += 2
        alerts.append("Low blood pressure (SBP 91–100 mmHg)")
    elif systolic_bp <= 110:
        score += 1

    # GCS (consciousness)
    if gcs <= 8:
        score += 3
        alerts.append("CRITICAL: Severe altered consciousness (GCS ≤ 8) — airway at risk")
    elif gcs <= 11:
        score += 2
        alerts.append("Altered consciousness (GCS 9–11)")
    elif gcs <= 14:
        score += 1

    # Urine output (oliguria)
    if urine_output_ml_per_hr < 10:
        score += 3
        alerts.append("Anuria — acute kidney injury concern")
    elif urine_output_ml_per_hr < 25:
        score += 2
        alerts.append("Oliguria — renal perfusion compromised")

    # Age risk factor
    if age >= 80:
        score += 1

    # qSOFA criteria (sepsis screening)
    qsofa_score = sum([
        1 if respiratory_rate >= 22 else 0,
        1 if systolic_bp <= 100 else 0,
        1 if gcs < 15 else 0,
    ])

    # Risk classification
    if score >= 7:
        risk_level = "CRITICAL"
        care = "Immediate ICU admission"
        actions = ["Immediate physician response", "Airway assessment", "IV access ×2", "Resuscitation"]
    elif score >= 5:
        risk_level = "HIGH"
        care = "Urgent ICU or HDU (High Dependency Unit)"
        actions = ["Urgent physician review", "Continuous monitoring", "IV access", "Labs + imaging"]
    elif score >= 3:
        risk_level = "MODERATE"
        care = "Step-down unit / close ward monitoring"
        actions = ["Physician review within 1 hour", "Vital signs every 30 minutes"]
    else:
        risk_level = "LOW"
        care = "Standard ward care"
        actions = ["Routine monitoring", "Re-assess if deterioration"]

    return {
        "status": "calculated",
        "composite_severity_score": score,
        "risk_level": risk_level,
        "recommended_care_level": care,
        "qsofa_score": qsofa_score,
        "qsofa_positive": qsofa_score >= 2,
        "sepsis_concern": qsofa_score >= 2,
        "critical_alerts": alerts,
        "immediate_actions": actions,
        "vital_signs_assessed": {
            "temperature_f": temperature,
            "heart_rate_bpm": heart_rate,
            "respiratory_rate": respiratory_rate,
            "spo2_percent": spo2,
            "systolic_bp_mmhg": systolic_bp,
            "gcs": gcs,
            "urine_output_ml_per_hr": urine_output_ml_per_hr,
        },
    }


def organ_dysfunction_assessment(
    organs_affected: list[str],
    lab_results: dict,
) -> dict:
    """Assesses multi-organ dysfunction using SOFA-like scoring criteria.

    Args:
        organs_affected: List of organ systems with dysfunction
            (e.g., ['respiratory', 'renal', 'hepatic', 'cardiovascular', 'coagulation', 'neurological']).
        lab_results: Dict of relevant lab values (e.g., {'creatinine': 2.5, 'bilirubin': 4.0,
            'platelets': 80, 'pao2_fio2': 200, 'map': 60}).

    Returns:
        dict: SOFA-like score per organ system, total score, mortality estimate, and management recommendations.
    """
    sofa_components = {}
    total_sofa = 0
    organ_management = []

    # Respiratory: PaO2/FiO2 ratio
    pf_ratio = lab_results.get("pao2_fio2", 400)
    if pf_ratio < 100:
        sofa_components["respiratory"] = 4
        organ_management.append("Respiratory: ARDS — lung-protective ventilation (6 mL/kg IBW, PEEP), prone positioning")
    elif pf_ratio < 200:
        sofa_components["respiratory"] = 3
        organ_management.append("Respiratory: Severe hypoxemia — high-flow O2, consider intubation")
    elif pf_ratio < 300:
        sofa_components["respiratory"] = 2
        organ_management.append("Respiratory: Moderate hypoxemia — supplemental O2, CPAP/BiPAP")
    elif pf_ratio < 400:
        sofa_components["respiratory"] = 1
    else:
        sofa_components["respiratory"] = 0

    # Renal: Creatinine and urine output
    creatinine = lab_results.get("creatinine", 1.0)
    if creatinine >= 5.0:
        sofa_components["renal"] = 4
        organ_management.append("Renal: Severe AKI — consider CRRT (continuous renal replacement therapy)")
    elif creatinine >= 3.5:
        sofa_components["renal"] = 3
        organ_management.append("Renal: Significant AKI — nephrology consultation, avoid nephrotoxins")
    elif creatinine >= 2.0:
        sofa_components["renal"] = 2
    elif creatinine >= 1.2:
        sofa_components["renal"] = 1
    else:
        sofa_components["renal"] = 0

    # Hepatic: Bilirubin
    bilirubin = lab_results.get("bilirubin", 1.0)
    if bilirubin >= 12:
        sofa_components["hepatic"] = 4
        organ_management.append("Hepatic: Severe liver failure — hepatology consultation, avoid hepatotoxic drugs")
    elif bilirubin >= 6:
        sofa_components["hepatic"] = 3
    elif bilirubin >= 2:
        sofa_components["hepatic"] = 2
    elif bilirubin >= 1.2:
        sofa_components["hepatic"] = 1
    else:
        sofa_components["hepatic"] = 0

    # Coagulation: Platelets
    platelets = lab_results.get("platelets", 200)
    if platelets < 20:
        sofa_components["coagulation"] = 4
        organ_management.append("Coagulation: Severe thrombocytopenia — platelet transfusion, hematology consult")
    elif platelets < 50:
        sofa_components["coagulation"] = 3
    elif platelets < 100:
        sofa_components["coagulation"] = 2
    elif platelets < 150:
        sofa_components["coagulation"] = 1
    else:
        sofa_components["coagulation"] = 0

    # Cardiovascular: MAP
    map_value = lab_results.get("map", 75)
    if map_value < 70:
        dose_norepinephrine = lab_results.get("norepinephrine_dose", 0)
        if dose_norepinephrine >= 0.1:
            sofa_components["cardiovascular"] = 4
            organ_management.append("Cardiovascular: Refractory shock — high-dose vasopressors, consider hydrocortisone")
        else:
            sofa_components["cardiovascular"] = 3
            organ_management.append("Cardiovascular: Shock — vasopressors + fluid resuscitation")
    elif map_value < 75:
        sofa_components["cardiovascular"] = 2
        organ_management.append("Cardiovascular: Borderline MAP — monitor closely, consider vasopressors")
    else:
        sofa_components["cardiovascular"] = 0

    # Neurological: GCS
    gcs = lab_results.get("gcs", 15)
    if gcs <= 6:
        sofa_components["neurological"] = 4
        organ_management.append("Neurological: Severe encephalopathy — airway protection, neuroimaging, neurology consult")
    elif gcs <= 9:
        sofa_components["neurological"] = 3
    elif gcs <= 12:
        sofa_components["neurological"] = 2
    elif gcs <= 14:
        sofa_components["neurological"] = 1
    else:
        sofa_components["neurological"] = 0

    total_sofa = sum(sofa_components.values())

    # Mortality estimation
    if total_sofa < 6:
        mortality_estimate = "<10%"
    elif total_sofa < 10:
        mortality_estimate = "15–20%"
    elif total_sofa < 12:
        mortality_estimate = "40–50%"
    else:
        mortality_estimate = ">50%"

    dysfunction_count = len([v for v in sofa_components.values() if v >= 2])
    mods = dysfunction_count >= 2

    return {
        "status": "assessed",
        "total_sofa_score": total_sofa,
        "sofa_by_organ": sofa_components,
        "organs_in_significant_dysfunction": dysfunction_count,
        "multi_organ_dysfunction_syndrome": mods,
        "estimated_mortality": mortality_estimate,
        "organ_specific_management": organ_management,
        "general_icu_priorities": [
            "Daily spontaneous awakening and breathing trials",
            "Venous thromboembolism (DVT) prophylaxis",
            "Stress ulcer prophylaxis if ventilated or coagulopathic",
            "Head of bed elevation 30–45°",
            "Tight glycemic control (target 140–180 mg/dL)",
            "Early enteral nutrition",
        ],
    }
