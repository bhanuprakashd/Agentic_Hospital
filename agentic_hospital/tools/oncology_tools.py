"""Oncology-specific diagnostic and assessment tools."""


def cancer_screening_recommendation(
    age: int,
    gender: str,
    family_history: list[str],
    smoking_history: bool,
    previous_cancer: bool,
) -> dict:
    """Provides age and risk-appropriate cancer screening recommendations.

    Args:
        age: Patient age in years.
        gender: Patient gender ('male' or 'female').
        family_history: List of cancers in first-degree relatives (e.g., ['breast cancer', 'colon cancer']).
        smoking_history: Whether patient has a history of smoking.
        previous_cancer: Whether patient has had cancer before.

    Returns:
        dict: Recommended screenings with timing and rationale.
    """
    screenings = []

    # Colorectal cancer screening
    if age >= 45 or any("colon" in h.lower() or "colorectal" in h.lower() for h in family_history):
        screenings.append({
            "test": "Colonoscopy",
            "frequency": "Every 10 years (or 5 years if family history)",
            "rationale": "Colorectal cancer screening" + (" - earlier due to family history" if any("colon" in h.lower() for h in family_history) else ""),
        })

    # Breast cancer screening
    if gender.lower() == "female":
        if age >= 40 or any("breast" in h.lower() for h in family_history):
            screenings.append({
                "test": "Mammography",
                "frequency": "Annually" if age >= 40 else "Discuss with provider",
                "rationale": "Breast cancer screening",
            })
        if any("breast" in h.lower() or "ovarian" in h.lower() for h in family_history):
            screenings.append({
                "test": "BRCA Genetic Testing",
                "frequency": "One-time",
                "rationale": "Genetic risk assessment due to family history",
            })

    # Cervical cancer screening
    if gender.lower() == "female" and 21 <= age <= 65:
        screenings.append({
            "test": "Pap Smear / HPV Co-testing",
            "frequency": "Every 3-5 years",
            "rationale": "Cervical cancer screening",
        })

    # Lung cancer screening
    if smoking_history and age >= 50:
        screenings.append({
            "test": "Low-Dose CT Chest",
            "frequency": "Annually",
            "rationale": "Lung cancer screening for smokers/former smokers age 50+",
        })

    # Prostate cancer screening
    if gender.lower() == "male" and age >= 50:
        screenings.append({
            "test": "PSA Blood Test + Digital Rectal Exam",
            "frequency": "Discuss with provider (shared decision-making)",
            "rationale": "Prostate cancer screening",
        })

    # Skin cancer screening
    if previous_cancer or any("melanoma" in h.lower() or "skin" in h.lower() for h in family_history):
        screenings.append({
            "test": "Full-Body Skin Examination",
            "frequency": "Annually",
            "rationale": "Skin cancer screening due to elevated risk",
        })

    # Liver cancer screening for high-risk
    if any("liver" in h.lower() or "hepatitis" in h.lower() for h in family_history):
        screenings.append({
            "test": "Liver Ultrasound + AFP",
            "frequency": "Every 6 months",
            "rationale": "Liver cancer surveillance due to risk factors",
        })

    if previous_cancer:
        screenings.append({
            "test": "Comprehensive Survivorship Follow-up",
            "frequency": "Per oncology guidelines for cancer type",
            "rationale": "Cancer survivorship monitoring",
        })

    return {
        "status": "recommendations_generated",
        "patient_profile": {
            "age": age,
            "gender": gender,
            "family_history": family_history,
            "smoking_history": smoking_history,
            "previous_cancer": previous_cancer,
        },
        "recommended_screenings": screenings,
        "general_advice": "Report any unexplained weight loss, persistent fatigue, unusual lumps, or changes in moles to your doctor promptly.",
    }


def staging_assessment(
    cancer_type: str,
    tumor_size_cm: float,
    lymph_nodes_involved: int,
    metastasis: bool,
    grade: str,
) -> dict:
    """Provides simplified TNM cancer staging assessment.

    Args:
        cancer_type: Type of cancer (e.g., 'breast', 'lung', 'colon').
        tumor_size_cm: Primary tumor size in centimeters.
        lymph_nodes_involved: Number of lymph nodes with cancer involvement.
        metastasis: Whether distant metastasis is present.
        grade: Tumor grade ('low', 'intermediate', 'high').

    Returns:
        dict: TNM staging with prognosis and treatment approach overview.
    """
    # T staging (simplified)
    if tumor_size_cm <= 2:
        t_stage = "T1"
    elif tumor_size_cm <= 5:
        t_stage = "T2"
    elif tumor_size_cm <= 7:
        t_stage = "T3"
    else:
        t_stage = "T4"

    # N staging
    if lymph_nodes_involved == 0:
        n_stage = "N0"
    elif lymph_nodes_involved <= 3:
        n_stage = "N1"
    elif lymph_nodes_involved <= 9:
        n_stage = "N2"
    else:
        n_stage = "N3"

    # M staging
    m_stage = "M1" if metastasis else "M0"

    # Overall stage
    if metastasis:
        overall_stage = "Stage IV"
        prognosis = "Advanced disease - focus on systemic therapy and quality of life"
    elif lymph_nodes_involved > 3:
        overall_stage = "Stage III"
        prognosis = "Locally advanced - multimodal treatment approach"
    elif lymph_nodes_involved > 0:
        overall_stage = "Stage II"
        prognosis = "Regional disease - surgery with adjuvant therapy likely"
    elif tumor_size_cm > 2:
        overall_stage = "Stage I-II"
        prognosis = "Early-stage with favorable prognosis"
    else:
        overall_stage = "Stage I"
        prognosis = "Early-stage - excellent prognosis with treatment"

    treatment_approaches = []
    if not metastasis:
        treatment_approaches.append("Surgical resection (primary treatment for localized disease)")
    if lymph_nodes_involved > 0 or tumor_size_cm > 2:
        treatment_approaches.append("Chemotherapy (adjuvant or neoadjuvant)")
    if grade.lower() == "high" or lymph_nodes_involved > 0:
        treatment_approaches.append("Radiation therapy")
    treatment_approaches.append("Targeted therapy / Immunotherapy (based on molecular profiling)")
    if metastasis:
        treatment_approaches.append("Palliative care consultation")

    return {
        "status": "staged",
        "cancer_type": cancer_type,
        "tnm_staging": f"{t_stage}{n_stage}{m_stage}",
        "overall_stage": overall_stage,
        "components": {
            "T": f"{t_stage} (tumor size: {tumor_size_cm} cm)",
            "N": f"{n_stage} ({lymph_nodes_involved} nodes involved)",
            "M": f"{m_stage} ({'distant metastasis present' if metastasis else 'no distant metastasis'})",
            "Grade": grade,
        },
        "prognosis": prognosis,
        "treatment_approaches": treatment_approaches,
        "note": "Final staging requires pathological confirmation. Molecular profiling recommended for treatment planning.",
    }
