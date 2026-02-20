"""Discharge planning tools for patient discharge process."""

from datetime import datetime, timedelta
from typing import Optional

# ── In-memory state ───────────────────────────────────────────────────────────
_DISCHARGE_SUMMARY_LOG: dict[str, list[dict]] = {}  # patient_id → discharge summaries
_GP_LETTER_LOG: dict[str, list[dict]] = {}  # patient_id → GP letters sent
_COMMUNITY_REFERRAL_LOG: dict[str, list[dict]] = {}  # patient_id → community referrals
_DISCHARGE_SEQ: dict[str, int] = {"n": 0}  # auto-increment for discharge IDs

# ── Community services ───────────────────────────────────────────────────────
_COMMUNITY_SERVICES = {
    "district_nursing": {
        "service": "District Nursing",
        "description": "Wound care, medication administration, chronic disease monitoring",
        "referral_required": True,
        "typical_duration": "Until patient self-manages",
    },
    "physiotherapy": {
        "service": "Physiotherapy",
        "description": "Mobility rehabilitation, post-operative exercises, falls prevention",
        "referral_required": True,
        "typical_duration": "6-12 sessions",
    },
    "occupational_therapy": {
        "service": "Occupational Therapy",
        "description": "ADL assessment, home modifications, equipment provision",
        "referral_required": True,
        "typical_duration": "2-6 sessions + equipment",
    },
    "social_work": {
        "service": "Social Work",
        "description": "Care package assessment, safeguarding, benefits advice, placement",
        "referral_required": True,
        "typical_duration": "Until social situation stable",
    },
    "palliative_care": {
        "service": "Palliative Care",
        "description": "Symptom management, end-of-life care, family support",
        "referral_required": True,
        "typical_duration": "Ongoing",
    },
    "mental_health_community": {
        "service": "Mental Health Community Team",
        "description": "Psychiatric follow-up, medication monitoring, crisis support",
        "referral_required": True,
        "typical_duration": "3-12 months",
    },
    "dietitian": {
        "service": "Community Dietitian",
        "description": "Nutritional advice, enteral feeding, weight management",
        "referral_required": True,
        "typical_duration": "2-8 sessions",
    },
    "podiatry": {
        "service": "Podiatry",
        "description": "Foot care, diabetic foot monitoring, nail care",
        "referral_required": True,
        "typical_duration": "Ongoing for high-risk",
    },
    "speech_therapy": {
        "service": "Speech & Language Therapy",
        "description": "Dysphagia assessment, communication aids, post-stroke therapy",
        "referral_required": True,
        "typical_duration": "6-12 sessions",
    },
}


def _get_patient_info(patient_id: str) -> dict:
    """Fetch basic patient info."""
    from .common_tools import _PATIENT_DB
    patient = _PATIENT_DB.get(patient_id, {})
    return {
        "name": patient.get("name", "Unknown"),
        "age": patient.get("age"),
        "gender": patient.get("gender"),
        "address": patient.get("address", ""),
        "phone": patient.get("phone", ""),
        "emergency_contact": patient.get("emergency_contact", ""),
    }


def check_discharge_criteria(
    patient_id: str,
    clinical_criteria: dict,
) -> dict:
    """Validates if patient meets clinical discharge criteria.

    Checks key clinical indicators to determine if patient is safe for discharge.

    Args:
        patient_id: Patient identifier.
        clinical_criteria: Dict containing:
            - haemodynamically_stable: bool
            - pain_controlled: bool
            - mobile_safe: bool (can mobilize safely)
            - tolerating_oral: bool (able to eat/drink)
            - wound_dressing_safe: bool
            - home_support_adequate: bool
            - patient_informed: bool
            - follow_up_arranged: bool

    Returns:
        dict: Discharge readiness assessment with criteria results.
    """
    criteria_results = {}
    passed = 0
    total = len(clinical_criteria)

    criteria_definitions = {
        "haemodynamically_stable": {
            "label": "Haemodynamically Stable",
            "description": "BP, HR, temp within acceptable ranges",
        },
        "pain_controlled": {
            "label": "Pain Controlled",
            "description": "Pain score ≤3 or patient satisfied with pain management",
        },
        "mobile_safe": {
            "label": "Safe to Mobilise",
            "description": "Patient can walk safely with/without aids",
        },
        "tolerating_oral": {
            "label": "Tolerating Oral Intake",
            "description": "Able to eat and drink without nausea/vomiting",
        },
        "wound_dressing_safe": {
            "label": "Wound/Dressing Safe",
            "description": "Wounds healing or district nurse arranged",
        },
        "home_support_adequate": {
            "label": "Adequate Home Support",
            "description": "Family/carer available or care package in place",
        },
        "patient_informed": {
            "label": "Patient Informed",
            "description": "Discharge plan discussed with patient",
        },
        "follow_up_arranged": {
            "label": "Follow-up Arranged",
            "description": "Outpatient appointment or GP follow-up booked",
        },
    }

    for key, value in clinical_criteria.items():
        criteria_results[key] = {
            "passed": bool(value),
            **criteria_definitions.get(key, {"label": key, "description": ""}),
        }
        if value:
            passed += 1

    readiness_score = (passed / total) * 100 if total > 0 else 0

    if readiness_score == 100:
        status = "ready"
        recommendation = "All criteria met — patient is ready for discharge."
    elif readiness_score >= 75:
        status = "mostly_ready"
        recommendation = "Most criteria met — address outstanding items before discharge."
    elif readiness_score >= 50:
        status = "partial"
        recommendation = "Several criteria pending — discharge planning should continue."
    else:
        status = "not_ready"
        recommendation = "Discharge criteria not met — continue inpatient care."

    return {
        "status": status,
        "patient_id": patient_id,
        "readiness_score": round(readiness_score, 1),
        "criteria_passed": passed,
        "criteria_total": total,
        "criteria_results": criteria_results,
        "recommendation": recommendation,
        "outstanding_items": [
            criteria_results[k]["label"] 
            for k, v in clinical_criteria.items() 
            if not v
        ],
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def generate_discharge_summary(
    patient_id: str,
    admitting_diagnosis: str,
    final_diagnosis: str,
    investigations: list[str],
    treatment: list[str],
    tta_medications: list[dict],
    follow_up_plan: str,
    clinical_course: str = "",
    complications: str = "",
    discharge_condition: str = "stable",
) -> dict:
    """Generates a structured discharge summary.

    Creates a comprehensive discharge summary document covering admission details,
    clinical course, investigations, treatment, and follow-up plan.

    Args:
        patient_id: Patient identifier.
        admitting_diagnosis: Initial diagnosis at admission.
        final_diagnosis: Final diagnosis at discharge.
        investigations: List of investigations performed.
        treatment: List of treatments/ procedures performed.
        tta_medications: List of TTA medications with dose/frequency.
        follow_up_plan: Follow-up plan description.
        clinical_course: Brief summary of hospital stay.
        complications: Any complications during admission.
        discharge_condition: Condition at discharge (stable/improved/unchanged/deteriorated).

    Returns:
        dict: Complete discharge summary document.
    """
    _DISCHARGE_SEQ["n"] += 1
    now = datetime.now()
    summary_id = f"DS-{now.strftime('%Y%m%d')}-{_DISCHARGE_SEQ['n']:04d}"

    patient_info = _get_patient_info(patient_id)

    summary = {
        "summary_id": summary_id,
        "patient_id": patient_id,
        "patient_name": patient_info["name"],
        "date_of_birth": patient_info.get("dob", "N/A"),
        "date_admitted": (now - timedelta(days=3)).strftime("%Y-%m-%d"),  # Mock
        "date_discharged": now.strftime("%Y-%m-%d"),
        "admitting_diagnosis": admitting_diagnosis,
        "final_diagnosis": final_diagnosis,
        "clinical_course": clinical_course or f"Patient admitted with {admitting_diagnosis}. Received {', '.join(treatment)}. Discharged in {discharge_condition} condition.",
        "investigations_performed": investigations,
        "treatment_provided": treatment,
        "complications": complications or "None",
        "discharge_condition": discharge_condition,
        "tta_medications": tta_medications,
        "follow_up_plan": follow_up_plan,
        "discharge_advice": [
            "Rest for the first 24-48 hours",
            "Gradually resume normal activities as tolerated",
            "Take medications as prescribed",
            "Attend all follow-up appointments",
            "Contact GP or return to hospital if symptoms worsen",
        ],
        "generated_at": now.strftime("%Y-%m-%d %H:%M"),
    }

    _DISCHARGE_SUMMARY_LOG.setdefault(patient_id, []).append(summary)

    return {
        "status": "generated",
        "summary_id": summary_id,
        "patient_id": patient_id,
        "discharge_summary": summary,
        "message": f"Discharge summary {summary_id} generated successfully.",
    }


def send_gp_letter(
    patient_id: str,
    gp_name: str,
    summary: dict,
    urgent_actions: str = "",
) -> dict:
    """Generates and 'sends' a discharge letter to the GP.

    Creates a structured GP letter summarizing the admission for primary care.

    Args:
        patient_id: Patient identifier.
        gp_name: Name of the GP/medical practice.
        summary: The discharge summary dict from generate_discharge_summary.
        urgent_actions: Any urgent actions required from GP.

    Returns:
        dict: GP letter with confirmation.
    """
    _DISCHARGE_SEQ["n"] += 1
    now = datetime.now()
    letter_id = f"GPL-{now.strftime('%Y%m%d')}-{_DISCHARGE_SEQ['n']:04d}"

    patient_info = _get_patient_info(patient_id)

    gp_letter = {
        "letter_id": letter_id,
        "patient_id": patient_id,
        "patient_name": patient_info["name"],
        "date_of_birth": patient_info.get("dob", "N/A"),
        "address": patient_info.get("address", ""),
        "date": now.strftime("%Y-%m-%d"),
        "recipient": gp_name,
        "re": f"Discharge Summary - {summary.get('final_diagnosis', 'N/A')}",
        "admission_summary": {
            "date_admitted": summary.get("date_admitted"),
            "date_discharged": summary.get("date_discharged"),
            "admitting_diagnosis": summary.get("admitting_diagnosis"),
            "final_diagnosis": summary.get("final_diagnosis"),
            "clinical_course": summary.get("clinical_course"),
            "discharge_condition": summary.get("discharge_condition"),
        },
        "investigations": summary.get("investigations_performed", []),
        "treatment": summary.get("treatment_provided", []),
        "medications": summary.get("tta_medications", []),
        "follow_up": summary.get("follow_up_plan"),
        "urgent_actions": urgent_actions or "None",
        "generated_at": now.strftime("%Y-%m-%d %H:%M"),
    }

    _GP_LETTER_LOG.setdefault(patient_id, []).append(gp_letter)

    return {
        "status": "sent",
        "letter_id": letter_id,
        "patient_id": patient_id,
        "gp_name": gp_name,
        "message": f"GP letter {letter_id} generated and sent to {gp_name}.",
        "urgent_actions": urgent_actions,
    }


def arrange_community_services(
    patient_id: str,
    services_required: list[str],
    clinical_reason: str = "",
    urgency: str = "routine",
) -> dict:
    """Refers patient to community health services.

    Creates referrals to district nursing, physiotherapy, OT, social work, etc.

    Args:
        patient_id: Patient identifier.
        services_required: List of service codes:
            - district_nursing, physiotherapy, occupational_therapy
            - social_work, palliative_care, mental_health_community
            - dietitian, podiatry, speech_therapy
        clinical_reason: Clinical reason for referral.
        urgency: "routine", "urgent", or "emergency".

    Returns:
        dict: Referral confirmation with service details.
    """
    patient_info = _get_patient_info(patient_id)

    referrals = []
    for service_code in services_required:
        service = _COMMUNITY_SERVICES.get(service_code)
        if not service:
            continue

        _DISCHARGE_SEQ["n"] += 1

        referral = {
            "referral_id": f"REF-{datetime.now().strftime('%Y%m%d')}-{_DISCHARGE_SEQ['n']:04d}",
            "patient_id": patient_id,
            "patient_name": patient_info["name"],
            "patient_address": patient_info.get("address", ""),
            "patient_phone": patient_info.get("phone", ""),
            "service_code": service_code,
            **service,
            "clinical_reason": clinical_reason or f"Post-discharge care following hospitalization",
            "urgency": urgency,
            "status": "referred",
            "referral_date": datetime.now().strftime("%Y-%m-%d"),
        }
        referrals.append(referral)

    _COMMUNITY_REFERRAL_LOG.setdefault(patient_id, []).extend(referrals)

    urgency_timeline = {
        "routine": "within 2-4 weeks",
        "urgent": "within 5-7 days",
        "emergency": "within 24-48 hours",
    }

    return {
        "status": "referred",
        "patient_id": patient_id,
        "referral_count": len(referrals),
        "referrals": referrals,
        "timeline": urgency_timeline.get(urgency, "within 2-4 weeks"),
        "message": f"{len(referrals)} community service referral(s) created for {patient_info['name']}.",
    }
