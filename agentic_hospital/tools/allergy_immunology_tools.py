"""Allergy and Immunology-specific diagnostic and assessment tools."""


def allergy_skin_test_interpretation(
    reactions: dict[str, int],
    test_type: str,
    negative_control_mm: int = 0,
    positive_control_mm: int = 5,
) -> dict:
    """Interprets allergy skin test results (skin prick or intradermal).

    Args:
        reactions: Dict mapping allergen name to wheal diameter in mm (e.g., {'cat dander': 6, 'dust mite': 4}).
        test_type: Type of test performed - 'skin_prick', 'intradermal', or 'patch'.
        negative_control_mm: Negative control (saline) wheal size in mm (default 0).
        positive_control_mm: Positive control (histamine) wheal size in mm (default 5).

    Returns:
        dict: Interpretation of each allergen result with overall sensitization profile.
    """
    if not reactions:
        return {
            "status": "no_reactions",
            "message": "No allergen reactions provided.",
        }

    # Positive threshold for skin prick test: >= 3mm above negative control
    prick_threshold = negative_control_mm + 3
    # Positive threshold for intradermal: >= 5mm above negative control
    id_threshold = negative_control_mm + 5

    threshold = prick_threshold if test_type != "intradermal" else id_threshold

    positive = {}
    negative = {}
    equivocal = {}

    for allergen, wheal_mm in reactions.items():
        delta = wheal_mm - negative_control_mm
        if test_type == "patch":
            # Patch test grading (ICDRG scale)
            if delta >= 2:
                positive[allergen] = {"wheal_mm": wheal_mm, "grade": "2+ (strong positive)"}
            elif delta >= 1:
                equivocal[allergen] = {"wheal_mm": wheal_mm, "grade": "1+ (weak positive — uncertain)"}
            else:
                negative[allergen] = {"wheal_mm": wheal_mm, "grade": "Negative"}
        else:
            if delta >= threshold:
                size_class = "3+ (large)" if delta >= 10 else "2+ (moderate)" if delta >= 5 else "1+ (mild)"
                positive[allergen] = {"wheal_mm": wheal_mm, "delta_from_negative_mm": delta, "grade": size_class}
            elif delta >= threshold - 2:
                equivocal[allergen] = {"wheal_mm": wheal_mm, "delta_from_negative_mm": delta, "grade": "Equivocal"}
            else:
                negative[allergen] = {"wheal_mm": wheal_mm, "delta_from_negative_mm": delta, "grade": "Negative"}

    profile = "polysensitized" if len(positive) > 3 else "monosensitized" if len(positive) == 1 else "oligosensitized" if positive else "non-sensitized"

    return {
        "status": "interpreted",
        "test_type": test_type,
        "positive_allergens": positive,
        "equivocal_allergens": equivocal,
        "negative_allergens": negative,
        "sensitization_profile": profile,
        "clinical_note": (
            "Positive skin test indicates sensitization, NOT clinical allergy. "
            "Correlate with patient history. Allergen immunotherapy may be considered for significant sensitizations."
        ),
        "recommendation": (
            "Consider allergen avoidance counseling and discuss immunotherapy eligibility "
            "if sensitizations correlate with clinical symptoms."
        ) if positive else "No significant sensitizations detected.",
    }


def immunodeficiency_risk_assessment(
    recurrent_infections: list[str],
    age: int,
    family_history: bool,
    infections_per_year: int = 0,
    unusual_organisms: bool = False,
    treatment_failures: bool = False,
) -> dict:
    """Assesses risk for primary immunodeficiency based on clinical warning signs.

    Uses the Jeffrey Modell Foundation 10 Warning Signs of Primary Immunodeficiency.

    Args:
        recurrent_infections: List of recurrent infection types (e.g., ['pneumonia', 'sinusitis', 'otitis media']).
        age: Patient age in years.
        family_history: Whether there is a family history of primary immunodeficiency or early unexplained death.
        infections_per_year: Number of infections per year requiring antibiotics.
        unusual_organisms: Whether infections are caused by opportunistic or unusual organisms.
        treatment_failures: Whether infections have failed to respond to standard antibiotics.

    Returns:
        dict: Immunodeficiency risk level, warning signs score, and recommended workup.
    """
    warning_signs = []
    score = 0

    # Warning sign 1: Recurrent ear infections
    ear_infections = [i for i in recurrent_infections if "ear" in i.lower() or "otitis" in i.lower()]
    if len(ear_infections) > 0 and age <= 18:
        warning_signs.append("Recurrent ear infections (>4/year in children)")
        score += 1

    # Warning sign 2: Recurrent sinusitis
    sinus = [i for i in recurrent_infections if "sinus" in i.lower()]
    if sinus:
        warning_signs.append("Recurrent sinusitis (>2/year)")
        score += 1

    # Warning sign 3: Recurrent pneumonia
    pneumonia = [i for i in recurrent_infections if "pneumonia" in i.lower() or "lung" in i.lower()]
    if len(pneumonia) >= 2:
        warning_signs.append("Two or more cases of pneumonia in the past year")
        score += 2

    # Warning sign 4: Antibiotics not clearing infections
    if treatment_failures:
        warning_signs.append("Infections not clearing with standard antibiotic courses")
        score += 2

    # Warning sign 5: Unusual organisms
    if unusual_organisms:
        warning_signs.append("Infections with unusual or opportunistic organisms")
        score += 3

    # Warning sign 6: Family history
    if family_history:
        warning_signs.append("Family history of primary immunodeficiency or early unexplained death")
        score += 2

    # Warning sign 7: Frequent antibiotic use
    if infections_per_year >= 4:
        warning_signs.append(f"Requires {infections_per_year}+ antibiotic courses per year")
        score += 1

    # Warning sign 8: Multiple infection sites
    sites = set()
    for inf in recurrent_infections:
        inf_lower = inf.lower()
        if any(k in inf_lower for k in ["ear", "otitis"]): sites.add("ear")
        elif any(k in inf_lower for k in ["sinus", "nasal"]): sites.add("sinuses")
        elif any(k in inf_lower for k in ["pneumonia", "lung", "bronchitis"]): sites.add("lung")
        elif any(k in inf_lower for k in ["skin", "abscess"]): sites.add("skin")
        elif any(k in inf_lower for k in ["meningitis", "brain"]): sites.add("CNS")
        elif any(k in inf_lower for k in ["urinary", "uti"]): sites.add("urinary")
    if len(sites) >= 3:
        warning_signs.append(f"Infections at multiple sites: {', '.join(sites)}")
        score += 1

    # Determine risk level
    if score >= 5 or unusual_organisms or (len(pneumonia) >= 2):
        risk_level = "HIGH"
        workup = [
            "Complete blood count with differential (CBC with diff)",
            "Serum immunoglobulins (IgG, IgA, IgM, IgE)",
            "Specific antibody titers (vaccine responses: tetanus, pneumococcal)",
            "Lymphocyte subsets (CD3, CD4, CD8, CD19, CD16/56)",
            "Complement levels (CH50, C3, C4)",
            "Neutrophil oxidative burst (DHR) for CGD",
            "Urgent referral to immunologist",
        ]
    elif score >= 3:
        risk_level = "MODERATE"
        workup = [
            "Complete blood count with differential",
            "Serum immunoglobulins (IgG, IgA, IgM)",
            "Specific antibody titers to vaccines",
            "Referral to immunologist for further evaluation",
        ]
    else:
        risk_level = "LOW"
        workup = ["No immediate workup required", "Monitor for progression of infections", "Re-evaluate if new warning signs develop"]

    return {
        "status": "assessed",
        "risk_level": risk_level,
        "warning_signs_score": score,
        "warning_signs_identified": warning_signs,
        "warning_signs_count": len(warning_signs),
        "recommended_workup": workup,
        "recommendation": (
            "Urgent immunology referral warranted." if risk_level == "HIGH"
            else "Immunology evaluation recommended." if risk_level == "MODERATE"
            else "Continue monitoring; reassess if infections worsen."
        ),
    }
