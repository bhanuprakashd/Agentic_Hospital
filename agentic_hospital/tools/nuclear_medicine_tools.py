"""Nuclear Medicine-specific diagnostic and assessment tools."""


def pet_ct_oncology_assessment(
    primary_tumor_type: str,
    suv_max: float,
    lesion_location: str,
    findings: list[str],
    comparison_available: bool = False,
) -> dict:
    """Interprets PET/CT findings for oncologic evaluation.

    Args:
        primary_tumor_type: Type of primary cancer (e.g., 'lung', 'lymphoma', 'melanoma').
        suv_max: Maximum standardized uptake value (SUVmax).
        lesion_location: Location of the most avid lesion.
        findings: List of PET/CT findings.
        comparison_available: Whether comparison with prior study is available.

    Returns:
        dict: PET/CT interpretation with oncologic significance.
    """
    # SUV interpretation varies by tumor type
    tumor_suv_thresholds = {
        "lung": {"likely_malignant": 2.5, "highly_suspicious": 5.0},
        "lymphoma": {"likely_malignant": 3.0, "highly_suspicious": 10.0},
        "melanoma": {"likely_malignant": 2.5, "highly_suspicious": 5.0},
        "colorectal": {"likely_malignant": 3.0, "highly_suspicious": 5.0},
        "esophageal": {"likely_malignant": 3.0, "highly_suspicious": 6.0},
        "head_neck": {"likely_malignant": 3.0, "highly_suspicious": 5.0},
    }

    thresholds = tumor_suv_thresholds.get(primary_tumor_type.lower(), {"likely_malignant": 2.5, "highly_suspicious": 4.0})

    # Determine metabolic activity level
    if suv_max >= thresholds["highly_suspicious"]:
        activity_level = "HIGHLY SUSPICIOUS"
        metabolic_description = f"SUVmax {suv_max} is highly concerning for malignancy"
    elif suv_max >= thresholds["likely_malignant"]:
        activity_level = "SUSPICIOUS"
        metabolic_description = f"SUVmax {suv_max} is suspicious for malignancy"
    elif suv_max > 1.5:
        activity_level = "MILDLY INCREASED"
        metabolic_description = f"SUVmax {suv_max} shows mild FDG uptake - correlation needed"
    else:
        activity_level = "NOT SIGNIFICANTLY INCREASED"
        metabolic_description = f"SUVmax {suv_max} is not significantly above background"

    # Differential considerations for increased uptake
    differential = ["Malignancy", "Inflammation/infection", "Granulomatous disease", "Brown fat (if in neck/mediastinum)"]

    if activity_level in ["SUSPICIOUS", "HIGHLY SUSPICIOUS"]:
        recommendations = [
            f"Findings concerning for {primary_tumor_type} malignancy",
            "Correlation with CT morphology recommended",
            "Consider biopsy if lesion is accessible",
            "If staging: assess for metastatic disease",
        ]
        if comparison_available:
            recommendations.append("Compare with prior study to assess treatment response")
    else:
        recommendations = [
            "Low-level FDG uptake - correlation with clinical context",
            "Consider CT or MRI for further characterization",
            "Follow-up imaging if clinically indicated",
        ]

    # TNM staging implications (simplified)
    staging_notes = []
    if "lymph node" in lesion_location.lower():
        staging_notes.append("Lymph node involvement may affect N staging")
    if "liver" in lesion_location.lower() or "bone" in lesion_location.lower() or "brain" in lesion_location.lower():
        staging_notes.append("Distant metastasis - M1 disease")
    if "lung" in lesion_location.lower() and primary_tumor_type.lower() != "lung":
        staging_notes.append("Consider lung metastasis vs primary lung malignancy")

    return {
        "status": "interpreted",
        "primary_tumor_type": primary_tumor_type,
        "suv_max": suv_max,
        "activity_level": activity_level,
        "metabolic_description": metabolic_description,
        "lesion_location": lesion_location,
        "findings": findings,
        "differential_diagnosis": differential,
        "recommendations": recommendations,
        "staging_implications": staging_notes if staging_notes else ["Primary lesion without obvious distant metastasis on this study"],
        "comparison_available": comparison_available,
        "response_assessment": "Comparison with prior study recommended for treatment response" if not comparison_available else "Compare SUVmax change with prior study",
    }


def thyroid_scan_interpretation(
    nodule_characteristics: str,
    uptake_percentage: float,
    homogeneity: str,
    thyroid_volume_grams: float = None,
    tsh: float = None,
) -> dict:
    """Interprets thyroid scan findings.

    Args:
        nodule_characteristics: Nodule appearance ('hot', 'warm', 'cold', 'none').
        uptake_percentage: 24-hour radioactive iodine uptake percentage (normal 10-30%).
        homogeneity: Gland homogeneity ('homogeneous', 'heterogeneous', 'focal_defect').
        thyroid_volume_grams: Thyroid volume in grams (normal 10-20g).
        tsh: TSH level in mIU/L (optional).

    Returns:
        dict: Thyroid scan interpretation with clinical recommendations.
    """
    findings = []
    diagnosis = []
    recommendations = []

    # Uptake interpretation
    if uptake_percentage > 30:
        uptake_status = "ELEVATED"
        findings.append(f"Uptake {uptake_percentage}% - elevated (hyperfunctioning)")
        if tsh and tsh < 0.1:
            diagnosis.append("Hyperthyroidism (Graves' disease, toxic nodule, or toxic multinodular goiter)")
        else:
            diagnosis.append("Hyperfunctioning thyroid - correlate with TSH")
    elif uptake_percentage < 5:
        uptake_status = "LOW"
        findings.append(f"Uptake {uptake_percentage}% - low (hypofunctioning)")
        diagnosis.append("Thyroiditis (subacute, silent, or postpartum)")
        diagnosis.append("Exogenous thyroid hormone intake")
        diagnosis.append("Iodine excess")
    else:
        uptake_status = "NORMAL"
        findings.append(f"Uptake {uptake_percentage}% - within normal range")

    # Nodule characteristics
    if nodule_characteristics == "hot":
        findings.append("Hot nodule - autonomously functioning")
        diagnosis.append("Functioning thyroid nodule (toxic adenoma if hyperthyroid)")
        recommendations.append("Hot nodules are rarely malignant - low risk")
        recommendations.append("If hyperthyroid: consider radioiodine ablation or surgery")
    elif nodule_characteristics == "cold":
        findings.append("Cold nodule - non-functioning")
        diagnosis.append("Non-functioning thyroid nodule")
        recommendations.append("Cold nodules have ~5-15% malignancy risk")
        recommendations.append("Ultrasound-guided FNA recommended if nodule > 1cm")
    elif nodule_characteristics == "warm":
        findings.append("Warm nodule - intermediate function")
        recommendations.append("Ultrasound characterization recommended")
        recommendations.append("FNA if ultrasound features are suspicious")
    elif nodule_characteristics == "none":
        findings.append("No discrete nodules identified")

    # Homogeneity
    if homogeneity == "heterogeneous":
        findings.append("Heterogeneous uptake pattern")
        diagnosis.append("Multinodular goiter")
        diagnosis.append("Hashimoto's thyroiditis")
    elif homogeneity == "focal_defect":
        findings.append("Focal defect in uptake")
        diagnosis.append("Thyroid nodule")
        diagnosis.append("Thyroid cyst")
        diagnosis.append("Thyroiditis")

    # Thyroid volume
    if thyroid_volume_grams:
        if thyroid_volume_grams > 25:
            findings.append(f"Goiter (thyroid volume {thyroid_volume_grams}g)")
            if thyroid_volume_grams > 50:
                recommendations.append("Large goiter - assess for compressive symptoms")
                recommendations.append("Consider surgery if symptomatic")

    # TSH correlation
    if tsh is not None:
        if tsh < 0.1:
            recommendations.append("Low TSH confirms hyperthyroidism - correlates with elevated uptake")
        elif tsh > 4.0:
            recommendations.append("Elevated TSH suggests hypothyroidism - consider Hashimoto's thyroiditis")

    return {
        "status": "interpreted",
        "uptake_percentage": uptake_percentage,
        "uptake_status": uptake_status,
        "nodule_characteristics": nodule_characteristics,
        "homogeneity": homogeneity,
        "thyroid_volume_grams": thyroid_volume_grams,
        "findings": findings,
        "diagnostic_considerations": diagnosis,
        "recommendations": recommendations if recommendations else ["Clinical correlation and follow-up as indicated"],
        "tsh": tsh,
    }