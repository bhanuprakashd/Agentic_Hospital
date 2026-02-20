"""Neurosurgery-specific diagnostic and assessment tools."""


def intracranial_pressure_assessment(
    gcs: int,
    pupil_reactivity: str,
    blood_pressure: str,
    headache_severity: int,
    vomiting: bool,
    papilledema: bool = False,
    focal_deficits: list[str] = None,
) -> dict:
    """Assesses intracranial pressure (ICP) concerns based on clinical signs.

    Args:
        gcs: Glasgow Coma Scale score (3-15).
        pupil_reactivity: Pupil reactivity ('brisk', 'sluggish', 'fixed', 'unilateral_fixed').
        blood_pressure: Blood pressure reading (e.g., '160/90').
        vomiting: Whether patient has projectile vomiting.
        headache_severity: Headache severity (0-10).
        papilledema: Whether papilledema is present on fundoscopy.
        focal_deficits: List of focal neurological deficits.

    Returns:
        dict: ICP assessment with urgency level and recommendations.
    """
    icp_concern_score = 0
    warning_signs = []

    # GCS contribution
    if gcs <= 8:
        icp_concern_score += 4
        warning_signs.append(f"Critical: GCS ≤ 8 ({gcs}) - airway protection needed")
    elif gcs <= 12:
        icp_concern_score += 3
        warning_signs.append(f"GCS 9-12 ({gcs}) - significant impairment")
    elif gcs <= 14:
        icp_concern_score += 1
        warning_signs.append(f"GCS < 15 ({gcs}) - mild impairment")

    # Pupil reactivity
    if pupil_reactivity == "fixed":
        icp_concern_score += 4
        warning_signs.append("CRITICAL: Bilateral fixed pupils - imminent herniation")
    elif pupil_reactivity == "unilateral_fixed":
        icp_concern_score += 3
        warning_signs.append("URGENT: Unilateral fixed pupil - uncal herniation sign")
    elif pupil_reactivity == "sluggish":
        icp_concern_score += 2
        warning_signs.append("Sluggish pupil reactivity")

    # Cushing's triad assessment
    try:
        systolic, diastolic = map(int, blood_pressure.split("/"))
        if systolic >= 180 and systolic - diastolic >= 80:
            icp_concern_score += 3
            warning_signs.append("Cushing's response: Hypertension with wide pulse pressure")
        elif systolic >= 160:
            icp_concern_score += 1
            warning_signs.append("Elevated blood pressure")
    except:
        pass

    # Other signs
    if papilledema:
        icp_concern_score += 2
        warning_signs.append("Papilledema present - chronic ICP elevation")
    if vomiting:
        icp_concern_score += 1
        warning_signs.append("Vomiting (may indicate ICP)")
    if headache_severity >= 8:
        icp_concern_score += 1
        warning_signs.append(f"Severe headache ({headache_severity}/10)")

    if focal_deficits:
        icp_concern_score += len(focal_deficits)
        warning_signs.append(f"Focal deficits: {', '.join(focal_deficits)}")

    # Urgency classification
    if icp_concern_score >= 8 or gcs <= 8 or pupil_reactivity in ["fixed", "unilateral_fixed"]:
        urgency = "EMERGENT"
        recommendation = "IMMEDIATE neurosurgery consultation and CT head without contrast"
        actions = [
            "Airway protection if GCS ≤ 8",
            "Elevate head of bed 30°",
            "Mannitol 0.25-1 g/kg IV or hypertonic saline 3% if signs of herniation",
            "Urgent CT head",
            "Neurosurgery consultation STAT",
            "Prepare for possible ICP monitor or EVD placement",
        ]
    elif icp_concern_score >= 5:
        urgency = "URGENT"
        recommendation = "Urgent CT head and neurosurgery consultation"
        actions = [
            "CT head without contrast",
            "Neurological monitoring every hour",
            "Elevate head of bed 30°",
            "Neurosurgery consultation",
        ]
    else:
        urgency = "MODERATE"
        recommendation = "CT head and close monitoring"
        actions = [
            "CT head to rule out mass lesion",
            "Neurological monitoring every 2-4 hours",
            "Consider lumbar puncture if CT negative and ICP concern persists",
        ]

    return {
        "status": "assessed",
        "gcs": gcs,
        "icp_concern_score": icp_concern_score,
        "urgency": urgency,
        "warning_signs": warning_signs,
        "recommendation": recommendation,
        "immediate_actions": actions,
        "clinical_signs": {
            "pupil_reactivity": pupil_reactivity,
            "papilledema": papilledema,
            "vomiting": vomiting,
            "headache_severity": headache_severity,
            "focal_deficits": focal_deficits or "None",
        },
    }


def spinal_cord_injury_assessment(
    level: str,
    completeness: str,
    motor_score_upper: int,
    motor_score_lower: int,
    sensory_intact: bool,
    bowel_bladder_function: str,
    mechanism: str,
) -> dict:
    """Assesses spinal cord injury and provides classification and management guidance.

    Args:
        level: Level of injury (e.g., 'C5', 'T10', 'L1').
        completeness: Completeness of injury ('complete', 'incomplete').
        motor_score_upper: Motor score for upper extremities (0-5 per side, max 50).
        motor_score_lower: Motor score for lower extremities (0-5 per side, max 50).
        sensory_intact: Whether sensory function is intact at the level.
        bowel_bladder_function: Bowel/bladder function ('normal', 'impaired', 'absent').
        mechanism: Mechanism of injury (e.g., 'trauma', 'tumor', 'degenerative').

    Returns:
        dict: Spinal cord injury classification with prognosis and management.
    """
    # ASIA Impairment Scale determination
    if completeness.lower() == "complete":
        asia_grade = "A - Complete"
        asia_description = "No motor or sensory function preserved below injury level"
    elif motor_score_lower == 0 and sensory_intact:
        asia_grade = "B - Sensory Incomplete"
        asia_description = "Sensory but no motor function preserved below injury"
    elif motor_score_lower > 0 and motor_score_lower < 25:
        asia_grade = "C - Motor Incomplete"
        asia_description = "Motor function preserved below injury, most muscles < grade 3"
    elif motor_score_lower >= 25 and motor_score_lower < 50:
        asia_grade = "D - Motor Incomplete"
        asia_description = "Motor function preserved, most muscles ≥ grade 3"
    else:
        asia_grade = "E - Normal"
        asia_description = "Normal motor and sensory function"

    # Functional implications based on level
    level_upper = level.upper()
    functional_status = {}

    if level_upper.startswith("C"):
        if level_upper in ["C1", "C2", "C3"]:
            functional_status = {
                "ventilator": "Likely ventilator-dependent",
                "mobility": "Power wheelchair with chin/head controls",
                "self_care": "Total assistance needed",
            }
        elif level_upper in ["C4", "C5"]:
            functional_status = {
                "ventilator": "May or may not need ventilator",
                "mobility": "Power wheelchair",
                "self_care": "Assistance with most ADLs",
            }
        elif level_upper in ["C6", "C7", "C8"]:
            functional_status = {
                "ventilator": "Independent breathing",
                "mobility": "Manual wheelchair possible",
                "self_care": "Independent with adaptations",
            }
    elif level_upper.startswith("T"):
        functional_status = {
            "ventilator": "Independent breathing",
            "mobility": "Manual wheelchair",
            "self_care": "Independent with ADLs",
            "standing": "Standing frame or braces possible",
        }
    elif level_upper.startswith("L") or level_upper.startswith("S"):
        functional_status = {
            "ventilator": "Independent breathing",
            "mobility": "Ambulation possible with aids",
            "self_care": "Independent",
        }

    # Autonomic dysreflexia risk
    autonomic_dysreflexia_risk = level_upper[0] in ["C", "T"] and int(level_upper[1] if level_upper[1:].isdigit() else 6) <= 6

    # Management priorities
    immediate_management = [
        "Spinal immobilization (cervical collar, log-roll precautions)",
        "High-dose steroids if within 8 hours of traumatic injury (controversial)",
        "MRI spine to characterize injury",
        "Neurosurgery/Orthopedic spine consultation",
        "Maintenance of mean arterial pressure ≥ 85 mmHg",
    ]

    if autonomic_dysreflexia_risk:
        immediate_management.append("Educate on autonomic dysreflexia signs and emergency response")

    # Bowel/bladder management
    bladder_management = {
        "normal": "No intervention needed",
        "impaired": "Intermittent catheterization or bladder training",
        "absent": "Indwelling catheter or intermittent catheterization program",
    }

    return {
        "status": "assessed",
        "injury_level": level.upper(),
        "asia_grade": asia_grade,
        "asia_description": asia_description,
        "mechanism": mechanism,
        "motor_scores": {
            "upper_extremity": f"{motor_score_upper}/50",
            "lower_extremity": f"{motor_score_lower}/50",
        },
        "bowel_bladder_function": bowel_bladder_function,
        "bladder_management": bladder_management.get(bowel_bladder_function, "Urology consultation"),
        "functional_expectations": functional_status,
        "autonomic_dysreflexia_risk": autonomic_dysreflexia_risk,
        "autonomic_dysreflexia_warning": "Monitor for severe headache, hypertension, bradycardia - emergency if T6 or above" if autonomic_dysreflexia_risk else "Low risk",
        "immediate_management": immediate_management,
        "rehabilitation_needs": [
            "Physical therapy",
            "Occupational therapy",
            "Bowel and bladder training",
            "Psychological support",
            "Vocational rehabilitation",
        ],
    }