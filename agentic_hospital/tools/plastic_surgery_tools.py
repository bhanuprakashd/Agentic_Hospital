"""Plastic Surgery-specific diagnostic and assessment tools."""


def burn_assessment(total_body_surface_area_percent: float, burn_depth: str,
                    age: int, weight_kg: float, inhalation_injury: bool,
                    hours_since_burn: float) -> dict:
    """Assesses burn severity and calculates initial fluid resuscitation.

    Uses the Parkland formula and ABA burn center referral criteria.

    Args:
        total_body_surface_area_percent: TBSA burned (%) — exclude superficial/1st-degree.
        burn_depth: Deepest burn depth: 'superficial', 'partial_thickness', 'full_thickness'.
        age: Patient age in years.
        weight_kg: Patient weight in kilograms.
        inhalation_injury: True if inhalation injury is confirmed or suspected.
        hours_since_burn: Hours elapsed since burn occurred.

    Returns:
        dict: Burn severity, ABA referral criteria met, Parkland fluid requirement,
              wound care recommendations, and disposition.
    """
    # ABA burn center referral criteria
    referral_criteria = []
    if total_body_surface_area_percent >= 10:
        referral_criteria.append(f"TBSA ≥10% ({total_body_surface_area_percent}%)")
    if burn_depth == "full_thickness" and total_body_surface_area_percent >= 1:
        referral_criteria.append("Full-thickness burns present")
    if inhalation_injury:
        referral_criteria.append("Inhalation injury")
    if age < 10 or age > 50:
        referral_criteria.append(f"Age risk group ({age} years)")
    special_areas = total_body_surface_area_percent > 0  # proxy — agent evaluates location
    if special_areas and burn_depth in ("partial_thickness", "full_thickness"):
        referral_criteria.append("Burns to face/hands/feet/genitalia/major joints (verify location)")

    # Severity classification
    if total_body_surface_area_percent < 10 and burn_depth == "superficial":
        severity = "MINOR"
    elif total_body_surface_area_percent < 20 and not inhalation_injury:
        severity = "MODERATE"
    elif total_body_surface_area_percent >= 20 or inhalation_injury or burn_depth == "full_thickness":
        severity = "MAJOR"
    else:
        severity = "MODERATE"

    # Parkland formula: 4 mL × weight_kg × TBSA%
    # Half in first 8 hours from time of burn, half over next 16 hours
    parkland_total_24h_ml = 4 * weight_kg * total_body_surface_area_percent
    hours_remaining_first_8 = max(0, 8 - hours_since_burn)
    if hours_remaining_first_8 > 0 and hours_remaining_first_8 < 8:
        first_half_rate_ml_hr = (parkland_total_24h_ml / 2) / hours_remaining_first_8
    elif hours_remaining_first_8 == 8:
        first_half_rate_ml_hr = (parkland_total_24h_ml / 2) / 8
    else:
        first_half_rate_ml_hr = 0  # first 8 hours already elapsed
    second_half_rate_ml_hr = (parkland_total_24h_ml / 2) / 16

    # Wound care by depth
    wound_care = {
        "superficial": "Cool water irrigation 10–20 min. Non-adherent dressing. Analgesia. No debridement.",
        "partial_thickness": "Gentle cleansing. Silver sulfadiazine or mafenide cream, or biologic dressing. Daily dressing changes. Tetanus prophylaxis.",
        "full_thickness": "Surgical debridement and skin grafting required. ICU monitoring if major burn. Early excision within 24–72 hours improves outcomes.",
    }.get(burn_depth, "Assess depth; treat accordingly.")

    # Disposition
    if severity == "MINOR":
        disposition = "Outpatient wound care with burn clinic follow-up in 48 hours."
    elif severity == "MODERATE":
        disposition = "Hospital admission. Consider burn center transfer per referral criteria."
    else:
        disposition = "Burn center transfer strongly recommended. Initiate Parkland resuscitation immediately."

    return {
        "status": "assessed",
        "burn_severity": severity,
        "tbsa_percent": total_body_surface_area_percent,
        "burn_depth": burn_depth,
        "inhalation_injury": inhalation_injury,
        "aba_burn_center_referral": {
            "criteria_met": referral_criteria,
            "transfer_recommended": len(referral_criteria) > 0,
        },
        "parkland_resuscitation": {
            "total_24h_ml": round(parkland_total_24h_ml),
            "fluid": "Lactated Ringer's solution",
            "first_8h_rate_ml_hr": round(first_half_rate_ml_hr) if first_half_rate_ml_hr else "First 8h elapsed",
            "next_16h_rate_ml_hr": round(second_half_rate_ml_hr),
            "note": "Titrate to urine output 0.5–1.0 mL/kg/hr (adults); 1.0 mL/kg/hr (children <30 kg)",
        },
        "wound_care": wound_care,
        "monitoring": [
            "Urine output every hour via Foley catheter",
            "Core temperature monitoring",
            "Electrolytes every 6 hours",
            "Albumin and hemoglobin daily",
            "Wound re-evaluation at 48–72 hours for depth reclassification",
        ],
        "disposition": disposition,
    }


def reconstructive_planning(defect_location: str, defect_size_cm2: float,
                             defect_type: str, cause: str,
                             patient_comorbidities: list[str]) -> dict:
    """Plans reconstructive surgery using the reconstructive ladder.

    Selects the optimal reconstructive option based on defect characteristics,
    following the reconstructive ladder (simple → complex).

    Args:
        defect_location: Anatomical location (e.g., 'scalp', 'face', 'hand', 'lower_leg', 'breast').
        defect_size_cm2: Defect surface area in square centimeters.
        defect_type: Type of defect: 'cutaneous', 'composite', 'bone', 'nerve', 'vessel'.
        cause: Cause of defect: 'cancer_resection', 'trauma', 'burn', 'infection', 'congenital'.
        patient_comorbidities: List of relevant comorbidities (e.g., ['diabetes', 'smoking', 'obesity']).

    Returns:
        dict: Recommended reconstructive options ranked from simplest to most complex,
              with donor site considerations and expected outcomes.
    """
    # Risk factor assessment
    high_risk = []
    if "diabetes" in patient_comorbidities:
        high_risk.append("Diabetes: impaired wound healing, infection risk")
    if "smoking" in patient_comorbidities:
        high_risk.append("Smoking: vasoconstriction, flap ischemia risk — advise cessation ≥4 weeks pre-op")
    if "obesity" in patient_comorbidities:
        high_risk.append("Obesity: wound dehiscence, seroma risk")
    if "peripheral_vascular_disease" in patient_comorbidities or "pvd" in patient_comorbidities:
        high_risk.append("PVD: limits pedicled flap reliability; consider free flap")
    if "radiation" in patient_comorbidities or "prior_radiation" in patient_comorbidities:
        high_risk.append("Prior radiation: poor wound bed; prefer vascularized tissue transfer")

    # Location-specific best options
    location_options = {
        "scalp": {
            "small": ["Primary closure", "Local rotation flap (Limberg, Rhomboid)"],
            "medium": ["Tissue expansion + advancement", "Galeal scoring + advancement"],
            "large": ["Free tissue transfer (latissimus dorsi, ALT)", "Tissue expansion x2"],
        },
        "face": {
            "small": ["Primary closure", "Local flap (bilobed, Z-plasty, advancement)"],
            "medium": ["Regional flap (nasolabial, forehead)", "Full-thickness skin graft"],
            "large": ["Free tissue transfer (radial forearm, ALT)", "Total face reconstruction"],
        },
        "hand": {
            "small": ["Primary closure", "Full-thickness skin graft (FTSG)", "Thenar/hypothenar flap"],
            "medium": ["Cross-finger flap", "Groin flap (pedicled)", "Reverse radial forearm flap"],
            "large": ["Free tissue transfer", "Composite tissue allotransplantation (CTA)"],
        },
        "lower_leg": {
            "small": ["Split-thickness skin graft (STSG)", "Local fasciocutaneous flap"],
            "medium": ["Propeller flap", "Gastrocnemius/soleus flap (proximal/middle leg)"],
            "large": ["Free tissue transfer (ALT, gracilis, latissimus)"],
        },
        "breast": {
            "small": ["Implant-based reconstruction (tissue expander → implant)", "Oncoplastic reduction"],
            "medium": ["Latissimus dorsi (LD) flap ± implant", "DIEP flap"],
            "large": ["DIEP flap (gold standard)", "TRAM flap", "SIEA flap"],
        },
    }

    size_category = "small" if defect_size_cm2 < 10 else ("medium" if defect_size_cm2 < 50 else "large")
    loc_key = defect_location.lower().replace(" ", "_")
    options = location_options.get(loc_key, {}).get(size_category, [
        "Primary closure if tension-free",
        "Split-thickness skin graft",
        "Local random pattern flap",
        "Regional pedicled flap",
        "Free tissue transfer (microsurgery)",
    ])

    # Add complexity based on defect type
    if defect_type in ("composite", "bone"):
        options.append("Vascularized bone flap (fibula, iliac crest) for bony defects")
    if defect_type == "nerve":
        options.append("Nerve graft (sural nerve), nerve conduit, or nerve transfer")
    if defect_type == "vessel":
        options.append("Vein graft interpositional repair or bypass")

    # Post-op monitoring for free flap
    free_flap_monitoring = []
    if "Free tissue transfer" in str(options) or "free flap" in str(options).lower():
        free_flap_monitoring = [
            "Hourly clinical flap monitoring for 72 hours (color, turgor, capillary refill, temperature)",
            "Handheld Doppler or implantable Doppler probe",
            "Maintain warm environment (>21°C), avoid vasopressors",
            "Keep well-hydrated (target: euvolemia)",
            "Anticoagulation per protocol (aspirin ± heparin infusion)",
        ]

    return {
        "status": "planned",
        "defect": {
            "location": defect_location,
            "size_cm2": defect_size_cm2,
            "size_category": size_category,
            "type": defect_type,
            "cause": cause,
        },
        "risk_factors": high_risk,
        "risk_level": "HIGH" if len(high_risk) >= 2 else ("MODERATE" if high_risk else "LOW"),
        "reconstructive_ladder_options": options,
        "recommended_option": options[-1] if len(high_risk) >= 2 else options[0],
        "free_flap_monitoring": free_flap_monitoring,
        "timing": {
            "cancer_resection": "Immediate reconstruction preferred (single anesthesia)",
            "trauma": "Delayed primary closure (48–72 h) or early definitive (72 h–7 days)",
            "burn": "Early excision and grafting within 24–72 hours",
            "infection": "Reconstruction after infection fully cleared (2–6 weeks)",
            "congenital": "Age-appropriate timing per protocol",
        }.get(cause, "Timing per clinical judgment"),
        "expected_outcomes": "Functional restoration primary goal; aesthetic optimization secondary. Discuss realistic expectations with patient.",
    }
