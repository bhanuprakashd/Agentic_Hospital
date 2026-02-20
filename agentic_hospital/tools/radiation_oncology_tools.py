"""Radiation Oncology-specific treatment planning and toxicity assessment tools."""


def calculate_radiation_dose(cancer_type: str, treatment_intent: str,
                              target_volume_cc: float, adjacent_critical_structures: list[str],
                              prior_radiation: bool) -> dict:
    """Calculates radiation dose prescription and fractionation scheme.

    Applies standard radiobiological principles (BED/EQD2) and current
    evidence-based dose prescriptions per NCCN/ASTRO guidelines.

    Args:
        cancer_type: Cancer being treated (e.g., 'prostate', 'breast', 'lung_nsclc',
                     'head_neck', 'brain_glioblastoma', 'cervix', 'rectal', 'lymphoma').
        treatment_intent: 'curative', 'adjuvant', 'neoadjuvant', or 'palliative'.
        target_volume_cc: Target volume in cubic centimeters (planning target volume, PTV).
        adjacent_critical_structures: Organs at risk near the target (e.g., ['spinal_cord',
                                       'heart', 'lungs', 'bowel', 'bladder', 'brainstem']).
        prior_radiation: True if the region has previously received radiation.

    Returns:
        dict: Recommended dose prescription, fractionation, technique, organs-at-risk
              dose constraints, and BED calculation.
    """
    # Evidence-based dose prescriptions
    dose_db = {
        "prostate": {
            "curative": {"dose_gy": 78, "fractions": 39, "fraction_size": 2.0, "technique": "IMRT/VMAT"},
            "hypofractionated_curative": {"dose_gy": 60, "fractions": 20, "fraction_size": 3.0, "technique": "IMRT/VMAT"},
            "sbrt_curative": {"dose_gy": 36.25, "fractions": 5, "fraction_size": 7.25, "technique": "SBRT (CyberKnife/LINAC)"},
            "palliative": {"dose_gy": 30, "fractions": 10, "fraction_size": 3.0, "technique": "3D-CRT"},
        },
        "breast": {
            "adjuvant": {"dose_gy": 50, "fractions": 25, "fraction_size": 2.0, "technique": "Tangential IMRT"},
            "hypofractionated_adjuvant": {"dose_gy": 40.05, "fractions": 15, "fraction_size": 2.67, "technique": "IMRT"},
            "palliative": {"dose_gy": 30, "fractions": 10, "fraction_size": 3.0, "technique": "3D-CRT"},
        },
        "lung_nsclc": {
            "curative": {"dose_gy": 60, "fractions": 30, "fraction_size": 2.0, "technique": "IMRT/4D-CT gating"},
            "sbrt_curative": {"dose_gy": 54, "fractions": 3, "fraction_size": 18.0, "technique": "SBRT (peripherally located)"},
            "palliative": {"dose_gy": 30, "fractions": 10, "fraction_size": 3.0, "technique": "3D-CRT"},
        },
        "head_neck": {
            "curative": {"dose_gy": 70, "fractions": 35, "fraction_size": 2.0, "technique": "IMRT (simultaneous integrated boost)"},
            "adjuvant": {"dose_gy": 60, "fractions": 30, "fraction_size": 2.0, "technique": "IMRT"},
            "palliative": {"dose_gy": 30, "fractions": 10, "fraction_size": 3.0, "technique": "3D-CRT"},
        },
        "brain_glioblastoma": {
            "curative": {"dose_gy": 60, "fractions": 30, "fraction_size": 2.0, "technique": "IMRT + temozolomide (Stupp protocol)"},
            "palliative": {"dose_gy": 30, "fractions": 10, "fraction_size": 3.0, "technique": "3D-CRT"},
        },
        "brain_metastasis": {
            "curative": {"dose_gy": 24, "fractions": 1, "fraction_size": 24.0, "technique": "SRS (Gamma Knife/LINAC)"},
            "palliative": {"dose_gy": 30, "fractions": 10, "fraction_size": 3.0, "technique": "WBRT"},
        },
        "cervix": {
            "curative": {"dose_gy": 45, "fractions": 25, "fraction_size": 1.8, "technique": "IMRT + brachytherapy boost (LDR/HDR)"},
            "palliative": {"dose_gy": 30, "fractions": 10, "fraction_size": 3.0, "technique": "3D-CRT"},
        },
        "rectal": {
            "neoadjuvant": {"dose_gy": 45, "fractions": 25, "fraction_size": 1.8, "technique": "IMRT + capecitabine (long course)"},
            "short_course_neoadjuvant": {"dose_gy": 25, "fractions": 5, "fraction_size": 5.0, "technique": "3D-CRT/IMRT"},
            "palliative": {"dose_gy": 30, "fractions": 10, "fraction_size": 3.0, "technique": "3D-CRT"},
        },
        "lymphoma": {
            "curative": {"dose_gy": 30, "fractions": 15, "fraction_size": 2.0, "technique": "ISRT (IMRT)"},
            "palliative": {"dose_gy": 20, "fractions": 10, "fraction_size": 2.0, "technique": "Involved-site RT"},
        },
        "bone_metastasis": {
            "palliative": {"dose_gy": 8, "fractions": 1, "fraction_size": 8.0, "technique": "3D-CRT (single fraction)"},
        },
    }

    # Select prescription
    cancer_key = cancer_type.lower().replace(" ", "_")
    prescriptions = dose_db.get(cancer_key, {})
    intent_key = treatment_intent.lower()

    if intent_key in prescriptions:
        rx = prescriptions[intent_key]
    elif "palliative" in prescriptions and intent_key == "palliative":
        rx = prescriptions["palliative"]
    elif prescriptions:
        rx = list(prescriptions.values())[0]  # default to first available
    else:
        rx = {"dose_gy": 30, "fractions": 10, "fraction_size": 3.0, "technique": "3D-CRT (generic)"}

    dose_gy = rx["dose_gy"]
    fractions = rx["fractions"]
    fraction_size = rx["fraction_size"]
    technique = rx["technique"]

    # BED and EQD2 calculation (α/β = 10 for tumors, 3 for late-responding tissues)
    alpha_beta_tumor = 10
    alpha_beta_late = 3
    bed_tumor = dose_gy * (1 + fraction_size / alpha_beta_tumor)
    bed_late = dose_gy * (1 + fraction_size / alpha_beta_late)
    eqd2_tumor = bed_tumor / (1 + 2 / alpha_beta_tumor)
    eqd2_late = bed_late / (1 + 2 / alpha_beta_late)

    # Organs at risk (OAR) dose constraints
    oar_constraints = {}
    constraint_db = {
        "spinal_cord": "Max 45 Gy (conventional); Max 14 Gy (SBRT/SRS single fraction)",
        "brainstem": "Max 54 Gy (1-3 cc); Max 60 Gy (<1 cc)",
        "heart": "Mean <26 Gy; V25Gy <10% for breast; V30Gy <46%",
        "lungs": "V20Gy <30–35%; Mean lung dose <20 Gy; V5Gy <65%",
        "bowel": "Max <45–50 Gy; V45Gy <195 cc for small bowel",
        "bladder": "V50Gy <50%; Max <65 Gy",
        "rectum": "V70Gy <20%; V65Gy <25%; V40Gy <80% (prostate RT)",
        "optic_nerve": "Max <54 Gy; Max <8 Gy (SRS)",
        "parotid": "Mean <25–26 Gy (at least one parotid)",
        "kidneys": "Mean <18 Gy each; V20Gy <32% bilateral",
        "liver": "Mean <28–32 Gy; V30Gy <60%",
        "esophagus": "Mean <34 Gy; Max <74 Gy",
    }
    for struct in adjacent_critical_structures:
        struct_key = struct.lower().replace(" ", "_")
        if struct_key in constraint_db:
            oar_constraints[struct] = constraint_db[struct_key]

    # Re-irradiation note
    reirrad_note = None
    if prior_radiation:
        reirrad_note = (
            "CAUTION: Prior radiation history. Cumulative dose to critical structures must be calculated. "
            "Radiobiology consult recommended. Consider SBRT for re-irradiation if anatomically feasible. "
            "BED summation required for OAR constraints."
        )

    return {
        "status": "calculated",
        "cancer_type": cancer_type,
        "treatment_intent": treatment_intent,
        "prescription": {
            "total_dose_gy": dose_gy,
            "fractions": fractions,
            "dose_per_fraction_gy": fraction_size,
            "technique": technique,
            "treatment_duration_weeks": round(fractions / 5, 1),
        },
        "radiobiology": {
            "bed_tumor_gy": round(bed_tumor, 1),
            "bed_late_tissue_gy": round(bed_late, 1),
            "eqd2_tumor_gy": round(eqd2_tumor, 1),
            "eqd2_late_tissue_gy": round(eqd2_late, 1),
            "alpha_beta_tumor": alpha_beta_tumor,
            "alpha_beta_late": alpha_beta_late,
        },
        "organs_at_risk_constraints": oar_constraints,
        "target_volume_cc": target_volume_cc,
        "reirradiation_note": reirrad_note,
        "concurrent_systemic_therapy": {
            "head_neck": "Cisplatin 100 mg/m² every 3 weeks or weekly 40 mg/m²",
            "cervix": "Cisplatin 40 mg/m² weekly",
            "rectal_long_course": "Capecitabine 825 mg/m² BID on RT days",
            "brain_glioblastoma": "Temozolomide 75 mg/m² daily during RT (Stupp protocol)",
            "lung_nsclc": "Durvalumab consolidation after concurrent chemoRT",
        }.get(cancer_key, "Per medical oncology recommendation"),
        "guidelines_reference": "NCCN, ASTRO, ESTRO guidelines for respective tumor site.",
    }


def radiation_toxicity_assessment(cancer_type: str, treatment_site: str,
                                   dose_delivered_gy: float, weeks_since_treatment: int,
                                   reported_symptoms: list[str]) -> dict:
    """Assesses and grades radiation-related toxicity using CTCAE v5.0.

    Differentiates acute (<90 days) vs. late toxicities and provides management.

    Args:
        cancer_type: Cancer type being treated.
        treatment_site: Body region irradiated (e.g., 'head_neck', 'chest', 'pelvis', 'brain').
        dose_delivered_gy: Total dose delivered in Gray.
        weeks_since_treatment: Weeks since radiation treatment ended (0 = ongoing).
        reported_symptoms: List of patient-reported symptoms.

    Returns:
        dict: CTCAE-graded toxicities, management recommendations, and expected timeline.
    """
    # Determine acute vs. late
    toxicity_phase = "acute" if weeks_since_treatment < 13 else "late"

    # Site-specific toxicity profiles
    toxicity_profiles = {
        "head_neck": {
            "acute": {
                "mucositis": "Grade 1–2: saltwater rinses, magic mouthwash, lidocaine. Grade 3+: IV hydration, PEG tube consideration, opioids.",
                "xerostomia": "Saliva substitutes, pilocarpine 5 mg TID, amifostine (if protocol).",
                "dermatitis": "Aquaphor, silvadene for Grade 3. Hydrocolloid dressings for moist desquamation.",
                "dysphagia": "Speech therapy, dietary modification, NG/PEG tube if <1500 kcal/day by mouth.",
                "odynophagia": "Viscous lidocaine, systemic opioids if severe.",
            },
            "late": {
                "xerostomia": "Permanent if parotid spared inadequately. Pilocarpine, cevimeline.",
                "fibrosis": "Pentoxifylline + Vitamin E (PENTOCLO protocol). Physical therapy, jaw exercises.",
                "osteoradionecrosis": "Hyperbaric oxygen, sequestrectomy, or free flap reconstruction.",
                "hypothyroidism": "Monitor TSH every 6 months. Levothyroxine replacement.",
                "carotid_stenosis": "Annual carotid duplex ultrasound. Vascular surgery referral.",
            },
        },
        "chest": {
            "acute": {
                "esophagitis": "PPI, sucralfate, magic mouthwash. Grade 3+: IV hydration, TPN.",
                "pneumonitis": "Prednisone 1 mg/kg/day tapering over 4–8 weeks. Avoid re-irradiation.",
                "fatigue": "Exercise, counseling, rule out anemia/hypothyroidism.",
                "skin_reaction": "Aquaphor, silvadene for Grade 3+ dermatitis.",
            },
            "late": {
                "pulmonary_fibrosis": "PFT monitoring, supplemental oxygen, anti-fibrotics (pirfenidone/nintedanib).",
                "cardiac_toxicity": "Echocardiogram, cardiology referral if symptomatic. Statins, ACE inhibitors.",
                "esophageal_stricture": "Dilation. Consider esophageal stent for malignant stricture.",
            },
        },
        "pelvis": {
            "acute": {
                "diarrhea": "Loperamide, low-residue diet, hydration, Imodium. Grade 3+: IV fluids, octreotide.",
                "cystitis": "Hydration, phenazopyridine, rule out infection. Grade 3+: urology consult.",
                "proctitis": "Mesalazine suppositories, hydrocortisone enema, sucralfate enemas.",
                "vaginal_mucositis": "Sitz baths, topical lidocaine.",
            },
            "late": {
                "bowel_obstruction": "Surgical evaluation. NG decompression. Late radiation enteropathy — parenteral nutrition.",
                "fistula": "Surgery, temporary diversion colostomy.",
                "vaginal_stenosis": "Vaginal dilators starting 4–6 weeks post-RT. Topical estrogen.",
                "erectile_dysfunction": "PDE-5 inhibitors, vacuum devices, penile rehabilitation.",
                "bladder_contracture": "Urologic evaluation, suprapubic catheter, cystectomy in severe cases.",
            },
        },
        "brain": {
            "acute": {
                "cerebral_edema": "Dexamethasone 4–8 mg every 6 hours. Taper carefully.",
                "fatigue": "Rest, modafinil off-label for radiation fatigue.",
                "alopecia": "Temporary (returns in 3–6 months for doses <55 Gy).",
                "nausea": "Ondansetron, dexamethasone.",
            },
            "late": {
                "radiation_necrosis": "Bevacizumab 7.5 mg/kg every 3 weeks (most effective). Hyperbaric oxygen.",
                "cognitive_decline": "Memantine during WBRT (RTOG 0614). Neurocognitive rehabilitation.",
                "leukoencephalopathy": "Avoid concurrent methotrexate. Monitor with MRI.",
                "hypopituitarism": "Annual hormonal panel. Hormone replacement therapy.",
            },
        },
    }

    site_key = treatment_site.lower().replace(" ", "_")
    site_profile = toxicity_profiles.get(site_key, {})
    phase_profile = site_profile.get(toxicity_phase, {})

    # Match reported symptoms to management
    symptom_management = {}
    for symptom in reported_symptoms:
        sym_lower = symptom.lower().replace(" ", "_")
        matched = {k: v for k, v in phase_profile.items() if k in sym_lower or sym_lower in k}
        if matched:
            symptom_management[symptom] = list(matched.values())[0]
        else:
            symptom_management[symptom] = "Symptomatic management; specialist consultation if Grade 3+."

    # CTCAE grading guide
    ctcae_grades = {
        1: "Mild; asymptomatic or mild symptoms; clinical or diagnostic observations only",
        2: "Moderate; minimal, local, or non-invasive intervention indicated",
        3: "Severe; IV intervention indicated; hospitalization indicated",
        4: "Life-threatening; urgent intervention indicated",
        5: "Death related to adverse event",
    }

    return {
        "status": "assessed",
        "cancer_type": cancer_type,
        "treatment_site": treatment_site,
        "dose_delivered_gy": dose_delivered_gy,
        "toxicity_phase": toxicity_phase.upper(),
        "weeks_since_treatment": weeks_since_treatment,
        "symptom_management": symptom_management,
        "ctcae_grading_reference": ctcae_grades,
        "expected_timeline": (
            "Acute toxicities (mucositis, dermatitis, diarrhea) peak 2–4 weeks into treatment and resolve 4–8 weeks after. "
            "Late toxicities (fibrosis, fistula, necrosis) emerge months to years later and are often irreversible."
        ) if toxicity_phase == "acute" else (
            "Late effects are typically permanent or slowly progressive. "
            "Early intervention improves quality of life. Annual surveillance with relevant specialists recommended."
        ),
        "when_to_escalate": [
            "Grade 3+ toxicity → hospital admission consideration",
            "Inability to maintain oral intake → nutritional support",
            "New neurological deficit → urgent imaging",
            "Suspected fistula → surgical consultation",
            "Severe bleeding → urgent intervention",
        ],
        "guidelines": "CTCAE v5.0 (NCI) | ASTRO toxicity management guidelines",
    }
