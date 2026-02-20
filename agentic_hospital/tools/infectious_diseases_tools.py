"""Infectious Diseases-specific diagnostic and assessment tools."""


def sepsis_screening(
    temperature: float,
    heart_rate: int,
    respiratory_rate: int,
    white_blood_cell_count: float,
    systolic_bp: int,
    altered_mentation: bool = False,
    source: str = "unknown",
    lactate: float = None,
) -> dict:
    """Screens for sepsis using qSOFA and SIRS criteria.

    Args:
        temperature: Body temperature in Fahrenheit.
        heart_rate: Heart rate in beats per minute.
        respiratory_rate: Respiratory rate in breaths per minute.
        white_blood_cell_count: WBC count in thousands/μL.
        systolic_bp: Systolic blood pressure in mmHg.
        altered_mentation: Whether patient has altered mental status.
        source: Suspected infection source (e.g., 'pneumonia', 'uti', 'abdominal').
        lactate: Serum lactate in mmol/L (optional).

    Returns:
        dict: Sepsis screening with qSOFA, SIRS scores, and management recommendations.
    """
    # SIRS criteria
    sirs_criteria = []
    sirs_score = 0

    if temperature > 100.4 or temperature < 96.8:
        sirs_criteria.append("Temperature abnormality")
        sirs_score += 1
    if heart_rate > 90:
        sirs_criteria.append("Heart rate > 90")
        sirs_score += 1
    if respiratory_rate > 20:
        sirs_criteria.append("Respiratory rate > 20")
        sirs_score += 1
    if white_blood_cell_count > 12 or white_blood_cell_count < 4:
        sirs_criteria.append("WBC abnormality")
        sirs_score += 1

    sirs_positive = sirs_score >= 2

    # qSOFA criteria
    qsofa_criteria = []
    qsofa_score = 0

    if respiratory_rate >= 22:
        qsofa_criteria.append("Respiratory rate ≥ 22")
        qsofa_score += 1
    if systolic_bp <= 100:
        qsofa_criteria.append("Systolic BP ≤ 100")
        qsofa_score += 1
    if altered_mentation:
        qsofa_criteria.append("Altered mental status")
        qsofa_score += 1

    qsofa_positive = qsofa_score >= 2

    # Determine severity
    if qsofa_positive:
        severity = "SEPSIS - HIGH RISK"
        recommendation = "URGENT: Initiate sepsis bundle immediately"
        actions = [
            "Blood cultures × 2 before antibiotics",
            "Broad-spectrum antibiotics within 1 hour",
            "Lactate level (if not done)",
            "30 mL/kg crystalloid if hypotensive or lactate ≥ 4",
            "Reassess volume status and tissue perfusion",
            "ICU consultation if not improving",
        ]
    elif sirs_positive:
        severity = "SEPSIS - MODERATE RISK"
        recommendation = "Monitor closely; consider sepsis pathway"
        actions = [
            "Obtain cultures",
            "Consider early antibiotics",
            "Monitor for deterioration",
            "Repeat vital signs in 1 hour",
        ]
    else:
        severity = "LOW RISK FOR SEPSIS"
        recommendation = "Continue monitoring"
        actions = [
            "Monitor for new symptoms",
            "Consider other diagnoses",
        ]

    # Lactate interpretation
    lactate_interpretation = None
    if lactate is not None:
        if lactate >= 4:
            lactate_interpretation = "SEVERE - Lactate ≥ 4 mmol/L indicates severe sepsis/septic shock"
            actions.insert(0, "LACTATE ELEVATED: Aggressive fluid resuscitation required")
        elif lactate >= 2:
            lactate_interpretation = "ELEVATED - Lactate 2-4 mmol/L suggests tissue hypoperfusion"
        else:
            lactate_interpretation = "Normal lactate"

    return {
        "status": "screened",
        "suspected_source": source,
        "severity": severity,
        "sirs_score": sirs_score,
        "sirs_criteria_met": sirs_criteria,
        "sirs_positive": sirs_positive,
        "qsofa_score": qsofa_score,
        "qsofa_criteria_met": qsofa_criteria,
        "qsofa_positive": qsofa_positive,
        "lactate": f"{lactate} mmol/L" if lactate else "Not available",
        "lactate_interpretation": lactate_interpretation,
        "recommendation": recommendation,
        "immediate_actions": actions,
        "vital_signs": {
            "temperature_f": temperature,
            "heart_rate_bpm": heart_rate,
            "respiratory_rate": respiratory_rate,
            "systolic_bp_mmhg": systolic_bp,
            "wbc_k_ul": white_blood_cell_count,
        },
    }


def antibiotic_selection_guide(
    infection_type: str,
    severity: str,
    allergies: list[str],
    renal_function: str = "normal",
    recent_hospitalization: bool = False,
) -> dict:
    """Provides empiric antibiotic selection guidance based on infection type.

    Args:
        infection_type: Type of infection (e.g., 'pneumonia_community', 'uti', 'cellulitis', 'meningitis').
        severity: Severity level ('mild', 'moderate', 'severe').
        allergies: List of drug allergies.
        renal_function: Renal function status ('normal', 'mild_impairment', 'moderate_impairment', 'severe_impairment', 'dialysis').
        recent_hospitalization: Hospitalization within past 90 days.

    Returns:
        dict: Empiric antibiotic recommendations with alternatives for allergies.
    """
    # Standard empiric regimens
    regimens = {
        "pneumonia_community": {
            "mild": {"first_line": "Amoxicillin 1g TID + Doxycycline 100mg BID", "alternative": "Azithromycin 500mg daily"},
            "moderate": {"first_line": "Amoxicillin-Clavulanate 875mg BID + Azithromycin 500mg daily", "alternative": "Levofloxacin 750mg daily"},
            "severe": {"first_line": "Ceftriaxone 2g IV daily + Azithromycin 500mg IV daily", "alternative": "Levofloxacin 750mg IV daily"},
        },
        "pneumonia_hospital": {
            "mild": {"first_line": "Ceftriaxone 2g IV daily", "alternative": "Ampicillin-Sulbactam 3g IV q6h"},
            "moderate": {"first_line": "Piperacillin-Tazobactam 4.5g IV q6h", "alternative": "Cefepime 2g IV q8h"},
            "severe": {"first_line": "Vancomycin IV + Piperacillin-Tazobactam 4.5g IV q6h", "alternative": "Vancomycin IV + Meropenem 1g IV q8h"},
        },
        "uti": {
            "mild": {"first_line": "Nitrofurantoin 100mg BID x 5 days", "alternative": "TMP-SMX DS BID x 3 days"},
            "moderate": {"first_line": "Ciprofloxacin 500mg BID x 7 days", "alternative": "Cefdinir 300mg BID x 7 days"},
            "severe": {"first_line": "Ceftriaxone 1g IV daily", "alternative": "Piperacillin-Tazobactam 3.375g IV q6h"},
        },
        "cellulitis": {
            "mild": {"first_line": "Cephalexin 500mg QID", "alternative": "Dicloxacillin 500mg QID"},
            "moderate": {"first_line": "Cefazolin 1g IV q8h", "alternative": "Clindamycin 600mg IV q8h"},
            "severe": {"first_line": "Vancomycin IV 15-20mg/kg q8-12h", "alternative": "Linezolid 600mg IV q12h"},
        },
        "meningitis": {
            "mild": {"first_line": "Ceftriaxone 2g IV q12h + Vancomycin IV", "alternative": "Meropenem 2g IV q8h"},
            "moderate": {"first_line": "Ceftriaxone 2g IV q12h + Vancomycin IV + Dexamethasone 0.15mg/kg q6h", "alternative": "Meropenem 2g IV q8h"},
            "severe": {"first_line": "Ceftriaxone 2g IV q12h + Vancomycin IV + Ampicillin 2g IV q4h + Dexamethasone", "alternative": "Meropenem 2g IV q8h + Vancomycin IV"},
        },
        "abdominal": {
            "mild": {"first_line": "Ciprofloxacin 500mg BID + Metronidazole 500mg TID", "alternative": "Amoxicillin-Clavulanate 875mg BID"},
            "moderate": {"first_line": "Ceftriaxone 2g IV daily + Metronidazole 500mg IV q8h", "alternative": "Ertapenem 1g IV daily"},
            "severe": {"first_line": "Piperacillin-Tazobactam 4.5g IV q6h", "alternative": "Meropenem 1g IV q8h"},
        },
        "sepsis_unknown": {
            "mild": {"first_line": "Ceftriaxone 2g IV daily", "alternative": "Levofloxacin 750mg IV daily"},
            "moderate": {"first_line": "Piperacillin-Tazobactam 4.5g IV q6h", "alternative": "Cefepime 2g IV q8h"},
            "severe": {"first_line": "Vancomycin IV + Piperacillin-Tazobactam 4.5g IV q6h", "alternative": "Vancomycin IV + Meropenem 1g IV q8h"},
        },
    }

    regimen = regimens.get(infection_type, regimens.get("sepsis_unknown", {})).get(severity, {})

    # Check for allergies and provide alternatives
    allergies_lower = [a.lower() for a in allergies]
    penicillin_allergy = any("penicillin" in a or "amoxicillin" in a or "ampicillin" in a for a in allergies_lower)
    cephalosporin_allergy = any("cephalosporin" in a or "cepha" in a for a in allergies_lower)
    sulfa_allergy = any("sulfa" in a or "sulfonamide" in a for a in allergies_lower)
    vancomycin_allergy = any("vancomycin" in a for a in allergies_lower)

    warnings = []
    if penicillin_allergy and "cef" in regimen.get("first_line", "").lower():
        warnings.append("CAUTION: First-line contains cephalosporin - may have cross-reactivity with penicillin allergy. Consider alternative.")
    if sulfa_allergy and "tmp-smx" in regimen.get("first_line", "").lower():
        warnings.append("CAUTION: TMP-SMX contains sulfa - use alternative.")

    # Renal dosing notes
    renal_notes = []
    if renal_function in ["moderate_impairment", "severe_impairment", "dialysis"]:
        renal_notes.append("Renal dose adjustment required for most antibiotics")
        renal_notes.append("Check specific dosing guidelines for renal impairment")
    if renal_function == "dialysis":
        renal_notes.append("Time antibiotics after dialysis when possible")
        renal_notes.append("Vancomycin: check trough levels, typically dose after dialysis")

    # Hospitalization risk
    if recent_hospitalization:
        warnings.append("Recent hospitalization: Consider broader coverage for healthcare-associated pathogens (MRSA, Pseudomonas)")

    return {
        "status": "recommendation_generated",
        "infection_type": infection_type,
        "severity": severity,
        "first_line": regimen.get("first_line", "Consult infectious diseases"),
        "alternative": regimen.get("alternative", "Consult infectious diseases"),
        "allergies_noted": allergies,
        "warnings": warnings,
        "renal_dosing_notes": renal_notes,
        "duration_guidance": {
            "pneumonia_community": "5-7 days",
            "uti": "3-7 days depending on severity",
            "cellulitis": "5-14 days",
            "meningitis": "7-21 days depending on organism",
            "sepsis": "7-10 days typically, reassess daily",
        }.get(infection_type, "Reassess duration based on clinical response"),
        "general_principles": [
            "Obtain cultures before antibiotics when possible",
            "Reassess at 48-72 hours for de-escalation",
            "Narrow spectrum once pathogen identified",
            "Switch from IV to PO when clinically stable",
        ],
    }