"""Ophthalmology-specific diagnostic and assessment tools."""


def vision_assessment(
    right_eye_acuity: str,
    left_eye_acuity: str,
    right_eye_pressure: int = None,
    left_eye_pressure: int = None,
    pupil_response: str = "normal",
    red_reflex: str = "normal",
    symptoms: list[str] = None,
) -> dict:
    """Assesses vision and eye health based on examination findings.

    Args:
        right_eye_acuity: Visual acuity right eye (e.g., '20/20', '20/40', 'CF', 'HM', 'LP').
        left_eye_acuity: Visual acuity left eye.
        right_eye_pressure: Intraocular pressure right eye in mmHg (normal 10-21).
        left_eye_pressure: Intraocular pressure left eye in mmHg.
        pupil_response: Pupil response ('normal', 'RAPD', 'sluggish', 'fixed').
        red_reflex: Red reflex assessment ('normal', 'absent', 'white', 'asymmetric').
        symptoms: List of presenting symptoms.

    Returns:
        dict: Vision assessment with findings interpretation and recommendations.
    """
    findings = []
    urgency = "ROUTINE"

    # Visual acuity interpretation
    def interpret_acuity(acuity):
        if acuity == "20/20" or acuity == "20/25":
            return "Normal"
        elif acuity in ["20/30", "20/40"]:
            return "Mild impairment"
        elif acuity in ["20/50", "20/60", "20/70", "20/80"]:
            return "Moderate impairment"
        elif acuity in ["20/100", "20/200"]:
            return "Severe impairment (legal blindness threshold)"
        elif acuity in ["CF", "HM"]:
            return "Severe impairment (count fingers/hand motion)"
        elif acuity == "LP":
            return "Profound impairment (light perception only)"
        elif acuity == "NLP":
            return "No light perception (blind)"
        return "Unknown"

    right_status = interpret_acuity(right_eye_acuity)
    left_status = interpret_acuity(left_eye_acuity)

    if "Severe" in right_status or "Profound" in right_status or right_status == "No light perception (blind)":
        findings.append(f"Right eye: {right_status}")
    if "Severe" in left_status or "Profound" in left_status or left_status == "No light perception (blind)":
        findings.append(f"Left eye: {left_status}")

    # Intraocular pressure assessment
    if right_eye_pressure is not None:
        if right_eye_pressure > 30:
            findings.append(f"CRITICAL: Right eye IOP {right_eye_pressure} mmHg - acute glaucoma concern")
            urgency = "EMERGENT"
        elif right_eye_pressure > 21:
            findings.append(f"Right eye IOP elevated ({right_eye_pressure} mmHg)")
    if left_eye_pressure is not None:
        if left_eye_pressure > 30:
            findings.append(f"CRITICAL: Left eye IOP {left_eye_pressure} mmHg - acute glaucoma concern")
            urgency = "EMERGENT"
        elif left_eye_pressure > 21:
            findings.append(f"Left eye IOP elevated ({left_eye_pressure} mmHg)")

    # Pupil response
    if pupil_response == "RAPD":
        findings.append("Relative afferent pupillary defect (RAPD) - optic nerve or retinal pathology")
    elif pupil_response == "fixed":
        findings.append("CRITICAL: Fixed pupil - emergency evaluation needed")
        urgency = "EMERGENT"

    # Red reflex
    if red_reflex == "white":
        findings.append("CRITICAL: White reflex (leukocoria) - rule out retinoblastoma or cataract")
        urgency = "URGENT"
    elif red_reflex == "absent":
        findings.append("Absent red reflex - possible media opacity")
        urgency = "URGENT" if urgency == "ROUTINE" else urgency
    elif red_reflex == "asymmetric":
        findings.append("Asymmetric red reflex - evaluate for strabismus or media opacity")

    # Symptom-based concerns
    if symptoms:
        emergency_symptoms = ["sudden vision loss", "flashes", "curtain", "eye pain", "double vision", "halos"]
        for symptom in symptoms:
            if any(es in symptom.lower() for es in emergency_symptoms):
                if urgency == "ROUTINE":
                    urgency = "URGENT"
                findings.append(f"Concerning symptom: {symptom}")

    # Recommendations
    recommendations = []
    if urgency == "EMERGENT":
        recommendations.append("IMMEDIATE ophthalmology consultation")
        recommendations.append("If acute angle-closure glaucoma suspected: IV acetazolamide, topical pilocarpine")
    elif urgency == "URGENT":
        recommendations.append("Same-day or urgent ophthalmology referral")
    else:
        recommendations.append("Routine ophthalmology referral")
        recommendations.append("Annual dilated eye exam recommended")

    # Additional workup
    workup = ["Dilated fundus examination"]
    if right_eye_pressure and left_eye_pressure and (right_eye_pressure > 21 or left_eye_pressure > 21):
        workup.append("Gonioscopy")
        workup.append("Visual field testing")
    if "flashes" in str(symptoms).lower() or "floaters" in str(symptoms).lower():
        workup.append("Urgent dilated exam to rule out retinal detachment")

    return {
        "status": "assessed",
        "right_eye": {
            "visual_acuity": right_eye_acuity,
            "interpretation": right_status,
            "intraocular_pressure": f"{right_eye_pressure} mmHg" if right_eye_pressure else "Not measured",
        },
        "left_eye": {
            "visual_acuity": left_eye_acuity,
            "interpretation": left_status,
            "intraocular_pressure": f"{left_eye_pressure} mmHg" if left_eye_pressure else "Not measured",
        },
        "pupil_response": pupil_response,
        "red_reflex": red_reflex,
        "findings": findings if findings else ["No significant abnormalities detected"],
        "urgency": urgency,
        "recommendations": recommendations,
        "recommended_workup": workup,
    }


def glaucoma_risk_assessment(
    intraocular_pressure: int,
    cup_disc_ratio: float,
    family_history_glaucoma: bool,
    age: int,
    race: str,
    myopia: bool = False,
    diabetes: bool = False,
    hypertension: bool = False,
) -> dict:
    """Assesses glaucoma risk and screening recommendations.

    Args:
        intraocular_pressure: IOP in mmHg (normal 10-21).
        cup_disc_ratio: Optic disc cup-to-disc ratio (normal < 0.4).
        family_history_glaucoma: Whether patient has family history of glaucoma.
        age: Patient age in years.
        race: Patient race/ethnicity ('white', 'black', 'asian', 'hispanic').
        myopia: Whether patient has myopia (nearsightedness).
        diabetes: Whether patient has diabetes.
        hypertension: Whether patient has hypertension.

    Returns:
        dict: Glaucoma risk assessment with recommendations.
    """
    risk_score = 0
    risk_factors = []

    # IOP contribution
    if intraocular_pressure > 30:
        risk_score += 4
        risk_factors.append(f"Very elevated IOP ({intraocular_pressure} mmHg) - HIGH RISK")
    elif intraocular_pressure > 25:
        risk_score += 3
        risk_factors.append(f"Elevated IOP ({intraocular_pressure} mmHg)")
    elif intraocular_pressure > 21:
        risk_score += 2
        risk_factors.append(f"Borderline elevated IOP ({intraocular_pressure} mmHg)")
    elif intraocular_pressure < 10:
        risk_score += 1
        risk_factors.append(f"Low IOP ({intraocular_pressure} mmHg) - monitor")

    # Cup-to-disc ratio
    if cup_disc_ratio > 0.8:
        risk_score += 4
        risk_factors.append(f"Severe optic disc cupping (C/D ratio {cup_disc_ratio})")
    elif cup_disc_ratio > 0.6:
        risk_score += 3
        risk_factors.append(f"Moderate optic disc cupping (C/D ratio {cup_disc_ratio})")
    elif cup_disc_ratio > 0.4:
        risk_score += 1
        risk_factors.append(f"Mild optic disc cupping (C/D ratio {cup_disc_ratio})")

    # Age
    if age >= 70:
        risk_score += 2
        risk_factors.append(f"Age ≥ 70 ({age})")
    elif age >= 60:
        risk_score += 1
        risk_factors.append(f"Age ≥ 60 ({age})")

    # Race (higher risk in African Americans)
    if race.lower() in ["black", "african american"]:
        risk_score += 2
        risk_factors.append("African American race - increased glaucoma risk")

    # Family history
    if family_history_glaucoma:
        risk_score += 2
        risk_factors.append("Family history of glaucoma")

    # Other risk factors
    if myopia:
        risk_score += 1
        risk_factors.append("Myopia")
    if diabetes:
        risk_score += 1
        risk_factors.append("Diabetes")
    if hypertension:
        risk_score += 1
        risk_factors.append("Hypertension")

    # Risk classification
    if risk_score >= 8:
        risk_level = "HIGH"
        screening_interval = "Every 6-12 months"
        recommendation = "Urgent ophthalmology referral for comprehensive glaucoma evaluation"
    elif risk_score >= 5:
        risk_level = "MODERATE"
        screening_interval = "Every 1-2 years"
        recommendation = "Ophthalmology referral for baseline glaucoma evaluation"
    else:
        risk_level = "LOW"
        screening_interval = "Every 2-4 years (or as per age-based guidelines)"
        recommendation = "Routine eye exam with IOP measurement"

    return {
        "status": "assessed",
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors if risk_factors else ["No significant risk factors identified"],
        "intraocular_pressure": f"{intraocular_pressure} mmHg",
        "cup_disc_ratio": cup_disc_ratio,
        "screening_interval": screening_interval,
        "recommendation": recommendation,
        "glaucoma_type_considerations": {
            "IOP_elevated": "Primary open-angle glaucoma if IOP > 21 mmHg",
            "angle_closure": "Consider gonioscopy if narrow angles suspected",
            "normal_tension": "Normal-tension glaucoma if cupping with normal IOP",
        },
        "treatment_options_if_glaucoma": [
            "Topical IOP-lowering drops (prostaglandin analogs, beta-blockers, etc.)",
            "Laser trabeculoplasty (SLT)",
            "Surgical options (trabeculectomy, tube shunt) if progressive",
        ],
    }