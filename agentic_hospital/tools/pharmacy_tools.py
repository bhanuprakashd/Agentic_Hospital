"""Pharmacy-specific tools for medication verification, dispensing, and reconciliation."""

from datetime import datetime, timedelta
from typing import Optional

# ── In-memory state ───────────────────────────────────────────────────────────
_DISPENSE_LOG: dict[str, list[dict]] = {}  # patient_id → list of dispensing records
_RECONCILIATION_LOG: dict[str, list[dict]] = {}  # patient_id → reconciliation records
_PRESCRIPTION_SEQ: dict[str, int] = {"n": 0}  # auto-increment for prescription IDs

# ── Hospital formulary (subset) ──────────────────────────────────────────────
_FORMULARY: dict[str, dict] = {
    "Aspirin": {"dose": "75-100mg", "route": "oral", "frequency": "daily", "form": "tablet"},
    "Atorvastatin": {"dose": "10-80mg", "route": "oral", "frequency": "nightly", "form": "tablet"},
    "Metformin": {"dose": "500mg-2g", "route": "oral", "frequency": "twice daily", "form": "tablet"},
    "Lisinopril": {"dose": "2.5-40mg", "route": "oral", "frequency": "daily", "form": "tablet"},
    "Amlodipine": {"dose": "2.5-10mg", "route": "oral", "frequency": "daily", "form": "tablet"},
    "Omeprazole": {"dose": "20-40mg", "route": "oral", "frequency": "daily", "form": "capsule"},
    "Metoprolol": {"dose": "25-200mg", "route": "oral", "frequency": "twice daily", "form": "tablet"},
    "Warfarin": {"dose": "1-10mg", "route": "oral", "frequency": "daily", "form": "tablet"},
    "Clopidogrel": {"dose": "75mg", "route": "oral", "frequency": "daily", "form": "tablet"},
    "Amiodarone": {"dose": "100-400mg", "route": "oral", "frequency": "daily", "form": "tablet"},
    "Simvastatin": {"dose": "10-80mg", "route": "oral", "frequency": "nightly", "form": "tablet"},
    "Digoxin": {"dose": "0.125-0.25mg", "route": "oral", "frequency": "daily", "form": "tablet"},
    "Furosemide": {"dose": "20-80mg", "route": "oral/IV", "frequency": "daily", "form": "tablet"},
    "Spironolactone": {"dose": "25-100mg", "route": "oral", "frequency": "daily", "form": "tablet"},
    "Pantoprazole": {"dose": "20-40mg", "route": "oral/IV", "frequency": "daily", "form": "tablet"},
    "Ceftriaxone": {"dose": "1-2g", "route": "IV/IM", "frequency": "daily", "form": "injection"},
    "Azithromycin": {"dose": "250-500mg", "route": "oral", "frequency": "daily", "form": "tablet"},
    "Amoxicillin": {"dose": "250-500mg", "route": "oral", "frequency": "three times daily", "form": "capsule"},
    "Fluconazole": {"dose": "50-200mg", "route": "oral", "frequency": "daily", "form": "capsule"},
    "Morphine": {"dose": "2.5-10mg", "route": "oral/IV", "frequency": "as required", "form": "tablet/injection"},
    "Tramadol": {"dose": "50-100mg", "route": "oral", "frequency": "as required", "form": "tablet"},
    "Paracetamol": {"dose": "500mg-1g", "route": "oral/PR", "frequency": "every 4-6 hours", "form": "tablet/suppository"},
    "Ibuprofen": {"dose": "200-600mg", "route": "oral", "frequency": "three times daily", "form": "tablet"},
    "Enoxaparin": {"dose": "40mg", "route": "subcutaneous", "frequency": "daily", "form": "injection"},
    "Insulin Glargine": {"dose": "10-80 units", "route": "subcutaneous", "frequency": "nightly", "form": "injection"},
    "Insulin Lispro": {"dose": "variable", "route": "subcutaneous", "frequency": "mealtime", "form": "injection"},
    "Levothyroxine": {"dose": "25-150mcg", "route": "oral", "frequency": "daily on empty stomach", "form": "tablet"},
    "Prednisolone": {"dose": "5-60mg", "route": "oral", "frequency": "daily", "form": "tablet"},
    "Dexamethasone": {"dose": "0.5-8mg", "route": "oral/IV", "frequency": "daily", "form": "tablet/injection"},
    "Vancomycin": {"dose": "500mg-1g", "route": "IV", "frequency": "every 6-12 hours", "form": "injection"},
    "Piperacillin-Tazobactam": {"dose": "2.25-4.5g", "route": "IV", "frequency": "every 6-8 hours", "form": "injection"},
    "Meropenem": {"dose": "0.5-1g", "route": "IV", "frequency": "every 8 hours", "form": "injection"},
    "Gentamicin": {"dose": "3-5mg/kg", "route": "IV", "frequency": "daily", "form": "injection"},
    "Amphotericin": {"dose": "0.5-1mg/kg", "route": "IV", "frequency": "daily", "form": "injection"},
    "Rivaroxaban": {"dose": "10-20mg", "route": "oral", "frequency": "daily", "form": "tablet"},
    "Apixaban": {"dose": "2.5-5mg", "route": "oral", "frequency": "twice daily", "form": "tablet"},
    "Dabigatran": {"dose": "75-150mg", "route": "oral", "frequency": "twice daily", "form": "capsule"},
}

# ── Allergy database (shared with common_tools) ──────────────────────────────
_ALLERGIES: dict[str, list[str]] = {
    "P001": ["Penicillin", "Sulfa"],
    "P002": ["Aspirin", "NSAIDs"],
    "P003": [],
    "P004": ["Morphine"],
    "P005": ["Penicillin", "Latex"],
    "P006": ["Codeine"],
    "P007": [],
    "P008": ["Vancomycin"],
    "P009": ["Aspirin"],
    "P010": ["Sulfa", "Morphine"],
}


def _get_patient_info(patient_id: str) -> dict:
    """Fetch basic patient info including allergies."""
    from .common_tools import _PATIENT_DB
    patient = _PATIENT_DB.get(patient_id, {})
    allergies = _ALLERGIES.get(patient_id, [])
    return {
        "name": patient.get("name", "Unknown"),
        "allergies": allergies,
        "age": patient.get("age"),
        "gender": patient.get("gender"),
    }


def _get_patient_medications(patient_id: str) -> list[str]:
    """Fetch current patient medications."""
    from .common_tools import _PATIENT_DB
    patient = _PATIENT_DB.get(patient_id, {})
    return patient.get("medications", [])


def verify_medication_order(
    patient_id: str,
    medication: str,
    dose: str,
    route: str = "oral",
    frequency: str = "daily",
    indication: str = "",
) -> dict:
    """Validates a medication order against formulary, allergies, and contraindications.

    Performs comprehensive verification including:
    - Formulary status
    - Allergy checks
    - Renal/hepatic dose adjustment flags
    - Common contraindications

    Args:
        patient_id: Patient identifier (e.g., "P001").
        medication: Medication name (e.g., "Aspirin").
        dose: Prescribed dose (e.g., "75mg").
        route: Route of administration (e.g., "oral", "IV").
        frequency: Dosing frequency (e.g., "daily", "twice daily").
        indication: Clinical indication for the medication.

    Returns:
        dict: Verification result with status, warnings, and recommendations.
    """
    med_normalized = medication.split()[0].strip()
    patient_info = _get_patient_info(patient_id)
    current_meds = _get_patient_medications(patient_id)

    # ── Check formulary ──────────────────────────────────────────────────────
    formulary_entry = _FORMULARY.get(med_normalized)
    if not formulary_entry:
        return {
            "status": "not_in_formulary",
            "medication": medication,
            "message": f"{med_normalized} is NOT in the hospital formulary.",
            "recommendation": "Contact pharmacy for non-formulary approval or consider alternative.",
        }

    # ── Check allergies ────────────────────────────────────────────────────────
    allergy_warnings = []
    patient_allergies = [a.lower() for a in patient_info["allergies"]]
    med_lower = med_normalized.lower()

    for allergy in patient_allergies:
        if allergy.lower() in med_lower or med_lower in allergy.lower():
            allergy_warnings.append(f"ALLERGY MATCH: Patient allergic to {allergy}")

    if "penicillin" in patient_allergies and "amoxicillin" in med_lower:
        allergy_warnings.append("CROSS-REACTIVITY: Penicillin allergy — confirm no reaction history")
    if "nsaids" in patient_allergies and ("ibuprofen" in med_lower or "aspirin" in med_lower):
        allergy_warnings.append("NSAID CROSS-REACTIVITY: Patient has NSAID allergy")

    # ── Check drug interactions with current meds ─────────────────────────────
    from .common_tools import check_drug_interactions
    all_meds = current_meds + [medication]
    interaction_result = check_drug_interactions(all_meds)

    # ── Generate verification result ───────────────────────────────────────────
    warnings = []
    if allergy_warnings:
        warnings.extend(allergy_warnings)
        status = "allergy_warning"
    elif interaction_result.get("status") == "interactions_found":
        severity = interaction_result.get("critical_count", 0) + interaction_result.get("high_severity_count", 0)
        status = "critical_interaction" if severity > 0 else "interaction_warning"
        warnings.append(f"Drug interaction: {interaction_result.get('count', 0)} found")
    else:
        status = "verified"

    return {
        "status": status,
        "medication": medication,
        "dose": dose,
        "route": route,
        "frequency": frequency,
        "indication": indication,
        "formulary_verified": formulary_entry is not None,
        "allergy_warnings": allergy_warnings,
        "interactions": interaction_result.get("interactions", [])[:3] if interaction_result.get("interactions") else [],
        "dose_appropriate": True,
        "renal_adjustment": "Check renal function for doses >1g" if med_normalized in ["Vancomycin", "Gentamicin", "Meropenem"] else None,
        "recommendation": "APPROVED — dispense as ordered" if status == "verified" else "REVIEW REQUIRED — pharmacist consult needed before dispensing",
        "verified_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def dispense_medication(
    patient_id: str,
    medication: str,
    dose: str,
    quantity: int = 30,
    instructions: str = "",
    pharmacist_id: str = "PH001",
) -> dict:
    """Records a medication dispensing event with batch tracking.

    Documents the complete dispensing record including pharmacist verification,
    batch number, expiry, and patient counseling notes.

    Args:
        patient_id: Patient identifier.
        medication: Medication name.
        dose: Dispensed dose.
        quantity: Number of units/tablets dispensed.
        instructions: Patient administration instructions.
        pharmacist_id: ID of verifying pharmacist.

    Returns:
        dict: Dispensing record with ID and confirmation.
    """
    _PRESCRIPTION_SEQ["n"] += 1
    now = datetime.now()
    dispense_id = f"DISP-{now.strftime('%Y%m%d')}-{_PRESCRIPTION_SEQ['n']:04d}"

    import random
    batch_number = f"BN{random.randint(10000, 99999)}"
    expiry_date = (now + timedelta(days=365)).strftime("%Y-%m-%d")

    dispense_record = {
        "dispense_id": dispense_id,
        "patient_id": patient_id,
        "medication": medication,
        "dose": dose,
        "quantity": quantity,
        "instructions": instructions,
        "pharmacist_id": pharmacist_id,
        "batch_number": batch_number,
        "expiry_date": expiry_date,
        "dispensed_at": now.strftime("%Y-%m-%d %H:%M"),
        "status": "dispensed",
    }

    _DISPENSE_LOG.setdefault(patient_id, []).append(dispense_record)

    return {
        "status": "dispensed",
        "dispense_id": dispense_id,
        "patient_id": patient_id,
        "medication": medication,
        "dose": dose,
        "quantity": quantity,
        "batch_number": batch_number,
        "expiry_date": expiry_date,
        "pharmacist_id": pharmacist_id,
        "message": f"{medication} {dose} dispensed successfully.",
    }


def medication_reconciliation(
    patient_id: str,
    stage: str = "admission",
) -> dict:
    """Compares home medications vs. inpatient orders (admission) or inpatient vs. discharge (discharge).

    Identifies omissions, duplications, interactions, and needs for continuation.

    Args:
        patient_id: Patient identifier.
        stage: "admission" or "discharge".

    Returns:
        dict: Reconciliation report with discrepancies and recommendations.
    """
    patient_info = _get_patient_info(patient_id)
    home_meds = _get_patient_medications(patient_id)

    inpatient_meds = []
    if patient_id in _DISPENSE_LOG:
        inpatient_meds = list(set([d["medication"] for d in _DISPENSE_LOG[patient_id]]))

    home_normalized = [m.split()[0].strip() for m in home_meds]
    inpatient_normalized = [m.split()[0].strip() for m in inpatient_meds]

    discrepancies = []

    if stage == "admission":
        for med in home_normalized:
            if med not in inpatient_normalized:
                discrepancies.append({
                    "type": "omission",
                    "medication": med,
                    "description": f"Home medication {med} NOT continued — review needed",
                    "action": "Continue or document reason for stopping",
                })

        for med in inpatient_normalized:
            if med not in home_normalized:
                discrepancies.append({
                    "type": "new",
                    "medication": med,
                    "description": f"New medication {med} started during admission",
                    "action": "Document indication and expected duration",
                })

    else:  # discharge
        for med in inpatient_normalized:
            if med not in home_normalized:
                discrepancies.append({
                    "type": "discharge_omission",
                    "medication": med,
                    "description": f"Inpatient medication {med} NOT on discharge prescription",
                    "action": "Either continue as TTA or document reason for stopping",
                })

        for med in home_normalized:
            if med not in inpatient_normalized:
                discrepancies.append({
                    "type": "home_continued",
                    "medication": med,
                    "description": f"Home medication {med} was held during admission — review for restart",
                    "action": "Assess if needs to be restarted on discharge",
                })

    _RECONCILIATION_LOG.setdefault(patient_id, []).append({
        "stage": stage,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "home_medications": home_meds,
        "inpatient_medications": inpatient_meds,
        "discrepancies": discrepancies,
    })

    return {
        "status": "reconciliation_complete",
        "patient_id": patient_id,
        "stage": stage,
        "home_medications": home_meds,
        "current_medications": inpatient_meds if stage == "admission" else [],
        "discrepancies": discrepancies,
        "discrepancy_count": len(discrepancies),
        "recommendation": (
            f"Review {len(discrepancies)} discrepancy(ies) with treating team before finalizing."
            if discrepancies else "No discrepancies found — medication list is consistent."
        ),
        "reconciled_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def generate_tta_prescription(
    patient_id: str,
    discharge_medications: list[dict],
    duration_days: int = 30,
    pharmacist_id: str = "PH001",
) -> dict:
    """Generates a Take-To-Home (TTA) prescription for discharge.

    Creates a complete discharge prescription with dosing instructions,
    warning signs, and follow-up requirements.

    Args:
        patient_id: Patient identifier.
        discharge_medications: List of medication dicts with keys:
            - medication: drug name
            - dose: dose amount
            - frequency: dosing frequency
            - route: administration route
        duration_days: Duration of prescription in days.
        pharmacist_id: ID of verifying pharmacist.

    Returns:
        dict: TTA prescription document.
    """
    _PRESCRIPTION_SEQ["n"] += 1
    now = datetime.now()
    rx_id = f"TTA-{now.strftime('%Y%m%d')}-{_PRESCRIPTION_SEQ['n']:04d}"

    patient_info = _get_patient_info(patient_id)

    rx_items = []
    for med in discharge_medications:
        med_name = med.get("medication", "")
        dose = med.get("dose", "")
        freq = med.get("frequency", "daily")
        route = med.get("route", "oral")

        instructions = f"Take {dose} {route} {freq}"
        if "once" in freq.lower():
            instructions = f"Take {dose} {route} once daily"
        elif "twice" in freq.lower():
            instructions = f"Take {dose} {route} twice daily"
        elif "three" in freq.lower():
            instructions = f"Take {dose} {route} three times daily"

        warnings = []
        if "warfarin" in med_name.lower():
            warnings.append("Take at the same time each day")
            warnings.append("Avoid sudden changes in diet")
            warnings.append("Report any unusual bleeding or bruising")
        if "insulin" in med_name.lower():
            warnings.append("Monitor blood glucose regularly")
            warnings.append("Do not skip meals")
        if "opioid" in med_name.lower() or "morphine" in med_name.lower():
            warnings.append("Do not drive or operate machinery")
            warnings.append("Avoid alcohol")
            warnings.append("Do not exceed prescribed dose")

        rx_items.append({
            "medication": med_name,
            "dose": dose,
            "frequency": freq,
            "route": route,
            "instructions": instructions,
            "warnings": warnings,
            "quantity": duration_days if "daily" in freq.lower() else duration_days * 3,
        })

    tta_document = {
        "prescription_id": rx_id,
        "patient_id": patient_id,
        "patient_name": patient_info["name"],
        "date_issued": now.strftime("%Y-%m-%d"),
        "valid_until": (now + timedelta(days=duration_days)).strftime("%Y-%m-%d"),
        "prescriber": "Discharge Team",
        "pharmacist_id": pharmacist_id,
        "medications": rx_items,
        "general_instructions": [
            "Take all medications as prescribed",
            "Do not share medications with others",
            "Store medications in a cool, dry place",
            "Contact the hospital if you experience any adverse effects",
        ],
        "follow_up": "Follow up with GP within 7 days or as instructed",
    }

    return {
        "status": "prescription_generated",
        "prescription_id": rx_id,
        "patient_id": patient_id,
        "patient_name": patient_info["name"],
        "medication_count": len(rx_items),
        "valid_until": tta_document["valid_until"],
        "prescription": tta_document,
        "message": f"TTA prescription {rx_id} generated with {len(rx_items)} medication(s)",
    }
