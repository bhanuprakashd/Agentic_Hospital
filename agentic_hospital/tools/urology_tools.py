"""Urology-specific diagnostic and assessment tools."""


def kidney_stone_assessment(
    stone_size_mm: float,
    stone_location: str,
    symptoms: list[str],
    fever: bool,
    creatinine: float = None,
    bilateral_stones: bool = False,
    solitary_kidney: bool = False,
) -> dict:
    """Assesses kidney stone and determines management approach.

    Args:
        stone_size_mm: Stone diameter in millimeters.
        stone_location: Location ('kidney', 'proximal_ureter', 'mid_ureter', 'distal_ureter', 'bladder').
        symptoms: List of symptoms (e.g., ['flank_pain', 'hematuria', 'nausea']).
        fever: Whether patient has fever.
        creatinine: Serum creatinine in mg/dL (optional).
        bilateral_stones: Whether stones are bilateral.
        solitary_kidney: Whether patient has only one functional kidney.

    Returns:
        dict: Stone assessment with management recommendations.
    """
    urgency = "NON-EMERGENT"
    interventions = []
    stone_passage_probability = None

    # Spontaneous passage probability based on size and location
    if stone_size_mm <= 4:
        stone_passage_probability = "~80%"
        interventions.append("Medical expulsive therapy (tamsulosin) recommended")
        interventions.append("Expectant management with hydration and analgesia")
    elif stone_size_mm <= 6:
        stone_passage_probability = "~60%"
        interventions.append("Trial of medical expulsive therapy (tamsulosin)")
        interventions.append("Consider surgical intervention if no passage in 4-6 weeks")
    elif stone_size_mm <= 10:
        stone_passage_probability = "~20-30%"
        interventions.append("Unlikely to pass spontaneously")
        interventions.append("Ureteroscopy or shock wave lithotripsy (SWL) recommended")
    else:
        stone_passage_probability = "< 10%"
        interventions.append("Very unlikely to pass spontaneously")
        interventions.append("Surgical intervention required: Ureteroscopy or PCNL")

    # Emergency indicators
    emergency_reasons = []
    if fever:
        urgency = "EMERGENT"
        emergency_reasons.append("Fever with obstructing stone - concern for urosepsis")
        interventions.insert(0, "URGENT: Broad-spectrum antibiotics and decompression")
    if creatinine and creatinine > 2.0:
        urgency = "URGENT"
        emergency_reasons.append(f"Elevated creatinine ({creatinine} mg/dL) - obstruction affecting kidney function")
    if bilateral_stones or solitary_kidney:
        urgency = "URGENT" if urgency != "EMERGENT" else urgency
        emergency_reasons.append("Bilateral obstruction or solitary kidney - requires urgent decompression")

    # Location-specific management
    location_management = {
        "kidney": "Observation for asymptomatic; ESWL or ureteroscopy for symptomatic stones < 2cm; PCNL for stones > 2cm",
        "proximal_ureter": "ESWL or ureteroscopy depending on size and patient factors",
        "mid_ureter": "Ureteroscopy preferred over ESWL",
        "distal_ureter": "Medical expulsive therapy for < 5mm; ureteroscopy for larger stones",
        "bladder": "Cystolitholapaxy for symptomatic bladder stones",
    }

    # Indications for intervention
    intervention_indications = []
    if "severe_pain" in [s.lower() for s in symptoms] or "uncontrolled_pain" in [s.lower() for s in symptoms]:
        intervention_indications.append("Uncontrolled pain despite analgesia")
    if "infection" in [s.lower() for s in symptoms] or fever:
        intervention_indications.append("Infection/sepsis with obstruction")
    if creatinine and creatinine > 1.5:
        intervention_indications.append("Renal function impairment")
    if stone_size_mm > 10:
        intervention_indications.append("Large stone size")
    if stone_size_mm > 5 and stone_location in ["proximal_ureter", "mid_ureter"]:
        intervention_indications.append("Proximal/mid ureteral stone > 5mm")

    return {
        "status": "assessed",
        "stone_size_mm": stone_size_mm,
        "stone_location": stone_location,
        "urgency": urgency,
        "emergency_indicators": emergency_reasons if emergency_reasons else ["None"],
        "spontaneous_passage_probability": stone_passage_probability,
        "management_approach": location_management.get(stone_location, "Urology consultation"),
        "recommended_interventions": interventions,
        "intervention_indications": intervention_indications if intervention_indications else ["None identified"],
        "follow_up": "Repeat imaging in 2-4 weeks if conservative management; sooner if symptoms worsen",
        "special_considerations": {
            "bilateral_stones": bilateral_stones,
            "solitary_kidney": solitary_kidney,
            "infection_signs": fever,
        },
    }


def prostate_assessment(
    psa: float,
    age: int,
    digital_rectal_exam: str,
    family_history_prostate_cancer: bool,
    previous_biopsy: bool = False,
    urinary_symptoms: list[str] = None,
) -> dict:
    """Assesses prostate cancer risk and need for biopsy.

    Args:
        psa: PSA level in ng/mL.
        age: Patient age in years.
        digital_rectal_exam: DRE finding ('normal', 'enlarged', 'nodule', 'hard').
        family_history_prostate_cancer: Family history of prostate cancer.
        previous_biopsy: Whether patient has had previous prostate biopsy.
        urinary_symptoms: List of urinary symptoms (e.g., ['frequency', 'nocturia', 'weak_stream']).

    Returns:
        dict: Prostate cancer risk assessment with recommendations.
    """
    # Age-specific PSA thresholds
    age_thresholds = {
        40: 2.5,
        50: 3.5,
        60: 4.5,
        70: 6.5,
    }

    age_threshold = age_thresholds.get((age // 10) * 10, 4.0)

    # Risk calculation
    risk_factors = []
    risk_score = 0

    # PSA level
    if psa > 10:
        risk_score += 3
        risk_factors.append(f"PSA > 10 ng/mL ({psa}) - HIGH risk")
    elif psa > 4:
        risk_score += 2
        risk_factors.append(f"PSA > 4 ng/mL ({psa}) - elevated")
    elif psa > age_threshold:
        risk_score += 1
        risk_factors.append(f"PSA above age-specific threshold ({psa} > {age_threshold})")

    # DRE findings
    if digital_rectal_exam == "nodule":
        risk_score += 3
        risk_factors.append("Palpable nodule on DRE - concerning")
    elif digital_rectal_exam == "hard":
        risk_score += 4
        risk_factors.append("Hard prostate on DRE - very concerning")
    elif digital_rectal_exam == "enlarged":
        risk_factors.append("Enlarged prostate on DRE - consider BPH vs cancer")

    # Family history
    if family_history_prostate_cancer:
        risk_score += 1
        risk_factors.append("Family history of prostate cancer")

    # Age
    if age >= 70:
        risk_factors.append("Age ≥ 70 - screening individualized based on life expectancy")
    elif age >= 50:
        risk_factors.append(f"Age {age} - appropriate for screening discussion")

    # Risk stratification
    if risk_score >= 5 or digital_rectal_exam in ["nodule", "hard"]:
        biopsy_recommendation = "RECOMMENDED"
        biopsy_reason = "High-risk features present"
        follow_up = "Urology referral for prostate biopsy"
    elif risk_score >= 3:
        biopsy_recommendation = "CONSIDER"
        biopsy_reason = "Elevated risk factors"
        follow_up = "Urology consultation to discuss biopsy vs MRI"
    elif psa > age_threshold and not previous_biopsy:
        biopsy_recommendation = "DISCUSS"
        biopsy_reason = "Elevated PSA - shared decision-making recommended"
        follow_up = "Consider PSA repeat in 4-6 weeks; MRI if persistent elevation"
    else:
        biopsy_recommendation = "NOT INDICATED"
        biopsy_reason = "No concerning features"
        follow_up = "Routine PSA screening per age-appropriate guidelines"

    # BPH assessment if urinary symptoms
    bph_assessment = None
    if urinary_symptoms:
        bph_assessment = {
            "symptoms_present": urinary_symptoms,
            "assessment": "Lower urinary tract symptoms present - consider IPSS questionnaire",
            "treatment_options": ["Alpha-blockers (tamsulosin)", "5-alpha reductase inhibitors", "Surgery if refractory"],
        }

    return {
        "status": "assessed",
        "psa": f"{psa} ng/mL",
        "age_specific_threshold": f"{age_threshold} ng/mL",
        "digital_rectal_exam": digital_rectal_exam,
        "risk_score": risk_score,
        "risk_factors": risk_factors if risk_factors else ["No elevated risk factors"],
        "biopsy_recommendation": biopsy_recommendation,
        "biopsy_reason": biopsy_reason,
        "previous_biopsy": "Yes" if previous_biopsy else "No",
        "follow_up": follow_up,
        "bph_assessment": bph_assessment,
        "screening_notes": [
            "PSA screening should be a shared decision between patient and physician",
            "Consider life expectancy and patient preferences",
            "False positives and overdiagnosis are concerns",
        ],
    }