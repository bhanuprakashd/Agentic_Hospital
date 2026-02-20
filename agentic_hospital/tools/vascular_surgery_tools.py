"""Vascular Surgery-specific diagnostic and assessment tools."""


def peripheral_arterial_disease_assessment(
    symptoms: list[str],
    ankle_brachial_index: float,
    risk_factors: list[str],
    wound_present: bool = False,
    resting_pain: bool = False,
) -> dict:
    """Assesses peripheral arterial disease severity and treatment options.

    Args:
        symptoms: List of symptoms (e.g., ['claudication', 'leg_pain', 'numbness']).
        ankle_brachial_index: Ankle-brachial index (normal 0.9-1.3).
        risk_factors: List of risk factors (e.g., ['diabetes', 'smoking', 'hypertension']).
        wound_present: Whether there is a wound/ulcer on the affected limb.
        resting_pain: Whether patient has pain at rest.

    Returns:
        dict: PAD assessment with severity classification and management.
    """
    # ABI interpretation
    if ankle_brachial_index > 1.3:
        abi_category = "Non-compressible vessels"
        abi_severity = "INCONCLUSIVE"
        note = "Vessels non-compressible (common in diabetes); consider toe-brachial index"
    elif ankle_brachial_index >= 0.9:
        abi_category = "Normal"
        abi_severity = "NONE"
        note = "Normal ABI"
    elif ankle_brachial_index >= 0.7:
        abi_category = "Mild PAD"
        abi_severity = "MILD"
        note = "Mild disease; may be asymptomatic or mild claudication"
    elif ankle_brachial_index >= 0.4:
        abi_category = "Moderate PAD"
        abi_severity = "MODERATE"
        note = "Moderate disease; claudication likely"
    else:
        abi_category = "Severe PAD"
        abi_severity = "SEVERE"
        note = "Severe disease; limb-threatening ischemia risk"

    # Fontaine classification
    if wound_present or resting_pain:
        if wound_present:
            fontaine_stage = "IV"
            fontaine_description = "Tissue loss / gangrene - CRITICAL LIMB ISCHEMIA"
        else:
            fontaine_stage = "III"
            fontaine_description = "Rest pain - CRITICAL LIMB ISCHEMIA"
        urgency = "URGENT"
    elif "claudication" in [s.lower() for s in symptoms]:
        fontaine_stage = "II"
        fontaine_description = "Intermittent claudication"
        urgency = "NON-URGENT"
    elif any(s in [s.lower() for s in symptoms] for s in ["pain", "numbness", "cold"]):
        fontaine_stage = "I"
        fontaine_description = "Asymptomatic or atypical symptoms"
        urgency = "NON-URGENT"
    else:
        fontaine_stage = "I"
        fontaine_description = "Asymptomatic"
        urgency = "NON-URGENT"

    # Treatment recommendations
    conservative = [
        "Smoking cessation (CRITICAL)",
        "Supervised exercise therapy (40 min, 3x/week)",
        "Antiplatelet therapy (aspirin 81mg or clopidogrel 75mg)",
        "Statin therapy (high-intensity)",
        "Blood pressure control (< 130/80)",
        "Diabetes management (HbA1c < 7%)",
    ]

    interventions = []
    if abi_severity in ["MODERATE", "SEVERE"] or fontaine_stage in ["III", "IV"]:
        interventions.append("Vascular surgery consultation")
        interventions.append("CT angiography or duplex ultrasound for anatomic assessment")
        if fontaine_stage in ["III", "IV"]:
            interventions.append("URGENT: Revascularization consideration (angioplasty/stent vs bypass)")
            interventions.append("Wound care if ulceration present")
    elif "claudication" in [s.lower() for s in symptoms]:
        interventions.append("Cilostazol 100mg twice daily (if no heart failure)")
        interventions.append("Consider revascularization if lifestyle-limiting despite conservative therapy")

    # Risk factor management
    rf_management = []
    for rf in risk_factors:
        rf_lower = rf.lower()
        if "smok" in rf_lower:
            rf_management.append("Smoking cessation - most important intervention")
        if "diabet" in rf_lower:
            rf_management.append("Tight glycemic control; foot inspection daily")
        if "hypertension" in rf_lower or "bp" in rf_lower:
            rf_management.append("ACE inhibitor or ARB for blood pressure")
        if "lipid" in rf_lower or "cholesterol" in rf_lower:
            rf_management.append("High-intensity statin (atorvastatin 40-80mg)")

    return {
        "status": "assessed",
        "ankle_brachial_index": ankle_brachial_index,
        "abi_category": abi_category,
        "pad_severity": abi_severity,
        "fontaine_stage": fontaine_stage,
        "fontaine_description": fontaine_description,
        "urgency": urgency,
        "critical_limb_ischemia": fontaine_stage in ["III", "IV"],
        "conservative_management": conservative,
        "intervention_options": interventions if interventions else ["Conservative management initially"],
        "risk_factor_management": rf_management if rf_management else ["Address modifiable risk factors"],
        "follow_up": [
            "Repeat ABI in 6-12 months if stable",
            "Foot exam at every visit if diabetic",
            "Immediate return for new wounds, rest pain, or worsening symptoms",
        ],
    }


def aortic_aneurysm_assessment(
    aneurysm_diameter_cm: float,
    location: str,
    age: int,
    symptoms: list[str],
    growth_rate_cm_per_year: float = None,
    female: bool = False,
) -> dict:
    """Assesses aortic aneurysm and determines surveillance vs repair timing.

    Args:
        aneurysm_diameter_cm: Maximum aneurysm diameter in centimeters.
        location: Aneurysm location ('abdominal', 'thoracic', 'thoracoabdominal').
        age: Patient age in years.
        symptoms: List of symptoms (e.g., ['back_pain', 'abdominal_pain']).
        growth_rate_cm_per_year: Annual growth rate in cm/year if known.
        female: Whether patient is female.

    Returns:
        dict: Aneurysm assessment with surveillance or repair recommendations.
    """
    # Diameter thresholds for intervention
    rupture_risk = "LOW"
    intervention_threshold = 5.5 if not female else 5.0  # Lower threshold for women

    if location.lower() == "abdominal":
        if aneurysm_diameter_cm >= 5.5:
            intervention = "RECOMMENDED"
            rupture_risk = "MODERATE to HIGH"
        elif aneurysm_diameter_cm >= 5.0:
            intervention = "CONSIDER (especially if female or high-risk features)"
            rupture_risk = "MODERATE"
        else:
            intervention = "SURVEILLANCE"
    elif location.lower() == "thoracic":
        intervention_threshold = 6.0
        if aneurysm_diameter_cm >= 6.0:
            intervention = "RECOMMENDED"
            rupture_risk = "MODERATE to HIGH"
        elif aneurysm_diameter_cm >= 5.5:
            intervention = "CONSIDER"
            rupture_risk = "MODERATE"
        else:
            intervention = "SURVEILLANCE"
    else:  # thoracoabdominal
        intervention_threshold = 6.0
        if aneurysm_diameter_cm >= 6.0:
            intervention = "RECOMMENDED"
            rupture_risk = "HIGH"
        else:
            intervention = "SURVEILLANCE"

    # Growth rate consideration
    if growth_rate_cm_per_year is not None and growth_rate_cm_per_year > 0.5:
        intervention = "CONSIDER (rapid growth > 0.5 cm/year)"
        rupture_risk = "INCREASED"

    # Symptomatic aneurysm = emergency
    emergency = False
    concerning_symptoms = ["severe_back_pain", "severe_abdominal_pain", "tearing_pain", "hypotension"]
    if any(s in [sym.lower() for sym in symptoms] for s in concerning_symptoms):
        emergency = True
        intervention = "EMERGENT"
        rupture_risk = "IMMINENT"

    # Surveillance interval
    if aneurysm_diameter_cm < 3.0:
        surveillance_interval = "No surveillance needed (normal aorta)"
    elif aneurysm_diameter_cm < 4.0:
        surveillance_interval = "Ultrasound every 3 years"
    elif aneurysm_diameter_cm < 4.5:
        surveillance_interval = "Ultrasound every 12 months"
    elif aneurysm_diameter_cm < 5.5:
        surveillance_interval = "Ultrasound or CT every 6 months"
    else:
        surveillance_interval = "Imaging as part of pre-operative planning"

    # Repair options
    repair_options = []
    if location.lower() == "abdominal" and intervention != "SURVEILLANCE":
        repair_options = [
            "Endovascular Aneurysm Repair (EVAR) - if anatomy suitable",
            "Open Surgical Repair - if not EVAR candidate",
        ]
    elif location.lower() == "thoracic" and intervention != "SURVEILLANCE":
        repair_options = [
            "Thoracic Endovascular Aortic Repair (TEVAR) - preferred if anatomy suitable",
            "Open Surgical Repair - for complex anatomy",
        ]

    return {
        "status": "assessed",
        "aneurysm_diameter": f"{aneurysm_diameter_cm} cm",
        "location": location,
        "intervention_threshold": f"{intervention_threshold} cm",
        "intervention_recommendation": intervention,
        "rupture_risk": rupture_risk,
        "emergency": emergency,
        "symptomatic": len(symptoms) > 0,
        "surveillance_interval": surveillance_interval if intervention == "SURVEILLANCE" else "N/A - intervention recommended",
        "repair_options": repair_options if repair_options else ["Surveillance - no repair indicated currently"],
        "risk_factor_modification": [
            "Smoking cessation - most important",
            "Blood pressure control",
            "Statin therapy",
            "Avoid heavy lifting if large aneurysm",
        ],
        "warning_signs": [
            "Seek immediate medical attention for: sudden severe back/abdominal pain, tearing sensation, dizziness, fainting",
        ],
    }