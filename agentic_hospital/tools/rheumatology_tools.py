"""Rheumatology-specific diagnostic and assessment tools."""


def arthritis_assessment(
    joint_symptoms: list[str],
    morning_stiffness_minutes: int,
    symmetric_involvement: bool,
    small_joint_involvement: bool,
    rf_factor: bool = None,
    anti_ccp: bool = None,
    esr: int = None,
    crp: float = None,
    age: int = None,
) -> dict:
    """Assesses arthritis type using classification criteria and clinical features.

    Args:
        joint_symptoms: List of affected joints (e.g., ['hands', 'wrists', 'knees']).
        morning_stiffness_minutes: Duration of morning stiffness in minutes.
        symmetric_involvement: Whether joint involvement is symmetric.
        small_joint_involvement: Whether small joints (hands, feet) are involved.
        rf_factor: Rheumatoid factor result (True if positive).
        anti_ccp: Anti-CCP antibody result (True if positive).
        esr: Erythrocyte sedimentation rate in mm/hr (normal < 20-30).
        crp: C-reactive protein in mg/dL (normal < 1.0).
        age: Patient age in years.

    Returns:
        dict: Arthritis assessment with likely diagnosis and workup recommendations.
    """
    # Calculate rheumatoid arthritis probability (simplified ACR/EULAR criteria)
    ra_score = 0
    ra_features = []

    # Joint involvement
    if small_joint_involvement:
        ra_score += 2
        ra_features.append("Small joint involvement (hands/feet)")
    if symmetric_involvement:
        ra_score += 1
        ra_features.append("Symmetric joint involvement")

    # Serology
    if anti_ccp is True:
        ra_score += 3
        ra_features.append("Anti-CCP positive (high specificity for RA)")
    elif rf_factor is True:
        ra_score += 2
        ra_features.append("RF positive")

    # Acute phase reactants
    if esr and esr > 30:
        ra_score += 1
        ra_features.append(f"Elevated ESR ({esr} mm/hr)")
    if crp and crp > 1.0:
        ra_score += 1
        ra_features.append(f"Elevated CRP ({crp} mg/dL)")

    # Duration
    if morning_stiffness_minutes > 60:
        ra_score += 1
        ra_features.append(f"Morning stiffness > 1 hour ({morning_stiffness_minutes} min)")
    elif morning_stiffness_minutes > 30:
        ra_features.append(f"Morning stiffness {morning_stiffness_minutes} min")

    # Differential diagnosis
    differentials = []

    if ra_score >= 6:
        primary_diagnosis = "Rheumatoid Arthritis (probable)"
        differentials = ["Psoriatic arthritis", "SLE with arthritis", "Parvovirus arthritis"]
        confidence = "HIGH"
    elif ra_score >= 4:
        primary_diagnosis = "Rheumatoid Arthritis (possible)"
        differentials = ["Psoriatic arthritis", "Seronegative spondyloarthritis", "Early RA"]
        confidence = "MODERATE"
    elif "back" in [j.lower() for j in joint_symptoms] and age and age < 45:
        primary_diagnosis = "Seronegative Spondyloarthritis"
        differentials = ["Ankylosing spondylitis", "Psoriatic arthritis", "Reactive arthritis"]
        confidence = "MODERATE"
    elif morning_stiffness_minutes < 30 and age and age > 50:
        primary_diagnosis = "Osteoarthritis"
        differentials = ["Crystal arthritis (gout/pseudogout)", "Rheumatoid arthritis"]
        confidence = "MODERATE"
    elif not small_joint_involvement and morning_stiffness_minutes < 30:
        primary_diagnosis = "Osteoarthritis or Crystal Arthritis"
        differentials = ["Gout", "Pseudogout (CPPD)", "Osteoarthritis"]
        confidence = "LOW"
    else:
        primary_diagnosis = "Inflammatory Arthritis - type undifferentiated"
        differentials = ["Rheumatoid arthritis", "Psoriatic arthritis", "SLE", "Viral arthritis"]
        confidence = "LOW"

    # Workup recommendations
    workup = []

    if anti_ccp is None:
        workup.append("Anti-CCP antibody (more specific than RF for RA)")
    if rf_factor is None:
        workup.append("Rheumatoid factor (RF)")
    if esr is None:
        workup.append("ESR (sedimentation rate)")
    if crp is None:
        workup.append("CRP (C-reactive protein)")

    workup.extend([
        "X-rays of affected joints (hands, feet if RA suspected)",
        "Consider ultrasound for synovitis detection",
    ])

    if "spondyloarthritis" in primary_diagnosis.lower() or "back" in [j.lower() for j in joint_symptoms]:
        workup.append("HLA-B27 testing")
        workup.append("Sacral X-rays or MRI spine")

    # Treatment considerations
    if "Rheumatoid" in primary_diagnosis:
        treatment = [
            "DMARD therapy indicated if RA confirmed",
            "Methotrexate is first-line DMARD",
            "Consider short-term NSAIDs or prednisone bridge",
            "Early treatment prevents joint damage",
        ]
    else:
        treatment = [
            "NSAIDs for symptom relief",
            "Further workup to clarify diagnosis",
            "Physical therapy for joint protection",
        ]

    return {
        "status": "assessed",
        "primary_diagnosis": primary_diagnosis,
        "diagnostic_confidence": confidence,
        "ra_probability_score": ra_score,
        "supporting_features": ra_features,
        "differential_diagnoses": differentials,
        "workup_recommendations": workup,
        "treatment_considerations": treatment,
        "clinical_features": {
            "joints_affected": joint_symptoms,
            "morning_stiffness_minutes": morning_stiffness_minutes,
            "symmetric": symmetric_involvement,
            "small_joints": small_joint_involvement,
        },
        "lab_results": {
            "RF": "Positive" if rf_factor else "Negative" if rf_factor is False else "Not done",
            "Anti-CCP": "Positive" if anti_ccp else "Negative" if anti_ccp is False else "Not done",
            "ESR": f"{esr} mm/hr" if esr else "Not done",
            "CRP": f"{crp} mg/dL" if crp else "Not done",
        },
    }


def lupus_activity_assessment(
    symptoms: list[str],
    complement_c3: float = None,
    complement_c4: float = None,
    anti_ds_dna: float = None,
    current_medications: list[str] = None,
) -> dict:
    """Assesses systemic lupus erythematosus (SLE) disease activity.

    Args:
        symptoms: List of current symptoms (e.g., ['rash', 'joint_pain', 'fatigue', 'proteinuria']).
        complement_c3: Complement C3 level (normal ~90-180 mg/dL).
        complement_c4: Complement C4 level (normal ~10-40 mg/dL).
        anti_ds_dna: Anti-dsDNA antibody titer (normal varies by lab).
        current_medications: List of current SLE medications.

    Returns:
        dict: SLE disease activity assessment with recommendations.
    """
    # Organ involvement assessment
    organ_involvement = {
        "constitutional": [],
        "mucocutaneous": [],
        "musculoskeletal": [],
        "renal": [],
        "neurological": [],
        "cardiovascular": [],
        "pulmonary": [],
        "hematological": [],
    }

    symptoms_lower = [s.lower() for s in symptoms]

    # Constitutional
    constitutional_symptoms = ["fever", "fatigue", "weight_loss", "malaise"]
    for s in constitutional_symptoms:
        if s in symptoms_lower:
            organ_involvement["constitutional"].append(s)

    # Mucocutaneous
    mucocutaneous_symptoms = ["rash", "malar_rash", "discoid_rash", "photosensitivity", "oral_ulcers", "alopecia"]
    for s in mucocutaneous_symptoms:
        if s in symptoms_lower:
            organ_involvement["mucocutaneous"].append(s)

    # Musculoskeletal
    musculoskeletal_symptoms = ["joint_pain", "arthritis", "myalgia", "muscle_pain", "joint_swelling"]
    for s in musculoskeletal_symptoms:
        if s in symptoms_lower:
            organ_involvement["musculoskeletal"].append(s)

    # Renal
    renal_symptoms = ["proteinuria", "hematuria", "renal_insufficiency", "edema", "hypertension_new"]
    for s in renal_symptoms:
        if s in symptoms_lower:
            organ_involvement["renal"].append(s)

    # Neurological
    neuro_symptoms = ["seizure", "psychosis", "headache_severe", "cognitive_dysfunction", "neuropathy"]
    for s in neuro_symptoms:
        if s in symptoms_lower:
            organ_involvement["neurological"].append(s)

    # Cardiovascular
    cardiac_symptoms = ["pericarditis", "chest_pain", "myocarditis", "valvular_disease"]
    for s in cardiac_symptoms:
        if s in symptoms_lower:
            organ_involvement["cardiovascular"].append(s)

    # Pulmonary
    pulmonary_symptoms = ["pleuritis", "pleural_effusion", "pneumonitis", "pulmonary_hypertension"]
    for s in pulmonary_symptoms:
        if s in symptoms_lower:
            organ_involvement["pulmonary"].append(s)

    # Hematological
    hematological_symptoms = ["anemia", "leukopenia", "thrombocytopenia", "hemolysis"]
    for s in hematological_symptoms:
        if s in symptoms_lower:
            organ_involvement["hematological"].append(s)

    # Count active organs
    active_organs = sum(1 for organ, sx in organ_involvement.items() if sx)

    # Lab activity markers
    lab_activity = []
    if complement_c3 is not None and complement_c3 < 80:
        lab_activity.append("Low C3 (consumption)")
    if complement_c4 is not None and complement_c4 < 10:
        lab_activity.append("Low C4 (consumption)")
    if anti_ds_dna is not None and anti_ds_dna > 100:
        lab_activity.append("Elevated anti-dsDNA (active disease marker)")

    # Activity level determination
    severe_organs = ["renal", "neurological", "cardiovascular", "pulmonary"]
    has_severe_involvement = any(organ_involvement[organ] for organ in severe_organs)

    if has_severe_involvement or active_organs >= 4:
        activity_level = "HIGH"
        recommendation = "Consider immunosuppressive therapy escalation (cyclophosphamide, mycophenolate, or rituximab)"
        urgency = "URGENT rheumatology follow-up"
    elif active_organs >= 2 or lab_activity:
        activity_level = "MODERATE"
        recommendation = "May require adjustment of maintenance therapy"
        urgency = "Schedule rheumatology follow-up within 2-4 weeks"
    else:
        activity_level = "LOW/QUIESCENT"
        recommendation = "Continue current maintenance therapy"
        urgency = "Routine follow-up"

    # Treatment considerations
    treatment_notes = []
    if current_medications:
        current_lower = [m.lower() for m in current_medications]
        if "prednisone" in str(current_lower) or "steroid" in str(current_lower):
            treatment_notes.append("On corticosteroids - taper goal if disease controlled")
        if "hydroxychloroquine" in str(current_lower):
            treatment_notes.append("Hydroxychloroquine is appropriate for all SLE patients")
        if activity_level == "HIGH" and "mycophenolate" not in str(current_lower) and "cyclophosphamide" not in str(current_lower):
            treatment_notes.append("Consider adding immunosuppressive agent for severe disease")
    else:
        treatment_notes.append("Ensure hydroxychloroquine is in regimen if no contraindications")

    return {
        "status": "assessed",
        "disease_activity": activity_level,
        "active_organ_systems": {k: v for k, v in organ_involvement.items() if v},
        "active_organ_count": active_organs,
        "lab_activity_markers": lab_activity if lab_activity else ["No active lab markers"],
        "urgency": urgency,
        "treatment_recommendation": recommendation,
        "treatment_notes": treatment_notes,
        "monitoring": [
            "Regular CBC, CMP, urinalysis",
            "Complement levels (C3, C4) every 3-6 months",
            "Anti-dsDNA with disease flares",
            "Urine protein/creatinine ratio if renal involvement",
            "Bone density if on chronic steroids",
        ],
        "symptoms_reported": symptoms,
    }