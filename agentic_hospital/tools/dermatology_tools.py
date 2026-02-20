"""Dermatology-specific diagnostic and assessment tools."""


def skin_lesion_analysis(
    description: str,
    location: str,
    size_mm: float,
    color: str,
    border: str,
    duration: str,
    changes_noted: list[str],
    pain_or_itch: str,
) -> dict:
    """Analyzes skin lesion characteristics using ABCDE criteria for melanoma screening.

    Args:
        description: Description of the lesion (e.g., 'raised mole', 'flat patch', 'scaly plaque').
        location: Body location of the lesion.
        size_mm: Diameter of the lesion in millimeters.
        color: Color description (e.g., 'brown', 'multicolored', 'pink', 'black').
        border: Border description ('regular', 'irregular', 'jagged', 'poorly_defined').
        duration: How long the lesion has been present.
        changes_noted: List of changes (e.g., ['growing', 'color change', 'bleeding', 'itching']).
        pain_or_itch: Whether lesion is painful or itchy ('none', 'itchy', 'painful', 'both').

    Returns:
        dict: Lesion analysis with ABCDE score and recommendations.
    """
    abcde_flags = {}
    concern_score = 0

    # A - Asymmetry
    if "irregular" in description.lower() or "asymmetric" in description.lower():
        abcde_flags["A_Asymmetry"] = "POSITIVE - Asymmetric shape noted"
        concern_score += 2
    else:
        abcde_flags["A_Asymmetry"] = "Not noted"

    # B - Border
    if border.lower() in ["irregular", "jagged", "poorly_defined"]:
        abcde_flags["B_Border"] = f"POSITIVE - {border} border"
        concern_score += 2
    else:
        abcde_flags["B_Border"] = "Regular border"

    # C - Color
    concerning_colors = ["multicolored", "black", "blue", "red and brown", "varied"]
    if any(c in color.lower() for c in concerning_colors):
        abcde_flags["C_Color"] = f"POSITIVE - Concerning color: {color}"
        concern_score += 2
    else:
        abcde_flags["C_Color"] = f"Uniform color: {color}"

    # D - Diameter
    if size_mm >= 6:
        abcde_flags["D_Diameter"] = f"POSITIVE - {size_mm}mm (>6mm threshold)"
        concern_score += 1
    else:
        abcde_flags["D_Diameter"] = f"{size_mm}mm (within normal)"

    # E - Evolution
    evolution_signs = ["growing", "color change", "shape change", "new symptoms"]
    evolving = [c for c in changes_noted if any(e in c.lower() for e in evolution_signs)]
    if evolving:
        abcde_flags["E_Evolution"] = f"POSITIVE - Changes noted: {', '.join(evolving)}"
        concern_score += 2
    else:
        abcde_flags["E_Evolution"] = "Stable / No evolution noted"

    # Additional red flags
    if "bleeding" in [c.lower() for c in changes_noted]:
        concern_score += 2

    # Risk assessment
    if concern_score >= 6:
        risk = "HIGH"
        recommendation = "URGENT: Dermatoscopy and biopsy recommended. Refer to dermatologist within 2 weeks."
    elif concern_score >= 3:
        risk = "MODERATE"
        recommendation = "Dermatoscopy recommended. Schedule dermatology evaluation within 1 month."
    else:
        risk = "LOW"
        recommendation = "Monitor for changes. Follow up if any ABCDE changes occur."

    return {
        "status": "analyzed",
        "concern_level": risk,
        "concern_score": concern_score,
        "abcde_assessment": abcde_flags,
        "lesion_details": {
            "description": description,
            "location": location,
            "size_mm": size_mm,
            "color": color,
            "border": border,
            "duration": duration,
            "changes": changes_noted,
        },
        "recommendation": recommendation,
        "note": "Clinical correlation required. Dermoscopy and/or biopsy provide definitive diagnosis.",
    }


def allergy_patch_test_interpretation(
    allergens_tested: list[str],
    reactions: dict[str, str],
    timing_hours: int,
) -> dict:
    """Interprets allergy patch test results.

    Args:
        allergens_tested: List of allergens that were tested.
        reactions: Dictionary mapping allergen name to reaction grade ('negative', 'doubtful', '1+', '2+', '3+').
        timing_hours: Hours since patch application when reading was done (typically 48 or 72).

    Returns:
        dict: Patch test interpretation with identified allergens and avoidance recommendations.
    """
    positive_reactions = []
    negative_reactions = []
    avoidance_guide = {
        "nickel": "Avoid costume jewelry, belt buckles, jean buttons. Use nickel-free alternatives.",
        "fragrance": "Use fragrance-free products. Check ingredients for parfum, linalool, limonene.",
        "preservatives": "Avoid products with methylisothiazolinone (MI), formaldehyde releasers.",
        "latex": "Use non-latex gloves. Alert healthcare providers. Carry medical alert card.",
        "cobalt": "Often cross-reacts with nickel. Avoid blue-pigmented items and certain metals.",
        "chromium": "Avoid leather products tanned with chromium, some cements.",
        "neomycin": "Avoid neomycin-containing topical antibiotics. Use alternatives (mupirocin).",
        "balsam of peru": "Avoid cinnamon, cloves, vanilla, citrus peel, tomato, chocolate in severe cases.",
        "lanolin": "Avoid wool wax-containing products. Check cosmetics and moisturizers.",
        "formaldehyde": "Avoid formaldehyde-releasing preservatives in cosmetics and household products.",
    }

    for allergen in allergens_tested:
        reaction = reactions.get(allergen, "not_tested")
        if reaction in ["1+", "2+", "3+"]:
            severity = {"1+": "Mild", "2+": "Moderate", "3+": "Severe"}[reaction]
            guidance = avoidance_guide.get(allergen.lower(), "Avoid products containing this allergen.")
            positive_reactions.append({
                "allergen": allergen,
                "reaction_grade": reaction,
                "severity": severity,
                "avoidance_guidance": guidance,
            })
        elif reaction == "doubtful":
            positive_reactions.append({
                "allergen": allergen,
                "reaction_grade": "Doubtful (?+)",
                "severity": "Uncertain",
                "avoidance_guidance": "May need repeat testing. Avoid if clinically correlates.",
            })
        else:
            negative_reactions.append(allergen)

    return {
        "status": "interpreted",
        "reading_timing": f"{timing_hours} hours post-application",
        "total_tested": len(allergens_tested),
        "positive_count": len(positive_reactions),
        "positive_reactions": positive_reactions,
        "negative_reactions": negative_reactions,
        "general_advice": "Identified contact allergens should be strictly avoided. Read product labels carefully.",
    }
