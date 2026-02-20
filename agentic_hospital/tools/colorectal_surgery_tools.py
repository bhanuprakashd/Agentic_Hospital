"""Colorectal Surgery-specific diagnostic and screening tools."""


def colorectal_cancer_screening(
    age: int,
    family_history: bool,
    polyp_history: bool,
    ibd_history: bool,
    previous_crc: bool = False,
    high_risk_syndrome: bool = False,
) -> dict:
    """Generates colorectal cancer (CRC) screening recommendations based on risk profile.

    Based on USPSTF and ACG (American College of Gastroenterology) guidelines.

    Args:
        age: Patient age in years.
        family_history: Whether first-degree relative had CRC or advanced adenoma.
        polyp_history: Whether patient has a personal history of colorectal polyps.
        ibd_history: Whether patient has ulcerative colitis or Crohn's disease.
        previous_crc: Whether patient has a personal history of colorectal cancer.
        high_risk_syndrome: Whether patient has Lynch syndrome, FAP, or other hereditary CRC syndrome.

    Returns:
        dict: Screening recommendation, preferred modality, interval, and special considerations.
    """
    recommendations = []
    interval = "N/A"
    modality = ""
    risk_category = "AVERAGE"
    start_age = 45  # USPSTF 2021 recommendation

    # High-risk syndromes
    if high_risk_syndrome:
        risk_category = "VERY HIGH"
        modality = "Colonoscopy"
        interval = "Annual or as directed by genetics specialist"
        recommendations = [
            "Genetic counseling referral mandatory (Lynch syndrome, FAP, MAP, etc.)",
            "Begin colonoscopy at age 20–25 or 10 years before youngest affected relative",
            "Consider prophylactic colectomy discussion for FAP",
        ]
        return {
            "status": "recommendation_generated",
            "risk_category": risk_category,
            "preferred_screening_modality": modality,
            "screening_interval": interval,
            "start_screening_age": "20-25 or per genetics team",
            "recommendations": recommendations,
        }

    # Previous CRC
    if previous_crc:
        risk_category = "HIGH"
        modality = "Colonoscopy"
        interval = "Year 1 post-resection, then every 3–5 years depending on findings"
        recommendations = [
            "CEA every 3–6 months for 5 years",
            "CT chest/abdomen/pelvis annually for 3–5 years",
        ]
        return {
            "status": "recommendation_generated",
            "risk_category": risk_category,
            "preferred_screening_modality": modality,
            "screening_interval": interval,
            "recommendations": recommendations,
        }

    # IBD
    if ibd_history:
        risk_category = "HIGH"
        modality = "Colonoscopy with chromoendoscopy"
        if age >= 18:
            recommendations.append("Begin surveillance 8 years after IBD onset (for pancolitis) or 15 years (left-sided colitis)")
            recommendations.append("Colonoscopy every 1–3 years thereafter")
            interval = "Every 1–3 years based on disease extent and activity"

    # Personal polyp history
    elif polyp_history:
        risk_category = "HIGH"
        modality = "Colonoscopy"
        interval = "3–5 years depending on polyp number, size, and histology"
        recommendations.append("Surveillance interval based on prior colonoscopy findings (per gastroenterologist)")

    # Family history
    elif family_history:
        risk_category = "INCREASED"
        modality = "Colonoscopy"
        start_age = min(40, age)  # Start at 40 or 10 years before youngest family member's diagnosis
        interval = "Every 5 years"
        recommendations.append(f"Begin colonoscopy at age 40 (or 10 years before youngest relative's diagnosis)")

    # Average risk
    else:
        risk_category = "AVERAGE"
        if age < start_age:
            return {
                "status": "recommendation_generated",
                "risk_category": risk_category,
                "recommendation": f"Screening recommended starting at age {start_age}. Patient is currently {age}.",
                "preferred_screening_modality": "Colonoscopy every 10 years OR annual FIT/gFOBT",
                "screening_interval": "Begin at age 45",
            }
        modality = "Colonoscopy (preferred) OR annual FIT test"
        interval = "Colonoscopy every 10 years; annual FIT if colonoscopy declined"
        recommendations.append("FIT (fecal immunochemical test) annually is an acceptable alternative to colonoscopy")
        recommendations.append("CT colonography every 5 years is another alternative modality")

    if not recommendations:
        recommendations.append(f"Colonoscopy with {interval} intervals recommended")

    return {
        "status": "recommendation_generated",
        "patient_age": age,
        "risk_category": risk_category,
        "risk_factors": {
            "family_history_crc": family_history,
            "personal_polyp_history": polyp_history,
            "ibd_history": ibd_history,
        },
        "preferred_screening_modality": modality,
        "screening_interval": interval,
        "recommendations": recommendations,
    }


def bowel_obstruction_assessment(
    symptoms: list[str],
    severity: str,
    duration: str,
    prior_abdominal_surgery: bool = False,
    vomiting_character: str = "unknown",
) -> dict:
    """Assesses bowel obstruction type, severity, and management approach.

    Args:
        symptoms: List of symptoms (e.g., ['abdominal distension', 'nausea', 'vomiting', 'no bowel movements']).
        severity: Severity of symptoms ('mild', 'moderate', 'severe').
        duration: Duration of symptoms (e.g., '6 hours', '2 days').
        prior_abdominal_surgery: Whether patient has had previous abdominal surgery (adhesion risk).
        vomiting_character: Character of vomit ('bilious', 'feculent', 'non-bilious', 'unknown').

    Returns:
        dict: Suspected obstruction type, strangulation risk, urgency, and management plan.
    """
    symptoms_lower = [s.lower() for s in symptoms]

    # Classify obstruction type
    sbo_features = ["nausea", "vomiting", "cramping", "early distension", "prior surgery"]
    lbo_features = ["constipation", "massive distension", "late vomiting", "late onset", "change in bowel habit"]

    sbo_score = sum(1 for s in symptoms_lower if any(f in s for f in sbo_features))
    if prior_abdominal_surgery:
        sbo_score += 2
    lbo_score = sum(1 for s in symptoms_lower if any(f in s for f in lbo_features))

    obstruction_type = "Small Bowel Obstruction (SBO)" if sbo_score >= lbo_score else "Large Bowel Obstruction (LBO)"

    # Strangulation risk factors
    strangulation_signs = []
    if any("fever" in s or "rigidity" in s or "peritonitis" in s or "constant pain" in s for s in symptoms_lower):
        strangulation_signs.append("Peritoneal signs or constant pain — strangulation risk HIGH")
    if severity == "severe":
        strangulation_signs.append("Severe severity — consider closed loop or strangulated obstruction")
    if vomiting_character == "feculent":
        strangulation_signs.append("Feculent vomiting — prolonged or low SBO / LBO")

    strangulation_risk = "HIGH" if strangulation_signs else "LOW to MODERATE"

    # Vomiting pattern clues
    obstruction_level = "Unknown"
    if vomiting_character == "non-bilious":
        obstruction_level = "Proximal to Ampulla of Vater (gastric or pyloric)"
    elif vomiting_character == "bilious":
        obstruction_level = "Distal to Ligament of Treitz (jejunum or beyond)"
    elif vomiting_character == "feculent":
        obstruction_level = "Distal ileum or colon"

    # Urgency and management
    if strangulation_risk == "HIGH":
        urgency = "EMERGENT"
        management = [
            "EMERGENT surgical exploration — do not delay",
            "IV fluid resuscitation",
            "NGT decompression",
            "Broad-spectrum antibiotics",
            "Urgent surgical consultation",
            "CT abdomen/pelvis with IV contrast (if time allows)",
        ]
    elif severity == "severe":
        urgency = "URGENT"
        management = [
            "CT abdomen/pelvis with contrast to confirm diagnosis",
            "NPO, IV fluids, NGT insertion",
            "Surgical consultation within hours",
            "Serial abdominal exams",
            "Bowel rest trial 24–48h for SBO without strangulation",
        ]
    else:
        urgency = "NON-EMERGENT"
        management = [
            "CT abdomen/pelvis for confirmation",
            "NPO, IV fluids",
            "NGT decompression if vomiting",
            "Trial of conservative management 24–48h",
            "Surgical consultation",
            "Water-soluble contrast challenge (Gastrografin) for SBO",
        ]

    return {
        "status": "assessed",
        "suspected_obstruction_type": obstruction_type,
        "suspected_obstruction_level": obstruction_level,
        "strangulation_risk": strangulation_risk,
        "strangulation_indicators": strangulation_signs,
        "urgency": urgency,
        "prior_abdominal_surgery": prior_abdominal_surgery,
        "management_plan": management,
        "immediate_actions": [
            "ABG / lactate (elevated lactate suggests ischemia)",
            "CBC, BMP, lipase",
            "Upright CXR / AXR as initial imaging",
            "CT abdomen/pelvis with contrast for definitive evaluation",
        ],
    }
