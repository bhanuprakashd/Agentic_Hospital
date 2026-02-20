"""Patient monitoring and critical alert tools.

Implements autonomous critical value detection against AACC (American Association
for Clinical Chemistry) critical lab value thresholds and vital sign danger zones.
"""

import datetime
from typing import Optional

# Import shared patient data
from .common_tools import _PATIENT_DB, _LAB_DB


# =============================================================================
# AACC CRITICAL VALUE THRESHOLDS
# Reference: AACC Critical Values 2022 / Joint Commission Standards
# =============================================================================
_CRITICAL_LAB_THRESHOLDS: dict[str, dict] = {
    # Electrolytes
    "Potassium":      {"low": 2.5,   "high": 6.5,  "unit": "mEq/L",    "panel": "BMP",
                       "action_low":  "IV KCl replacement; continuous cardiac monitoring; recheck in 2h",
                       "action_high": "Calcium gluconate IV; insulin + dextrose; telemetry; nephrology consult"},
    "Sodium":         {"low": 120.0, "high": 160.0, "unit": "mEq/L",    "panel": "BMP",
                       "action_low":  "Hypertonic saline if severe (<115) or symptomatic; neurology consult; correct ≤8 mEq/day to prevent osmotic demyelination",
                       "action_high": "Free water replacement; correct slowly ≤10 mEq/24h; neurology consult"},
    "Glucose":        {"low": 40.0,  "high": 500.0, "unit": "mg/dL",    "panel": "BMP",
                       "action_low":  "D50 50 mL IV stat if altered consciousness; orange juice if alert; recheck in 15 min",
                       "action_high": "Insulin protocol; hydration; investigate DKA/HHS; ABG"},
    "Calcium":        {"low": 6.5,   "high": 13.5,  "unit": "mg/dL",    "panel": "BMP",
                       "action_low":  "IV calcium gluconate 1–2 g; cardiac monitoring; recheck albumin-corrected",
                       "action_high": "IV hydration 200–300 mL/h; bisphosphonate; calcitonin; malignancy workup"},
    "Bicarbonate":    {"low": 10.0,  "high": 40.0,  "unit": "mEq/L",    "panel": "BMP",
                       "action_low":  "ABG stat; treat underlying acidosis; sodium bicarbonate if pH <7.1",
                       "action_high": "ABG stat; identify metabolic alkalosis cause; chloride replacement if hypochloremic"},
    "BUN":            {"high": 100.0, "unit": "mg/dL", "panel": "BMP",
                       "action_high": "Nephrology consult; assess for acute uremia; dialysis if BUN >100 with symptoms"},
    "Creatinine":     {"high": 10.0,  "unit": "mg/dL", "panel": "BMP",
                       "action_high": "Nephrology emergent consult; dialysis evaluation; discontinue nephrotoxic drugs"},
    # Hematology
    "Hemoglobin":     {"low": 6.0,   "high": 20.0,  "unit": "g/dL",     "panel": "CBC",
                       "action_low":  "Type and crossmatch; transfusion threshold Hgb <7 (or <8 if cardiac); identify bleeding source",
                       "action_high": "Phlebotomy if polycythemia vera; hydration; hyperviscosity workup"},
    "Platelets":      {"low": 20.0,  "high": 1000.0,"unit": "×10³/µL",  "panel": "CBC",
                       "action_low":  "Hematology consult; platelet transfusion if <10K or active bleeding; hold anticoagulants",
                       "action_high": "Hematology consult; rule out ET; aspirin for thrombocytosis if reactive"},
    "WBC":            {"low": 2.0,   "high": 30.0,  "unit": "×10³/µL",  "panel": "CBC",
                       "action_low":  "Neutropenia precautions; G-CSF consideration; bone marrow evaluation; reverse isolation",
                       "action_high": "Peripheral smear; hematology consult; blast differential; leukemia workup"},
    # Coagulation
    "INR":            {"high": 4.0,   "unit": "",     "panel": "INR",
                       "action_high": "Hold Warfarin; Vitamin K 2.5–5 mg PO (or 10 mg IV if urgent); FFP if active bleeding; hematology"},
    # Cardiac
    "BNP":            {"high": 500.0, "unit": "pg/mL","panel": "BNP",
                       "action_high": "Cardiology consult; chest X-ray; echocardiogram; optimize diuresis; loop diuretic IV"},
    # Liver
    "Total_Bilirubin":{"high": 15.0,  "unit": "mg/dL","panel": "LFTs",
                       "action_high": "GI/hepatology consult; liver failure workup; coagulation panel; acetaminophen level"},
    "ALT":            {"high": 500.0, "unit": "U/L",  "panel": "LFTs",
                       "action_high": "Hepatology consult; acetaminophen toxicity? viral hepatitis panel; discontinue hepatotoxic drugs"},
}

_CRITICAL_VITAL_THRESHOLDS = {
    "systolic_bp": {
        "critical_low":  70,  "warning_low":  90,
        "warning_high": 180,  "critical_high": 220,
        "unit": "mmHg",
        "action_low":  "Shock protocol: IV access x2, fluid challenge 500 mL, vasopressors if refractory; ICU alert",
        "action_high": "Hypertensive emergency: IV labetalol/nicardipine; reduce MAP ≤25% in first hour",
    },
    "heart_rate": {
        "critical_low":  40, "warning_low":  50,
        "warning_high": 130, "critical_high": 160,
        "unit": "bpm",
        "action_low":  "Atropine 0.5 mg IV; transcutaneous pacing if unstable; cardiology",
        "action_high": "12-lead ECG; rate control; cardioversion if hemodynamically unstable",
    },
    "spo2": {
        "critical_low": 88, "warning_low": 92,
        "unit": "%",
        "action_low":  "High-flow O2; prepare for NIV/intubation if declining; ICU alert; ABG stat",
    },
    "respiratory_rate": {
        "critical_low":  8, "warning_low": 10,
        "warning_high": 25, "critical_high": 35,
        "unit": "breaths/min",
        "action_low":  "Assess for opioid toxicity (naloxone); airway; ABG",
        "action_high": "Respiratory distress: O2; identify cause (PE, pneumonia, HF); may need NIV",
    },
    "temperature_f": {
        "critical_low":  95.0, "warning_low":  96.8,
        "warning_high": 101.3, "critical_high": 104.0,
        "unit": "°F",
        "action_low":  "Active warming: blankets, warm IV fluids; check TSH/sepsis; ICU if <94°F",
        "action_high": "Blood cultures x2; broad-spectrum antibiotics; acetaminophen; cooling measures if >40°C",
    },
}

# In-session alert log
_ALERT_LOG: list[dict] = []


# =============================================================================
# TOOL FUNCTIONS
# =============================================================================

def check_critical_lab_values(patient_id: str) -> dict:
    """Scans all available lab results for a patient against AACC critical value thresholds.

    Automatically identifies dangerous lab values that require immediate clinical action,
    ranked by severity. Call this proactively for any patient with acute illness or
    significant comorbidities.

    Args:
        patient_id: The patient identifier (P001–P010).

    Returns:
        dict: Critical and warning lab values with immediate action recommendations,
              ranked by severity. Returns 'all_clear' if no critical values found.
    """
    if patient_id not in _LAB_DB:
        return {
            "status": "not_found",
            "message": f"No lab data on file for patient '{patient_id}'.",
        }

    patient = _PATIENT_DB.get(patient_id, {})
    patient_name = patient.get("name", patient_id)
    patient_labs = _LAB_DB[patient_id]

    critical_alerts = []
    warning_alerts = []

    for panel_name, panel_data in patient_labs.items():
        if not isinstance(panel_data, dict):
            continue

        for analyte, threshold in _CRITICAL_LAB_THRESHOLDS.items():
            value = None

            # Path 1: analyte is a direct key in the panel (e.g., BMP → Glucose, Potassium)
            for k, v in panel_data.items():
                if k.lower() == analyte.lower() and isinstance(v, (int, float)):
                    value = v
                    break

            # Path 2: panel name matches analyte (single-value panels like BNP, INR, TSH)
            # stored as {"value": 890, "unit": "pg/mL", "status": "..."}
            if value is None and panel_name.lower() == analyte.lower():
                raw = panel_data.get("value")
                if isinstance(raw, (int, float)):
                    value = raw

            if value is None:
                continue

            low = threshold.get("low")
            high = threshold.get("high")
            unit = threshold.get("unit", "")

            alert_entry = {
                "analyte": analyte,
                "value": value,
                "unit": unit,
                "panel": panel_name,
                "patient_id": patient_id,
                "patient_name": patient_name,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            }

            if low is not None and value < low:
                severity = "CRITICAL" if value < low * 0.85 else "WARNING"
                alert_entry.update({
                    "direction": "LOW",
                    "threshold": f"Critical low: <{low} {unit}",
                    "severity": severity,
                    "immediate_action": threshold.get("action_low", "Notify physician immediately"),
                })
                if severity == "CRITICAL":
                    critical_alerts.append(alert_entry)
                else:
                    warning_alerts.append(alert_entry)

            elif high is not None and value > high:
                severity = "CRITICAL" if value > high * 1.15 else "WARNING"
                alert_entry.update({
                    "direction": "HIGH",
                    "threshold": f"Critical high: >{high} {unit}",
                    "severity": severity,
                    "immediate_action": threshold.get("action_high", "Notify physician immediately"),
                })
                if severity == "CRITICAL":
                    critical_alerts.append(alert_entry)
                else:
                    warning_alerts.append(alert_entry)

    # Log all alerts
    for alert in critical_alerts + warning_alerts:
        _ALERT_LOG.append(alert)

    if not critical_alerts and not warning_alerts:
        return {
            "status": "all_clear",
            "patient_id": patient_id,
            "patient_name": patient_name,
            "message": f"No critical or warning lab values detected for {patient_name}. All checked values within safe thresholds.",
            "panels_scanned": list(patient_labs.keys()),
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

    total_alerts = len(critical_alerts) + len(warning_alerts)

    return {
        "status": "alerts_found",
        "patient_id": patient_id,
        "patient_name": patient_name,
        "total_alerts": total_alerts,
        "critical_count": len(critical_alerts),
        "warning_count": len(warning_alerts),
        "critical_alerts": critical_alerts,
        "warning_alerts": warning_alerts,
        "overall_urgency": "CRITICAL — immediate physician notification required" if critical_alerts else "WARNING — timely physician review required",
        "panels_scanned": list(patient_labs.keys()),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "notification_required": True,
        "escalation_instruction": (
            f"ALERT: {patient_name} ({patient_id}) has {len(critical_alerts)} CRITICAL "
            f"and {len(warning_alerts)} WARNING lab value(s). "
            "Notify attending physician immediately. Do NOT delay treatment pending additional review."
            if critical_alerts else
            f"NOTICE: {patient_name} ({patient_id}) has {len(warning_alerts)} WARNING lab value(s). "
            "Physician review required within 1 hour."
        ),
    }


def generate_deterioration_alert(
    patient_id: str,
    trigger: str,
    value: float,
    unit: str,
    clinical_context: Optional[str] = None,
) -> dict:
    """Generates a structured clinical deterioration alert for a specific abnormal finding.

    Use when a specific vital sign or lab value crosses a danger threshold during
    a consultation. Produces an actionable, timestamped alert record.

    Args:
        patient_id: The patient identifier (P001–P010).
        trigger: The clinical parameter that triggered the alert (e.g., 'Potassium', 'systolic_bp', 'spo2').
        value: The measured value that triggered the alert.
        unit: Unit of measurement (e.g., 'mEq/L', 'mmHg', '%').
        clinical_context: Optional free-text clinical context (e.g., 'Patient on furosemide + ACEi').

    Returns:
        dict: Structured alert with severity classification, thresholds, and immediate actions.
    """
    patient = _PATIENT_DB.get(patient_id, {})
    patient_name = patient.get("name", patient_id)
    allergies = patient.get("allergies", [])
    medications = patient.get("current_medications", [])

    alert_id = f"ALERT-{patient_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Look up in lab thresholds first, then vitals
    trigger_key = trigger.strip().title()
    threshold_data = _CRITICAL_LAB_THRESHOLDS.get(trigger_key)
    threshold_type = "lab"

    if not threshold_data:
        trigger_lower = trigger.lower().replace(" ", "_")
        threshold_data = _CRITICAL_VITAL_THRESHOLDS.get(trigger_lower)
        threshold_type = "vital"

    if not threshold_data:
        # Generic alert if no threshold data
        alert = {
            "status": "alert_generated",
            "alert_id": alert_id,
            "patient_id": patient_id,
            "patient_name": patient_name,
            "trigger": trigger,
            "value": f"{value} {unit}",
            "severity": "WARNING",
            "direction": "ABNORMAL",
            "threshold": "No specific threshold on file",
            "immediate_action": "Notify attending physician for clinical evaluation",
            "clinical_context": clinical_context,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "patient_allergies": allergies,
            "current_medications": medications[:5] if medications else [],
        }
        _ALERT_LOG.append(alert)
        return alert

    # Determine direction and severity
    low = threshold_data.get("low") or threshold_data.get("critical_low") or threshold_data.get("warning_low")
    high = threshold_data.get("high") or threshold_data.get("critical_high") or threshold_data.get("warning_high")

    if low and value < low:
        direction = "CRITICALLY LOW"
        action = threshold_data.get("action_low", "Notify physician immediately")
        severity = "CRITICAL"
    elif high and value > high:
        direction = "CRITICALLY HIGH"
        action = threshold_data.get("action_high", "Notify physician immediately")
        severity = "CRITICAL"
    else:
        direction = "ABNORMAL"
        action = "Clinical review required"
        severity = "WARNING"

    # Check for medication interactions with the alert context
    interaction_flags = []
    if trigger_key == "Potassium" and value > 5.0:
        k_culprits = ["ace inhibitor", "spironolactone", "lisinopril", "losartan", "potassium"]
        for med in medications:
            if any(c in med.lower() for c in k_culprits):
                interaction_flags.append(f"Drug contributor: '{med}' increases potassium — consider dose reduction")
    if trigger_key == "INR" and value > 3.0:
        inr_meds = ["warfarin", "amiodarone", "fluconazole", "metronidazole"]
        for med in medications:
            if any(m in med.lower() for m in inr_meds):
                interaction_flags.append(f"Possible INR elevation contributor: '{med}'")

    alert = {
        "status": "alert_generated",
        "alert_id": alert_id,
        "patient_id": patient_id,
        "patient_name": patient_name,
        "trigger": trigger,
        "value": f"{value} {unit}",
        "threshold_type": threshold_type,
        "direction": direction,
        "severity": severity,
        "threshold_reference": f"Low: {threshold_data.get('low', 'N/A')} | High: {threshold_data.get('high', 'N/A')} {unit}",
        "immediate_action": action,
        "clinical_context": clinical_context or "Not specified",
        "medication_interaction_flags": interaction_flags,
        "patient_allergies": allergies,
        "current_medications": medications[:6] if medications else [],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "notification_required": True,
        "escalation_message": (
            f"🚨 CRITICAL ALERT — {patient_name} ({patient_id}): "
            f"{trigger} = {value} {unit} ({direction}). "
            f"Immediate action: {action}"
        ),
    }

    _ALERT_LOG.append(alert)
    return alert
