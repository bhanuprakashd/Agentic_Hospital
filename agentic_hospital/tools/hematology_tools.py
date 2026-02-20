"""Hematology-specific diagnostic and assessment tools."""


def anemia_classification(
    hemoglobin: float,
    mcv: float,
    rdw: float,
    reticulocyte_count: float,
    iron: float = None,
    ferritin: float = None,
    b12: float = None,
    folate: float = None,
    gender: str = "female",
) -> dict:
    """Classifies anemia based on laboratory parameters.

    Args:
        hemoglobin: Hemoglobin level in g/dL (normal: male 13.5-17.5, female 12-16).
        mcv: Mean corpuscular volume in fL (normal: 80-100).
        rdw: Red cell distribution width % (normal: 11.5-14.5).
        reticulocyte_count: Reticulocyte count % (normal: 0.5-2.5).
        iron: Serum iron in mcg/dL (optional, normal: 60-170).
        ferritin: Serum ferritin in ng/mL (optional, normal: 20-300).
        b12: Vitamin B12 in pg/mL (optional, normal: 200-900).
        folate: Folate in ng/mL (optional, normal: 3-20).
        gender: Patient gender ('male' or 'female').

    Returns:
        dict: Anemia classification with likely causes and workup recommendations.
    """
    # Determine if anemic
    if gender.lower() == "male":
        anemic = hemoglobin < 13.5
        severity = "Severe" if hemoglobin < 8 else "Moderate" if hemoglobin < 11 else "Mild" if hemoglobin < 13.5 else "Normal"
    else:
        anemic = hemoglobin < 12.0
        severity = "Severe" if hemoglobin < 8 else "Moderate" if hemoglobin < 10 else "Mild" if hemoglobin < 12.0 else "Normal"

    if not anemic:
        return {
            "status": "no_anemia",
            "hemoglobin": f"{hemoglobin} g/dL",
            "interpretation": "Hemoglobin within normal range",
        }

    # MCV classification
    if mcv < 80:
        mcv_class = "MICROCYTIC"
        causes = ["Iron deficiency anemia", "Thalassemia", "Anemia of chronic disease", "Sideroblastic anemia"]
    elif mcv > 100:
        mcv_class = "MACROCYTIC"
        causes = ["Vitamin B12 deficiency", "Folate deficiency", "Liver disease", "Hypothyroidism", "Medications (methotrexate, hydroxyurea)", "Myelodysplastic syndrome"]
    else:
        mcv_class = "NORMOCYTIC"
        causes = ["Anemia of chronic disease", "Acute blood loss", "Hemolytic anemia", "Renal failure", "Mixed deficiency", "Bone marrow disorder"]

    # Reticulocyte response
    retic_adequate = reticulocyte_count > 2.0

    # RDW interpretation
    rdw_elevated = rdw > 14.5

    # Specific deficiencies
    deficiencies = []
    if iron is not None and iron < 60:
        deficiencies.append("Low iron")
    if ferritin is not None and ferritin < 30:
        deficiencies.append("Low ferritin (iron deficiency)")
    if b12 is not None and b12 < 200:
        deficiencies.append("Vitamin B12 deficiency")
    if folate is not None and folate < 3:
        deficiencies.append("Folate deficiency")

    # Differential diagnosis refinement
    differential = []
    if mcv_class == "MICROCYTIC":
        if ferritin is not None and ferritin < 30:
            differential.append("Iron deficiency anemia (most likely)")
        elif ferritin is not None and ferritin > 100:
            differential.append("Anemia of chronic disease")
            differential.append("Thalassemia trait (consider hemoglobin electrophoresis)")
        else:
            differential.extend(causes[:3])
    elif mcv_class == "MACROCYTIC":
        if b12 is not None and b12 < 200:
            differential.append("Vitamin B12 deficiency (confirmed)")
        elif folate is not None and folate < 3:
            differential.append("Folate deficiency (confirmed)")
        else:
            differential.extend(causes[:3])
    else:  # Normocytic
        if retic_adequate:
            differential.append("Hemolytic anemia or acute blood loss")
        else:
            differential.append("Anemia of chronic disease")
            differential.append("Renal failure")
            differential.append("Bone marrow disorder")

    # Workup recommendations
    workup = []
    if mcv_class == "MICROCYTIC" and ferritin is None:
        workup.append("Check serum iron, ferritin, TIBC")
        workup.append("Consider hemoglobin electrophoresis if thalassemia suspected")
    if mcv_class == "MACROCYTIC" and b12 is None:
        workup.append("Check vitamin B12 and folate levels")
        workup.append("Check TSH for hypothyroidism")
    if mcv_class == "NORMOCYTIC" and not retic_adequate:
        workup.append("Check renal function (BMP)")
        workup.append("Review peripheral smear")
        workup.append("Consider hematology referral for bone marrow evaluation")

    return {
        "status": "classified",
        "hemoglobin": f"{hemoglobin} g/dL",
        "anemia_severity": severity,
        "mcv_classification": mcv_class,
        "mcv": f"{mcv} fL",
        "rdw": f"{rdw}%",
        "rdw_interpretation": "Elevated (heterogeneous)" if rdw_elevated else "Normal (homogeneous)",
        "reticulocyte_count": f"{reticulocyte_count}%",
        "reticulocyte_response": "Adequate" if retic_adequate else "Inadequate",
        "potential_deficiencies": deficiencies if deficiencies else "None identified",
        "differential_diagnosis": differential,
        "workup_recommendations": workup,
    }


def dvt_risk_assessment(
    age: int,
    surgery_recent: bool,
    immobility: bool,
    cancer: bool,
    previous_dvt_pe: bool,
    pregnancy: bool,
    estrogen_therapy: bool,
    leg_swelling: bool,
    leg_pain: bool,
    positive_d_dimer: bool = None,
) -> dict:
    """Assesses DVT risk using Wells criteria and recommends workup.

    Args:
        age: Patient age in years.
        surgery_recent: Surgery or major trauma within 4 weeks.
        immobility: Bedridden ≥ 3 days or long-distance travel recently.
        cancer: Active cancer or treatment within 6 months.
        previous_dvt_pe: History of DVT or pulmonary embolism.
        pregnancy: Currently pregnant or up to 6 weeks postpartum.
        estrogen_therapy: On oral contraceptives or hormone replacement.
        leg_swelling: Calf swelling > 3 cm compared to asymptomatic side.
        leg_pain: Localized tenderness along deep venous system.
        positive_d_dimer: D-dimer test result if done (True/False/None).

    Returns:
        dict: DVT risk assessment with Wells score and management recommendations.
    """
    wells_score = 0
    clinical_features = []

    # Wells criteria scoring
    if cancer:
        wells_score += 1
        clinical_features.append("Active cancer (+1)")
    if previous_dvt_pe:
        wells_score += 1.5
        clinical_features.append("Previous DVT/PE (+1.5)")
    if surgery_recent or immobility:
        wells_score += 1.5
        clinical_features.append("Recent surgery/immobilization (+1.5)")
    if leg_swelling:
        wells_score += 1
        clinical_features.append("Calf swelling > 3 cm (+1)")
    if leg_pain:
        wells_score += 1
        clinical_features.append("Localized tenderness (+1)")
    if pregnancy or estrogen_therapy:
        wells_score += 1
        clinical_features.append("Pregnancy/estrogen therapy (+1)")

    # Age adjustment (some modified Wells criteria)
    if age >= 65:
        wells_score += 0.5

    # Pre-test probability
    if wells_score >= 2:
        probability = "HIGH"
        pre_test_prob = "50-75%"
    elif wells_score >= 1:
        probability = "MODERATE"
        pre_test_prob = "17-50%"
    else:
        probability = "LOW"
        pre_test_prob = "5-10%"

    # Management recommendations
    if probability == "HIGH":
        management = [
            "Urgent compression ultrasound (duplex) of lower extremity",
            "Consider starting anticoagulation empirically if delay in imaging",
            "D-dimer not needed - proceed directly to imaging",
        ]
        imaging_urgent = True
    elif probability == "MODERATE":
        if positive_d_dimer is True:
            management = [
                "Compression ultrasound (duplex) of lower extremity",
                "D-dimer positive - further workup warranted",
            ]
            imaging_urgent = True
        elif positive_d_dimer is False:
            management = [
                "D-dimer negative - DVT unlikely, consider alternative diagnoses",
                "Repeat evaluation if symptoms persist or worsen",
            ]
            imaging_urgent = False
        else:
            management = [
                "Check D-dimer",
                "If D-dimer positive, proceed to compression ultrasound",
            ]
            imaging_urgent = False
    else:  # LOW
        if positive_d_dimer is False:
            management = [
                "D-dimer negative - DVT effectively ruled out",
                "Consider alternative diagnoses",
            ]
            imaging_urgent = False
        elif positive_d_dimer is True:
            management = [
                "Compression ultrasound of lower extremity",
            ]
            imaging_urgent = False
        else:
            management = [
                "D-dimer recommended first",
                "If D-dimer negative, no imaging needed",
                "If D-dimer positive, compression ultrasound",
            ]
            imaging_urgent = False

    # PE risk reminder
    if wells_score >= 2:
        management.append("Assess for PE if any respiratory symptoms (CT angiography)")

    return {
        "status": "assessed",
        "wells_score": wells_score,
        "pre_test_probability": probability,
        "pre_test_probability_percentage": pre_test_prob,
        "clinical_features": clinical_features,
        "d_dimer_result": f"{'Positive' if positive_d_dimer else 'Negative' if positive_d_dimer is False else 'Not done'}",
        "imaging_urgent": imaging_urgent,
        "recommended_management": management,
        "anticoagulation_options_if_dvt": [
            "Low molecular weight heparin (enoxaparin) → transition to DOAC or warfarin",
            "Direct oral anticoagulant (rivaroxaban, apixaban) - can start immediately",
            "Duration: minimum 3 months for provoked DVT; extended for unprovoked or cancer-associated",
        ],
    }