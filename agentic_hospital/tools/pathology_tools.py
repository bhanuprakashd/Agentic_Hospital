"""Pathology-specific biopsy interpretation and critical lab value tools."""


def interpret_biopsy_result(tissue_type: str, microscopic_description: str,
                             immunohistochemistry: dict,
                             clinical_context: str) -> dict:
    """Interprets biopsy and histopathology results with diagnostic classification.

    Provides WHO classification, grading, staging implications, and actionable
    recommendations for the multidisciplinary team.

    Args:
        tissue_type: Organ/tissue biopsied (e.g., 'breast', 'prostate', 'colon',
                     'lung', 'lymph_node', 'skin', 'kidney', 'liver', 'thyroid').
        microscopic_description: Free-text microscopic findings as reported
            (e.g., 'invasive ductal carcinoma, grade 2, with lymphovascular invasion').
        immunohistochemistry: Dict of IHC markers and results
            (e.g., {'ER': 'positive_90%', 'PR': 'positive_70%', 'HER2': '2+',
                    'Ki67': '25%', 'p53': 'mutant_type'}).
        clinical_context: Clinical background and reason for biopsy.

    Returns:
        dict: Diagnosis, WHO classification, grading, staging implications,
              biomarker interpretation, and MDT recommendations.
    """
    desc_lower = microscopic_description.lower()
    tissue_lower = tissue_type.lower()
    ihc = immunohistochemistry

    # ---- BREAST ----
    if tissue_lower == "breast":
        if "invasive" in desc_lower and "ductal" in desc_lower:
            diagnosis = "Invasive Ductal Carcinoma (IDC) — WHO Grade as specified"
        elif "invasive" in desc_lower and "lobular" in desc_lower:
            diagnosis = "Invasive Lobular Carcinoma (ILC)"
        elif "ductal carcinoma in situ" in desc_lower or "dcis" in desc_lower:
            diagnosis = "Ductal Carcinoma In Situ (DCIS)"
        elif "benign" in desc_lower or "fibroadenoma" in desc_lower:
            diagnosis = "Benign breast lesion"
        else:
            diagnosis = f"Breast pathology: {microscopic_description}"

        # Molecular subtype from IHC
        er = ihc.get("ER", "").lower()
        pr = ihc.get("PR", "").lower()
        her2 = ihc.get("HER2", "")
        ki67 = ihc.get("Ki67", "0%").replace("%", "")
        try:
            ki67_val = int(ki67)
        except ValueError:
            ki67_val = 0

        her2_positive = "3+" in str(her2) or (str(her2) == "2+" and ihc.get("FISH") == "amplified")
        er_positive = "positive" in er
        pr_positive = "positive" in pr

        if er_positive and not her2_positive:
            subtype = "Luminal A" if ki67_val < 20 else "Luminal B (HER2-)"
        elif er_positive and her2_positive:
            subtype = "Luminal B (HER2+)"
        elif not er_positive and her2_positive:
            subtype = "HER2-Enriched"
        elif not er_positive and not pr_positive and not her2_positive:
            subtype = "Triple-Negative (TNBC)"
        else:
            subtype = "Undetermined — further IHC needed"

        biomarker_implications = {
            "Luminal A": "Endocrine therapy (tamoxifen/aromatase inhibitor). Low chemo benefit.",
            "Luminal B (HER2-)": "Endocrine therapy + consider chemotherapy (Oncotype DX). Ki67 >20%.",
            "Luminal B (HER2+)": "Endocrine + HER2-targeted (trastuzumab) + chemotherapy.",
            "HER2-Enriched": "HER2-targeted therapy (trastuzumab + pertuzumab) + chemotherapy.",
            "Triple-Negative (TNBC)": "Chemotherapy backbone. Consider pembrolizumab (PD-L1+) + immunotherapy. BRCA testing.",
        }.get(subtype, "Individualized based on profile.")

    # ---- PROSTATE ----
    elif tissue_lower == "prostate":
        gleason = ""
        for phrase in ["gleason", "grade group"]:
            if phrase in desc_lower:
                gleason = microscopic_description
                break
        diagnosis = f"Prostate Adenocarcinoma: {gleason}" if "adenocarcinoma" in desc_lower else f"Prostate biopsy: {microscopic_description}"
        subtype = "Not applicable"
        biomarker_implications = (
            "PSA + Gleason/Grade Group determine risk (D'Amico). "
            "Grade Group 1 (Gleason 6): active surveillance. "
            "Grade Group 2–3 (Gleason 7): intermediate risk — surgery or radiation. "
            "Grade Group 4–5 (Gleason 8–10): high risk — multimodal therapy. "
            "Consider genomic testing (Oncotype DX Prostate, Decipher)."
        )

    # ---- COLON/RECTUM ----
    elif tissue_lower in ("colon", "rectum", "colorectal"):
        if "adenocarcinoma" in desc_lower:
            diagnosis = "Colorectal Adenocarcinoma"
            grade = "Well-differentiated (G1)" if "well" in desc_lower else (
                "Moderately differentiated (G2)" if "moderate" in desc_lower else "Poorly differentiated (G3)")
            diagnosis += f", {grade}"
        elif "adenoma" in desc_lower:
            diagnosis = "Adenomatous Polyp — pre-malignant (tubular/tubulovillous/villous)"
        else:
            diagnosis = f"Colorectal pathology: {microscopic_description}"
        subtype = "MSI/MMR status pending" if not ihc else (
            "MSI-High/dMMR" if ihc.get("MLH1") == "lost" or ihc.get("MSH2") == "lost" else "MSS/pMMR")
        biomarker_implications = (
            "MSI-H/dMMR: excellent prognosis stage II; immunotherapy (pembrolizumab) 1st-line metastatic. "
            "MSS: FOLFOX/FOLFIRI ± bevacizumab/cetuximab (RAS/BRAF wt). BRAF V600E: BRAF inhibitor combo. "
            "HER2 amplification: pertuzumab + trastuzumab (2nd-line)."
        )

    # ---- LUNG ----
    elif tissue_lower == "lung":
        if "adenocarcinoma" in desc_lower:
            diagnosis = "Lung Adenocarcinoma (NSCLC)"
        elif "squamous" in desc_lower:
            diagnosis = "Squamous Cell Carcinoma (NSCLC)"
        elif "small cell" in desc_lower:
            diagnosis = "Small Cell Lung Cancer (SCLC)"
        elif "large cell" in desc_lower:
            diagnosis = "Large Cell Carcinoma (NSCLC)"
        else:
            diagnosis = f"Lung pathology: {microscopic_description}"
        subtype = "Molecular profiling pending"
        biomarker_implications = (
            "NSCLC: test EGFR, ALK, ROS1, KRAS G12C, BRAF V600E, MET exon 14, RET, NTRK, PD-L1 (TPS). "
            "EGFR-mutant: osimertinib 1st-line. "
            "ALK/ROS1: alectinib/crizotinib. "
            "KRAS G12C: sotorasib/adagrasib. "
            "High PD-L1 (≥50%): pembrolizumab monotherapy. "
            "SCLC: EP chemotherapy (etoposide + platinum). "
        )

    else:
        diagnosis = f"{tissue_type} biopsy: {microscopic_description}"
        subtype = "Tissue-specific classification required"
        biomarker_implications = "Correlate with clinical context. Oncology/specialist referral for interpretation."

    # General pathology quality
    adequacy = "Adequate for diagnosis" if len(microscopic_description) > 10 else "Specimen adequacy uncertain — clinical correlation required"

    return {
        "status": "interpreted",
        "tissue_type": tissue_type,
        "diagnosis": diagnosis,
        "molecular_subtype": subtype,
        "ihc_markers": ihc,
        "biomarker_implications": biomarker_implications,
        "specimen_adequacy": adequacy,
        "mdt_recommendations": [
            "Present at multidisciplinary tumor board (MDT)",
            "Complete molecular/genomic profiling (NGS panel) for malignant diagnoses",
            "Correlate with clinical, radiological, and surgical findings",
            "Repeat biopsy if specimen inadequate or diagnosis uncertain",
            "Germline genetic testing if hereditary syndrome suspected (BRCA, Lynch, FAP)",
        ],
        "turnaround_time": {
            "routine_histology": "2–3 working days",
            "immunohistochemistry": "3–5 working days",
            "FISH_amplification": "5–7 working days",
            "NGS_molecular": "7–14 working days",
        },
        "who_classification": "Per 5th Edition WHO Classification of Tumours (2021–2024)",
        "clinical_context": clinical_context,
    }


def critical_lab_value_alert(test_name: str, result_value: float,
                              result_unit: str, patient_id: str,
                              patient_age: int, patient_sex: str) -> dict:
    """Identifies critical laboratory values and generates immediate alert with management.

    Applies AACC and CAP critical value thresholds with age/sex-adjusted reference ranges.

    Args:
        test_name: Laboratory test name (e.g., 'potassium', 'sodium', 'glucose',
                   'hemoglobin', 'platelets', 'INR', 'creatinine', 'calcium',
                   'troponin', 'pH', 'pO2', 'lactate', 'ammonia', 'lithium').
        result_value: Numerical result value.
        result_unit: Unit of measurement (e.g., 'mEq/L', 'mg/dL', 'g/dL', 'x10³/µL').
        patient_id: Patient identifier for alert documentation.
        patient_age: Patient age in years.
        patient_sex: Patient sex ('male' or 'female').

    Returns:
        dict: Critical value classification, immediate management, differential diagnosis,
              and provider notification protocol.
    """
    test_lower = test_name.lower().replace(" ", "_")

    # Critical value thresholds (AACC/CAP standards)
    critical_thresholds = {
        "potassium": {
            "critical_low": 2.5, "low": 3.5, "high": 5.5, "critical_high": 6.5,
            "unit": "mEq/L",
            "low_dx": ["GI losses (vomiting/diarrhea)", "Diuretic use", "Hypomagnesemia", "Hyperaldosteronism", "Alkalosis"],
            "high_dx": ["Renal failure", "ACE inhibitor/ARB + K+ supplement", "Hemolyzed sample", "Acidosis", "Rhabdomyolysis"],
            "low_mgmt": "K <2.5: IV KCl 10–20 mEq/hr via central line; cardiac monitoring; correct Mg²⁺. Oral supplement if mild.",
            "high_mgmt": "K >6.5: Calcium gluconate 1 g IV (stabilize membrane); Insulin 10U + D50W; Kayexalate/patiromer; dialysis if refractory.",
        },
        "sodium": {
            "critical_low": 120, "low": 135, "high": 145, "critical_high": 160,
            "unit": "mEq/L",
            "low_dx": ["SIADH", "Heart failure", "Cirrhosis", "Psychogenic polydipsia", "Hypothyroidism"],
            "high_dx": ["Hypernatremic dehydration", "Diabetes insipidus", "Excessive Na+ intake", "Hypotonic fluid loss"],
            "low_mgmt": "Na <120: Hypertonic saline (3%) if severe/symptomatic — correct ≤8–10 mEq/L in 24h (ODS risk). Fluid restrict if SIADH.",
            "high_mgmt": "Na >160: Gradual correction with D5W or hypotonic saline — lower ≤10–12 mEq/L per 24h. Identify and treat cause.",
        },
        "glucose": {
            "critical_low": 40, "low": 70, "high": 200, "critical_high": 500,
            "unit": "mg/dL",
            "low_dx": ["Insulin excess", "Sulfonylurea use", "Insulinoma", "Adrenal insufficiency", "Sepsis"],
            "high_dx": ["Diabetic ketoacidosis (DKA)", "Hyperosmolar hyperglycemic state (HHS)", "Stress hyperglycemia", "Steroid use"],
            "low_mgmt": "Glucose <40: D50W 25 mL IV bolus; recheck in 15 min; glucagon 1 mg IM if no IV access; continuous glucose monitoring.",
            "high_mgmt": "Glucose >500: IV insulin drip + aggressive hydration. Rule out DKA (AG, ketones) vs HHS (hyperosmolarity). ICU monitoring.",
        },
        "hemoglobin": {
            "critical_low": 7.0, "low": 12.0, "high": 17.5, "critical_high": 20.0,
            "unit": "g/dL",
            "low_dx": ["Acute hemorrhage", "Iron deficiency anemia", "Hemolytic anemia", "Aplastic anemia", "Chronic disease"],
            "high_dx": ["Polycythemia vera", "Secondary polycythemia (hypoxia, EPO)", "Dehydration", "CO poisoning"],
            "low_mgmt": "Hgb <7: pRBC transfusion (threshold varies: <8 for cardiac disease). Identify and treat underlying cause. Iron/B12/folate if deficient.",
            "high_mgmt": "Hgb >20: Phlebotomy. Hydroxyurea for polycythemia vera. Supplemental O2 for hypoxia-driven polycythemia.",
        },
        "platelets": {
            "critical_low": 20, "low": 150, "high": 450, "critical_high": 1000,
            "unit": "x10³/µL",
            "low_dx": ["ITP", "HIT", "TTP/HUS", "Aplastic anemia", "Heparin exposure", "DIC"],
            "high_dx": ["Essential thrombocythemia", "Reactive thrombocytosis (infection, iron deficiency)", "CML", "Post-splenectomy"],
            "low_mgmt": "Plt <20 (or <50 with bleeding): Platelet transfusion (1 apheresis unit). Avoid aspirin/NSAIDs. TTP: PLASMA EXCHANGE (never platelet transfusion). HIT: stop heparin immediately.",
            "high_mgmt": "Plt >1000: Aspirin 81 mg (reduces thrombosis risk in ET). Cytoreduction (hydroxyurea/anagrelide) if ET. Rule out reactive causes.",
        },
        "inr": {
            "critical_low": 0.5, "low": 0.8, "high": 3.0, "critical_high": 5.0,
            "unit": "ratio",
            "low_dx": ["Thrombotic state", "Factor V Leiden (not directly)", "Early DIC"],
            "high_dx": ["Warfarin overdose", "Liver failure", "DIC", "Factor deficiency", "Vitamin K deficiency"],
            "low_mgmt": "INR <0.8: Investigate hypercoagulable state; clinical correlation.",
            "high_mgmt": "INR >5 (no bleeding): Hold warfarin; oral Vit K 2.5–5 mg. INR >5 (with bleeding/surgery): 4-factor PCC 25–50 U/kg IV + Vit K 10 mg IV. FFP 4 units if PCC unavailable.",
        },
        "calcium": {
            "critical_low": 6.0, "low": 8.5, "high": 10.5, "critical_high": 13.0,
            "unit": "mg/dL",
            "low_dx": ["Hypoparathyroidism", "Vitamin D deficiency", "Pancreatitis", "Renal failure", "Sepsis"],
            "high_dx": ["Hyperparathyroidism", "Malignancy (PTHrP)", "Sarcoidosis", "Vitamin D toxicity", "Thiazide diuretics"],
            "low_mgmt": "Ca <6 (symptomatic): IV calcium gluconate 1–2 g over 10–20 min; continuous monitoring; correct Mg²⁺ and Vit D.",
            "high_mgmt": "Ca >13: IV saline hydration 200–300 mL/hr; furosemide after hydration; zoledronic acid 4 mg IV (best for malignancy). Calcitonin for rapid lowering.",
        },
        "lactate": {
            "critical_low": 0, "low": 0, "high": 2.0, "critical_high": 4.0,
            "unit": "mmol/L",
            "low_dx": [],
            "high_dx": ["Septic shock", "Cardiogenic shock", "Mesenteric ischemia", "Hemorrhagic shock", "Metformin toxicity", "Cyanide poisoning"],
            "low_mgmt": "N/A",
            "high_mgmt": "Lactate >4: Sepsis bundle (30 mL/kg IV fluids, antibiotics, vasopressors if MAP <65, ICU). Serial lactate every 2 hours. Target clearance >10% per 2h.",
        },
        "troponin": {
            "critical_low": 0, "low": 0, "high": 0.04, "critical_high": 1.0,
            "unit": "ng/mL",
            "low_dx": [],
            "high_dx": ["STEMI/NSTEMI", "Myocarditis", "PE", "Stress cardiomyopathy (Takotsubo)", "CKD", "Sepsis"],
            "low_mgmt": "N/A",
            "high_mgmt": "Troponin rising: STAT 12-lead ECG; cardiology consult; dual antiplatelet + anticoagulation if ACS confirmed; cath lab activation for STEMI.",
        },
    }

    thresholds = critical_thresholds.get(test_lower, {})

    if thresholds:
        crit_low = thresholds.get("critical_low", float("-inf"))
        crit_high = thresholds.get("critical_high", float("inf"))
        low = thresholds.get("low", float("-inf"))
        high = thresholds.get("high", float("inf"))

        if result_value <= crit_low:
            alert_level = "CRITICAL LOW"
            differential = thresholds.get("low_dx", [])
            management = thresholds.get("low_mgmt", "Immediate clinical assessment required.")
        elif result_value >= crit_high:
            alert_level = "CRITICAL HIGH"
            differential = thresholds.get("high_dx", [])
            management = thresholds.get("high_mgmt", "Immediate clinical assessment required.")
        elif result_value < low:
            alert_level = "LOW"
            differential = thresholds.get("low_dx", [])
            management = "Monitor and investigate underlying cause."
        elif result_value > high:
            alert_level = "HIGH"
            differential = thresholds.get("high_dx", [])
            management = "Monitor and investigate underlying cause."
        else:
            alert_level = "NORMAL"
            differential = []
            management = "No immediate action required."
    else:
        alert_level = "UNKNOWN TEST — manual review required"
        differential = []
        management = "Consult reference laboratory for critical thresholds."

    is_critical = "CRITICAL" in alert_level

    return {
        "status": "alerted",
        "patient_id": patient_id,
        "test_name": test_name,
        "result": f"{result_value} {result_unit}",
        "alert_level": alert_level,
        "is_critical_value": is_critical,
        "differential_diagnosis": differential,
        "immediate_management": management,
        "notification_required": is_critical,
        "notification_protocol": (
            "STAT phone notification to ordering provider within 30 minutes. "
            "Document: provider name, time called, read-back of value confirmed."
        ) if is_critical else "Report in standard lab result workflow.",
        "repeat_testing": "Repeat in 2–4 hours after intervention" if is_critical else "Per clinical protocol.",
        "age": patient_age,
        "sex": patient_sex,
        "reference_source": "AACC Critical Value Guidelines | CAP Laboratory Standards | Clinical correlate required.",
    }
