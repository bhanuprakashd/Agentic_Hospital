"""Thoracic Surgery-specific assessment tools for pulmonary and pleural disease."""


def pulmonary_function_surgical_risk(fev1_percent_predicted: float,
                                     dlco_percent_predicted: float,
                                     planned_resection: str,
                                     fev1_absolute_liters: float,
                                     exercise_capacity_mets: float) -> dict:
    """Assesses pulmonary function and surgical risk for thoracic resection.

    Uses BTS/ESTS guidelines for pre-operative pulmonary risk stratification.
    Calculates predicted post-operative (ppo) lung function.

    Args:
        fev1_percent_predicted: Pre-operative FEV1 as % of predicted normal.
        dlco_percent_predicted: Pre-operative DLCO (diffusing capacity) as % of predicted.
        planned_resection: Surgical extent: 'pneumonectomy', 'bilobectomy', 'lobectomy',
                           'segmentectomy', or 'wedge_resection'.
        fev1_absolute_liters: Absolute FEV1 in liters.
        exercise_capacity_mets: Peak exercise capacity in metabolic equivalents (METs).
                                 (Walk 100m = ~3 METs; stair climb 2 flights = ~4 METs).

    Returns:
        dict: Predicted post-operative FEV1/DLCO, risk category, operative mortality
              estimate, and recommendations for fitness optimization.
    """
    # Segment-based ppo calculation (BTS guideline)
    # Total lung = 42 segments (right: 19, left: 23 — approximate)
    segments_removed = {
        "pneumonectomy": 19 if True else 23,  # right pneumonectomy most common
        "bilobectomy": 9,
        "lobectomy": 5,
        "segmentectomy": 2,
        "wedge_resection": 1,
    }.get(planned_resection.lower(), 5)

    total_segments = 42
    ppo_fraction = (total_segments - segments_removed) / total_segments
    ppo_fev1_percent = fev1_percent_predicted * ppo_fraction
    ppo_dlco_percent = dlco_percent_predicted * ppo_fraction
    ppo_fev1_liters = fev1_absolute_liters * ppo_fraction

    # Risk classification (BTS/ESTS thresholds)
    if ppo_fev1_percent >= 40 and ppo_dlco_percent >= 40 and exercise_capacity_mets >= 4:
        risk_category = "LOW"
        operative_mortality = "<2%"
        operability = "Fit for planned resection"
    elif ppo_fev1_percent >= 30 and ppo_dlco_percent >= 30 and exercise_capacity_mets >= 3:
        risk_category = "MODERATE"
        operative_mortality = "2–5%"
        operability = "Acceptable risk; consider smaller resection (lobectomy vs pneumonectomy)"
    elif ppo_fev1_percent >= 20 and ppo_dlco_percent >= 20 and exercise_capacity_mets >= 2:
        risk_category = "HIGH"
        operative_mortality = "5–15%"
        operability = "High risk; consider SBRT or ablation as alternatives; MDT discussion required"
    else:
        risk_category = "PROHIBITIVE"
        operative_mortality = ">15%"
        operability = "Not a surgical candidate; recommend SBRT/stereotactic ablation or best supportive care"

    # Fitness optimization
    optimization = []
    if fev1_percent_predicted < 70:
        optimization.append("Pulmonary rehabilitation for ≥4 weeks pre-operatively")
    if dlco_percent_predicted < 70:
        optimization.append("Optimize bronchodilation; treat reversible airway obstruction")
    if exercise_capacity_mets < 4:
        optimization.append("Supervised exercise training to improve cardiopulmonary fitness")
    optimization.extend([
        "Smoking cessation ≥8 weeks pre-operatively",
        "Optimize nutrition (BMI 20–30, albumin ≥3.5 g/dL)",
        "Incentive spirometry and breathing exercises",
        "Treat COPD exacerbation or active infection before scheduling surgery",
    ])

    return {
        "status": "assessed",
        "planned_resection": planned_resection,
        "preoperative_function": {
            "fev1_percent": fev1_percent_predicted,
            "fev1_liters": fev1_absolute_liters,
            "dlco_percent": dlco_percent_predicted,
            "exercise_capacity_mets": exercise_capacity_mets,
        },
        "predicted_post_operative": {
            "ppo_fev1_percent": round(ppo_fev1_percent, 1),
            "ppo_fev1_liters": round(ppo_fev1_liters, 2),
            "ppo_dlco_percent": round(ppo_dlco_percent, 1),
            "segments_to_be_removed": segments_removed,
        },
        "risk_category": risk_category,
        "estimated_operative_mortality": operative_mortality,
        "operability_assessment": operability,
        "critical_thresholds": {
            "ppo_fev1_low_risk": "≥40% predicted",
            "ppo_dlco_low_risk": "≥40% predicted",
            "absolute_contraindication": "ppo-FEV1 <30% OR ppo-DLCO <30% (relative contraindication for pneumonectomy)",
        },
        "fitness_optimization": optimization,
        "additional_tests_if_high_risk": [
            "Cardiopulmonary exercise testing (CPET) — VO₂max <10 mL/kg/min = prohibitive risk",
            "Quantitative V/Q scan for differential lung function (if pneumonectomy planned)",
            "Echocardiography for pulmonary hypertension assessment",
            "Right heart catheterization if PA pressure elevated",
        ],
        "guideline": "BTS Guidelines for Pre-Operative Assessment for Lung Resection (2001, updated) | ESTS Guidelines",
    }


def pleural_disease_assessment(symptom_onset: str, pleural_fluid_characteristics: dict,
                                imaging_findings: str, patient_history: list[str]) -> dict:
    """Assesses pleural disease and recommends diagnostic and therapeutic interventions.

    Covers pleural effusion, pneumothorax, empyema, malignant effusion, and mesothelioma.

    Args:
        symptom_onset: 'acute' (<72 hours), 'subacute' (days–weeks), or 'chronic' (>1 month).
        pleural_fluid_characteristics: Dict with available data: e.g.,
            {'appearance': 'straw_yellow', 'protein_g_dl': 4.2, 'ldh_iu_l': 320,
             'glucose_mg_dl': 85, 'ph': 7.2, 'serum_protein_g_dl': 7.0,
             'serum_ldh_iu_l': 200, 'white_cells_per_mm3': 1200, 'cell_type': 'lymphocytes'}.
        imaging_findings: Description of CXR/CT findings (e.g., 'right moderate effusion',
                          'bilateral small effusions', 'loculated effusion', 'pneumothorax 25%').
        patient_history: List of relevant history items (e.g., ['heart_failure', 'malignancy',
                         'tuberculosis', 'recent_pneumonia', 'asbestos_exposure', 'trauma']).

    Returns:
        dict: Light's criteria result (exudate vs. transudate), probable diagnosis,
              recommended interventions, and further workup.
    """
    # Light's criteria (exudate if ANY criterion met)
    lights_criteria = {}
    is_exudate = False
    fluid = pleural_fluid_characteristics

    if fluid.get("protein_g_dl") and fluid.get("serum_protein_g_dl"):
        ratio = fluid["protein_g_dl"] / fluid["serum_protein_g_dl"]
        lights_criteria["protein_ratio"] = round(ratio, 2)
        if ratio > 0.5:
            is_exudate = True
            lights_criteria["protein_criterion"] = "POSITIVE (>0.5)"
        else:
            lights_criteria["protein_criterion"] = "negative"

    if fluid.get("ldh_iu_l") and fluid.get("serum_ldh_iu_l"):
        ldh_ratio = fluid["ldh_iu_l"] / fluid["serum_ldh_iu_l"]
        lights_criteria["ldh_ratio"] = round(ldh_ratio, 2)
        if ldh_ratio > 0.6:
            is_exudate = True
            lights_criteria["ldh_ratio_criterion"] = "POSITIVE (>0.6)"
        else:
            lights_criteria["ldh_ratio_criterion"] = "negative"

        if fluid["ldh_iu_l"] > (2/3) * (fluid.get("serum_ldh_upper_limit", 200)):
            is_exudate = True
            lights_criteria["ldh_absolute_criterion"] = f"POSITIVE (>{round((2/3)*fluid.get('serum_ldh_upper_limit',200))} IU/L)"
        else:
            lights_criteria["ldh_absolute_criterion"] = "negative"

    fluid_type = "EXUDATE" if is_exudate else ("TRANSUDATE" if lights_criteria else "UNKNOWN (no fluid data)")

    # Differential diagnosis
    if fluid_type == "TRANSUDATE":
        probable_diagnoses = ["Heart failure (most common)", "Hepatic cirrhosis", "Nephrotic syndrome", "Hypoalbuminemia"]
    else:
        # Exudate differentials based on history and fluid
        probable_diagnoses = []
        if "malignancy" in patient_history:
            probable_diagnoses.append("Malignant pleural effusion")
        if "recent_pneumonia" in patient_history:
            probable_diagnoses.append("Parapneumonic effusion / Empyema")
        if "tuberculosis" in patient_history or fluid.get("cell_type") == "lymphocytes":
            probable_diagnoses.append("Tuberculous pleuritis")
        if "asbestos_exposure" in patient_history:
            probable_diagnoses.append("Malignant pleural mesothelioma")
        if "pulmonary_embolism" in patient_history:
            probable_diagnoses.append("PE-associated effusion")
        if "autoimmune" in patient_history:
            probable_diagnoses.append("Rheumatoid pleuritis / Lupus pleuritis")
        if not probable_diagnoses:
            probable_diagnoses = ["Parapneumonic", "Malignant", "TB pleuritis", "PE — further workup needed"]

    # pH-based management
    ph = fluid.get("ph")
    empyema_criteria = []
    if ph and ph < 7.2:
        empyema_criteria.append(f"Pleural pH <7.2 ({ph}) — chest tube drainage indicated")
    if fluid.get("glucose_mg_dl") and fluid["glucose_mg_dl"] < 60:
        empyema_criteria.append(f"Glucose <60 mg/dL ({fluid['glucose_mg_dl']}) — high risk of loculation")
    if fluid.get("ldh_iu_l") and fluid["ldh_iu_l"] > 1000:
        empyema_criteria.append(f"LDH >1000 IU/L ({fluid['ldh_iu_l']}) — frank empyema likely")

    # Pneumothorax sizing
    is_pneumothorax = "pneumothorax" in imaging_findings.lower()
    ptx_management = None
    if is_pneumothorax:
        ptx_management = {
            "BTS simple aspiration criteria": "First episode, small (<2 cm), asymptomatic → aspiration or observation",
            "Chest tube": "Large (≥2 cm), symptomatic, or secondary pneumothorax",
            "Tension": "EMERGENCY — immediate needle decompression 2nd ICS MCL, then chest tube",
            "Persistent air leak (>3–5 days)": "VATS pleurodesis / bullectomy",
        }

    return {
        "status": "assessed",
        "fluid_analysis": {
            "lights_criteria": lights_criteria,
            "fluid_type": fluid_type,
            "fluid_characteristics": fluid,
        },
        "probable_diagnoses": probable_diagnoses,
        "empyema_criteria_met": empyema_criteria,
        "pneumothorax_management": ptx_management,
        "intervention_recommendations": [
            "Diagnostic thoracentesis: cytology, cell count, protein, LDH, glucose, pH, culture",
            "CT-guided thoracentesis for loculated effusion",
            "Pleural biopsy (CT-guided or thoracoscopic) if malignancy/TB suspected",
            "Intrapleural fibrinolytics (alteplase + DNase) for loculated parapneumonic effusion",
            "Indwelling tunneled pleural catheter for recurrent malignant effusion",
            "VATS pleurodesis for definitive control",
        ] if fluid_type == "EXUDATE" else [
            "Treat underlying cause (heart failure, cirrhosis, hypoalbuminemia)",
            "Therapeutic thoracentesis if symptomatic",
            "Pleurodesis only after underlying cause optimized",
        ],
        "further_workup": [
            "CT Chest with contrast (if not done)",
            "Pleural fluid cytology (×3 samples increase sensitivity to ~87%)",
            "Pleural biopsy if lymphocytic exudate and TB/malignancy suspected",
            "PET/CT if malignant mesothelioma suspected",
            "ANA, RF, complement levels if autoimmune etiology",
        ],
        "symptom_onset": symptom_onset,
        "guideline": "BTS Guidelines for Investigation of Unilateral Pleural Effusion (2023) | Light's Criteria",
    }
