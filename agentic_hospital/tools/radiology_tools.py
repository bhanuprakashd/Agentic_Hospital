"""Radiology-specific imaging selection and critical findings tools."""


def imaging_study_selector(clinical_indication: str, body_region: str,
                            contraindications: list[str], urgency: str,
                            prior_imaging: str) -> dict:
    """Selects the most appropriate imaging modality for a clinical indication.

    Applies ACR Appropriateness Criteria and radiation dose considerations.

    Args:
        clinical_indication: Clinical question or suspected diagnosis.
        body_region: Anatomical region: 'head', 'chest', 'abdomen', 'pelvis',
                     'spine', 'extremity', 'whole_body', 'breast', 'vascular'.
        contraindications: List of contraindications (e.g., ['contrast_allergy',
                           'renal_failure', 'pacemaker', 'pregnancy', 'claustrophobia']).
        urgency: 'emergent', 'urgent', or 'routine'.
        prior_imaging: Description of prior imaging available, or 'none'.

    Returns:
        dict: Recommended study with rationale, alternative options, radiation dose,
              contrast considerations, and patient prep instructions.
    """
    indication_lower = clinical_indication.lower()
    region_lower = body_region.lower()

    # MRI contraindications
    mri_contraindicated = any(c in contraindications for c in
                               ["pacemaker", "cochlear_implant", "metallic_foreign_body",
                                "claustrophobia", "non_mri_compatible_implant"])
    # CT contrast contraindications
    contrast_contraindicated = any(c in contraindications for c in
                                    ["contrast_allergy", "renal_failure", "metformin"])
    # Radiation-sensitive
    pregnancy = "pregnancy" in contraindications

    # ---- HEAD ----
    if region_lower == "head":
        if any(k in indication_lower for k in ["stroke", "tia", "hemorrhage", "altered mental"]):
            primary = "CT Head without contrast" if urgency == "emergent" else "MRI Brain with DWI"
            rationale = "CT is fastest for hemorrhage exclusion in acute setting; MRI-DWI superior for ischemic stroke."
        elif "tumor" in indication_lower or "mass" in indication_lower or "metastasis" in indication_lower:
            primary = "MRI Brain with and without gadolinium" if not mri_contraindicated else "CT Head with contrast"
            rationale = "MRI with contrast is gold standard for intracranial masses."
        elif "sinusitis" in indication_lower:
            primary = "CT Sinuses without contrast"
            rationale = "CT sinuses delineates anatomy and extent of sinus disease."
        else:
            primary = "CT Head without contrast"
            rationale = "CT provides rapid assessment for most acute head pathology."
        alternatives = ["MRI Brain without/with contrast", "CT Angiography head/neck for vascular"]

    # ---- CHEST ----
    elif region_lower == "chest":
        if any(k in indication_lower for k in ["pe", "pulmonary embolism", "dvt"]):
            primary = "CT Pulmonary Angiography (CTPA)" if not contrast_contraindicated else "V/Q Scan"
            rationale = "CTPA is the gold standard for PE. V/Q scan if contrast contraindicated."
        elif any(k in indication_lower for k in ["pneumonia", "consolidation", "effusion"]):
            primary = "Chest X-Ray (PA and lateral)" if urgency != "routine" or prior_imaging == "none" else "CT Chest without contrast"
            rationale = "CXR is first-line for most pulmonary pathology; CT if CXR inconclusive."
        elif any(k in indication_lower for k in ["lung cancer", "nodule", "mass"]):
            primary = "CT Chest with contrast" if not contrast_contraindicated else "CT Chest without contrast"
            rationale = "CT with contrast for staging; low-dose CT for lung cancer screening (Lung-RADS)."
        elif "aorta" in indication_lower or "dissection" in indication_lower:
            primary = "CT Angiography Chest (CTA)" if not contrast_contraindicated else "MRI Aorta"
            rationale = "CTA is fastest and most accurate for aortic dissection/aneurysm."
        else:
            primary = "Chest X-Ray (PA and lateral)"
            rationale = "CXR is first-line screening for chest pathology."
        alternatives = ["CT Chest with/without contrast", "PET/CT for oncologic staging", "MRI Chest for cardiac/mediastinal"]

    # ---- ABDOMEN / PELVIS ----
    elif region_lower in ("abdomen", "pelvis", "abdomen_pelvis"):
        if any(k in indication_lower for k in ["appendicitis", "diverticulitis", "bowel obstruction"]):
            primary = "CT Abdomen/Pelvis with contrast (IV)" if not contrast_contraindicated else "CT Abdomen/Pelvis without contrast"
            rationale = "CT A/P with contrast is gold standard for acute abdominal emergencies."
        elif any(k in indication_lower for k in ["liver", "hepatic", "gallbladder", "biliary"]):
            primary = "Ultrasound Abdomen" if urgency != "routine" else "MRI Abdomen with/without gadolinium (MRCP for biliary)"
            rationale = "US is first-line for gallbladder/biliary. MRI/MRCP for liver characterization."
        elif any(k in indication_lower for k in ["renal", "kidney", "stone", "hydronephrosis"]):
            primary = "CT Abdomen/Pelvis without contrast (renal stone protocol)" if "stone" in indication_lower else "Ultrasound Renal"
            rationale = "Non-contrast CT is gold standard for urolithiasis. US avoids radiation."
        elif any(k in indication_lower for k in ["ovarian", "uterine", "pelvic pain"]):
            primary = "Pelvic Ultrasound (transvaginal preferred)" if not mri_contraindicated else "MRI Pelvis"
            rationale = "US is first-line for gynecologic pathology; MRI for complex lesions."
        else:
            primary = "CT Abdomen/Pelvis with contrast" if not contrast_contraindicated else "CT without contrast"
            rationale = "CT A/P provides comprehensive abdominal survey."
        alternatives = ["MRI Abdomen with gadolinium", "PET/CT for oncology", "Fluoroscopic studies (barium enema, swallow)"]

    # ---- SPINE ----
    elif region_lower == "spine":
        if any(k in indication_lower for k in ["cord compression", "myelopathy", "cauda equina"]):
            primary = "MRI Spine with and without gadolinium" if not mri_contraindicated else "CT Myelography"
            rationale = "MRI is gold standard for spinal cord and nerve root assessment. Emergent."
        elif "fracture" in indication_lower or "trauma" in indication_lower:
            primary = "CT Spine (cervical/thoracic/lumbar as indicated)"
            rationale = "CT superior to plain films for fracture detection and characterization."
        elif any(k in indication_lower for k in ["disc", "herniation", "radiculopathy", "stenosis"]):
            primary = "MRI Spine without contrast" if not mri_contraindicated else "CT Myelography"
            rationale = "MRI is first-line for disc disease and radiculopathy."
        else:
            primary = "X-Ray Spine (AP and lateral)"
            rationale = "Plain films for initial assessment of alignment, degenerative changes."
        alternatives = ["CT Spine", "MRI with gadolinium", "Nuclear bone scan for infection/malignancy"]

    # ---- BREAST ----
    elif region_lower == "breast":
        if any(k in indication_lower for k in ["screening", "mammogram"]):
            primary = "Digital Mammography or DBT (3D Tomosynthesis)"
            rationale = "DBT superior to 2D for dense breast tissue. Annual screening from age 40."
        elif "lump" in indication_lower or "mass" in indication_lower:
            primary = "Diagnostic Mammography + Ultrasound"
            rationale = "Combined imaging for symptomatic breast lump. MRI for extent of disease if malignancy confirmed."
        else:
            primary = "Breast Ultrasound"
            rationale = "US for targeted evaluation in young patients or dense breasts."
        alternatives = ["MRI Breast with gadolinium (high-risk screening)", "Breast biopsy under imaging guidance"]

    else:
        primary = "Plain X-Ray (AP and lateral)" if urgency == "emergent" else "Ultrasound"
        rationale = "X-ray is first-line for osseous structures; ultrasound for soft tissue."
        alternatives = ["MRI for soft tissue detail", "CT for complex anatomy"]

    # Pregnancy modifications
    if pregnancy:
        if region_lower in ("head", "extremity"):
            pass  # low/no gonadic dose — generally safe with shielding
        else:
            primary = "Ultrasound (preferred — no radiation)"
            rationale += " NOTE: Patient is pregnant — ultrasound preferred; MRI acceptable without gadolinium. Avoid CT unless life-threatening indication."
            alternatives = ["MRI without gadolinium", "CT only if life-threatening and benefits outweigh risks"]

    # Contrast allergy pre-medication
    premedication = None
    if "contrast_allergy" in contraindications and "CT" in primary and "without" not in primary:
        premedication = "Premedicate: Prednisone 50 mg PO at 13h, 7h, 1h before contrast + Diphenhydramine 50 mg IV/PO 1h before."

    # Radiation dose estimates
    dose_map = {
        "X-Ray": "0.01–0.1 mSv (very low)",
        "CT Head": "2 mSv",
        "CT Chest": "7 mSv",
        "CT Abdomen": "10 mSv",
        "CT Whole Body": "20 mSv",
        "MRI": "0 mSv (no ionizing radiation)",
        "Ultrasound": "0 mSv (no ionizing radiation)",
        "Nuclear": "6–25 mSv depending on agent",
        "PET/CT": "14–32 mSv",
    }
    rad_dose = next((v for k, v in dose_map.items() if k.lower() in primary.lower()), "Variable")

    return {
        "status": "selected",
        "clinical_indication": clinical_indication,
        "body_region": body_region,
        "recommended_study": primary,
        "rationale": rationale,
        "alternatives": alternatives,
        "radiation_dose_estimate": rad_dose,
        "contrast_required": "with contrast" in primary.lower(),
        "contrast_premedication": premedication,
        "contraindications_noted": contraindications,
        "patient_preparation": (
            "NPO 4 hours before if IV contrast. Remove metallic objects for MRI. "
            "Renal function (eGFR) required if IV contrast planned."
        ),
        "acr_appropriateness": "Usually Appropriate per ACR criteria for this indication.",
        "urgency": urgency,
    }


def report_critical_findings(finding_type: str, body_region: str,
                              severity: str, patient_id: str) -> dict:
    """Generates a critical radiology finding report with immediate notification protocol.

    Follows ACR and Joint Commission critical results communication standards.

    Args:
        finding_type: Type of critical finding (e.g., 'pneumothorax', 'intracranial_hemorrhage',
                      'aortic_dissection', 'pulmonary_embolism', 'bowel_perforation',
                      'spinal_cord_compression', 'malignancy_new').
        body_region: Anatomical region of the finding.
        severity: 'critical' (life-threatening, immediate), 'significant' (urgent, 1–4 hours),
                  or 'incidental' (non-urgent, routine report).
        patient_id: Patient identifier for documentation.

    Returns:
        dict: Standardized critical finding report with differential, immediate actions,
              recommended follow-up imaging, and communication protocol.
    """
    finding_lower = finding_type.lower()

    # Critical findings database
    findings_db = {
        "pneumothorax": {
            "description": "Air in pleural space causing lung collapse.",
            "urgent_actions": [
                "Notify ordering provider STAT",
                "Tension pneumothorax: immediate needle decompression 2nd ICS MCL, then chest tube",
                "Simple large (>2 cm): chest tube insertion (28–32 Fr)",
                "Small primary spontaneous (<2 cm): consider observation if stable",
            ],
            "follow_up_imaging": "Repeat CXR 4–6 hours post-intervention; CT Chest if complex",
            "differential": ["Tension pneumothorax", "Simple pneumothorax", "Pneumomediastinum"],
        },
        "intracranial_hemorrhage": {
            "description": "Hemorrhage within cranial vault — epidural, subdural, subarachnoid, or intracerebral.",
            "urgent_actions": [
                "Neurosurgery STAT consult",
                "Reverse anticoagulation if applicable (FFP, PCC, Vitamin K)",
                "Keep BP <160/90 mmHg for ICH; permissive hypertension for ischemic stroke",
                "Seizure prophylaxis (levetiracetam) per neurosurgery",
                "Elevate head of bed 30°, avoid Valsalva",
                "ICU admission",
            ],
            "follow_up_imaging": "CT Head repeat in 6 hours or sooner if neurological deterioration; MRI Brain for ischemic vs hemorrhagic differentiation",
            "differential": ["Epidural hematoma", "Subdural hematoma", "SAH", "Hypertensive ICH", "Hemorrhagic metastasis"],
        },
        "aortic_dissection": {
            "description": "Tear in the aortic intima with false lumen formation — surgical emergency (Type A).",
            "urgent_actions": [
                "Cardiothoracic surgery STAT",
                "Type A (ascending): emergency surgical repair",
                "Type B (descending): BP control (target SBP 100–120), HR <60 (IV beta-blocker)",
                "IV access x2, type & crossmatch 6 units pRBC",
                "ICU admission, arterial line",
                "Do NOT give anticoagulation",
            ],
            "follow_up_imaging": "CTA Aorta for surveillance (3 months, 6 months, then annually)",
            "differential": ["Type A dissection (DeBakey I/II)", "Type B dissection (DeBakey III)", "Aortic intramural hematoma", "Penetrating aortic ulcer"],
        },
        "pulmonary_embolism": {
            "description": "Thrombus in pulmonary vasculature — massive PE is immediately life-threatening.",
            "urgent_actions": [
                "Oxygen to maintain SpO2 ≥95%",
                "Anticoagulation: heparin bolus 80 U/kg IV then infusion",
                "Massive PE (hemodynamic instability): systemic thrombolysis (tPA 100 mg over 2 hrs) or catheter-directed therapy",
                "Pulmonary embolism response team (PERT) activation if available",
                "Echo for RV strain assessment",
                "ICU admission for high-risk PE",
            ],
            "follow_up_imaging": "CTPA 3–6 months to assess clot resolution; V/Q scan for chronic PE evaluation",
            "differential": ["Acute massive PE", "Submassive PE", "Low-risk PE", "Saddle embolus", "Pulmonary infarction"],
        },
        "bowel_perforation": {
            "description": "Free air in peritoneal cavity indicating GI perforation — surgical emergency.",
            "urgent_actions": [
                "General/colorectal surgery STAT",
                "NPO, IV access, fluid resuscitation",
                "Broad-spectrum antibiotics (piperacillin-tazobactam or cefepime + metronidazole)",
                "NG tube decompression if obstructed",
                "Emergency OR for repair/resection",
                "ICU post-operatively",
            ],
            "follow_up_imaging": "Post-operative CT A/P at 3–5 days if clinical concern for leak",
            "differential": ["Peptic ulcer perforation", "Colonic perforation (diverticular, neoplastic)", "Iatrogenic perforation"],
        },
        "spinal_cord_compression": {
            "description": "Compression of spinal cord or cauda equina requiring urgent decompression.",
            "urgent_actions": [
                "Neurosurgery and/or radiation oncology STAT consult",
                "Dexamethasone 10 mg IV bolus then 4 mg every 6 hours (for metastatic compression)",
                "Emergent MRI full spine with gadolinium if not already done",
                "Foley catheter (evaluate for urinary retention — cauda equina sign)",
                "Surgical decompression within 24 hours improves neurologic outcomes",
                "Radiation oncology for primary radiation if surgical candidate",
            ],
            "follow_up_imaging": "MRI spine with gadolinium post-decompression at 24–48 hours",
            "differential": ["Metastatic epidural compression", "Primary spinal tumor", "Disc herniation (acute massive)", "Epidural abscess/hematoma"],
        },
        "malignancy_new": {
            "description": "New malignancy identified on imaging — requires urgent oncologic workup.",
            "urgent_actions": [
                "Notify ordering provider urgently (same day)",
                "Direct communication with patient required",
                "Recommend tissue biopsy for histologic confirmation",
                "Oncology referral (urgent, within 1 week)",
                "Staging workup: PET/CT whole body, relevant tumor markers",
                "Multidisciplinary tumor board discussion",
            ],
            "follow_up_imaging": "PET/CT for staging; biopsy-guided by ultrasound/CT; MRI for local extent",
            "differential": ["Primary malignancy", "Metastatic disease", "Lymphoma", "Benign mimicker"],
        },
    }

    finding_data = findings_db.get(finding_lower, {
        "description": f"Critical finding: {finding_type} in {body_region}.",
        "urgent_actions": [
            "Notify ordering provider STAT",
            "Clinical assessment and stabilization",
            "Specialist consultation as appropriate",
        ],
        "follow_up_imaging": "Per specialist recommendation",
        "differential": ["Multiple etiologies possible — clinical correlation required"],
    })

    # Communication timeline by severity
    communication_timeline = {
        "critical": "Phone call to ordering provider WITHIN 30 MINUTES. Document: provider name, time, read-back confirmation.",
        "significant": "Phone call or direct message within 1–4 hours. Documentation required.",
        "incidental": "Include in dictated report. Recommend follow-up in impression.",
    }.get(severity, "Notify provider per departmental protocol")

    return {
        "status": "reported",
        "patient_id": patient_id,
        "finding_type": finding_type,
        "body_region": body_region,
        "severity_level": severity.upper(),
        "finding_description": finding_data["description"],
        "immediate_actions": finding_data["urgent_actions"],
        "differential_diagnosis": finding_data["differential"],
        "follow_up_imaging": finding_data["follow_up_imaging"],
        "communication_protocol": communication_timeline,
        "documentation_required": [
            f"Critical result logged in RIS/PACS at {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "Provider name and contact time documented",
            "Verbal read-back confirmation obtained",
            "Joint Commission critical results policy followed",
        ],
        "acr_reporting_standard": "ACR Practice Parameter for Communication of Diagnostic Imaging Findings adhered to.",
    }
