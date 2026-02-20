"""Hospital Bed Management & Admission System.

Provides real-time bed tracking across 20 inpatient wards (325 beds total),
with ASCII ward visualisations, markdown hospital dashboard, patient admission,
discharge, inter-ward transfer, and priority waitlist management.
"""

import datetime
from typing import Optional

# Import patient registry for cross-reference
from .common_tools import _PATIENT_DB


# =============================================================================
# PRIORITY ORDER (for sorting waitlists)
# =============================================================================
_PRIORITY_ORDER = {"emergency": 0, "urgent": 1, "routine": 2}


# =============================================================================
# BED DATABASE — 20 inpatient wards, 325 beds total
# Statuses: "available" | "occupied" | "cleaning" | "maintenance"
# Pre-populated: P001–P010 placed in clinically appropriate wards
# =============================================================================
def _make_bed(status: str, patient_id: str = "", patient_name: str = "",
              admitted: str = "", diagnosis: str = "", notes: str = "") -> dict:
    return {
        "status": status,
        "patient_id": patient_id,
        "patient_name": patient_name,
        "admitted": admitted,
        "diagnosis": diagnosis,
        "notes": notes,
    }


def _occ(pid: str, diag: str, admitted: str = "2026-02-18 09:00") -> dict:
    """Shorthand for a pre-occupied bed using a known patient."""
    p = _PATIENT_DB.get(pid, {})
    return _make_bed("occupied", pid, p.get("name", pid), admitted, diag)


def _anon(diag: str, admitted: str = "2026-02-17 14:00") -> dict:
    """Shorthand for an anonymised occupied bed (background census)."""
    return _make_bed("occupied", "", "Admitted Patient", admitted, diag)


_AVAIL = _make_bed("available")
_CLEAN = _make_bed("cleaning", notes="Housekeeping in progress — ready ~15 min")
_MAINT = _make_bed("maintenance", notes="Out of service — engineering review")


_BED_DB: dict[str, dict] = {

    # ── ICU (10 beds) ────────────────────────────────────────────────────────
    "ICU": {
        "capacity": 10,
        "bed_type": "intensive_care",
        "floor": "2",
        "nurse_station": "ICU Central",
        "beds": {
            "ICU-01": _occ("P003", "COPD exacerbation + Chronic Heart Failure (EF 40%)", "2026-02-18 08:30"),
            "ICU-02": _occ("P010", "Decompensated HF + Persistent AFib post-CABG", "2026-02-19 22:10"),
            "ICU-03": _anon("Post-cardiac arrest — ROSC, targeted temperature management"),
            "ICU-04": _anon("Septic shock — Gram-negative bacteraemia"),
            "ICU-05": _anon("ARDS — post-influenza pneumonia", "2026-02-16 11:30"),
            "ICU-06": _anon("Hypertensive emergency — MAP target in progress"),
            "ICU-07": _CLEAN,
            "ICU-08": _AVAIL,
            "ICU-09": _AVAIL,
            "ICU-10": _MAINT,
        },
    },

    # ── Emergency (15 beds) ──────────────────────────────────────────────────
    "Emergency": {
        "capacity": 15,
        "bed_type": "emergency",
        "floor": "1",
        "nurse_station": "ED Triage Desk",
        "beds": {
            "EM-01": _anon("Chest pain — rule out ACS, troponin pending"),
            "EM-02": _anon("Acute stroke — tPA eligible, CT complete"),
            "EM-03": _anon("Traumatic head injury — GCS 12"),
            "EM-04": _anon("Anaphylaxis — epinephrine given, monitoring"),
            "EM-05": _anon("Acute abdomen — surgical consult pending"),
            "EM-06": _anon("Altered mental status — metabolic workup"),
            "EM-07": _anon("Polytrauma — MVA", "2026-02-20 07:45"),
            "EM-08": _anon("Acute asthma exacerbation — neb therapy"),
            "EM-09": _anon("Supratherapeutic INR — hold warfarin protocol"),
            "EM-10": _anon("Diabetic ketoacidosis — insulin infusion"),
            "EM-11": _CLEAN,
            "EM-12": _CLEAN,
            "EM-13": _AVAIL,
            "EM-14": _AVAIL,
            "EM-15": _AVAIL,
        },
    },

    # ── Cardiology (20 beds) ─────────────────────────────────────────────────
    "Cardiology": {
        "capacity": 20,
        "bed_type": "general",
        "floor": "4",
        "nurse_station": "Cardiology Ward 4A",
        "beds": {
            "CARD-01": _anon("NSTEMI — post-PCI, monitoring", "2026-02-19 15:00"),
            "CARD-02": _anon("Paroxysmal SVT — rate control achieved"),
            "CARD-03": _anon("Acute decompensated HF — IV diuresis"),
            "CARD-04": _anon("New-onset atrial fibrillation — cardioversion planned"),
            "CARD-05": _anon("STEMI — post-primary PCI Day 2"),
            "CARD-06": _anon("Hypertensive urgency — oral antihypertensives"),
            "CARD-07": _anon("Pericarditis — NSAID therapy, monitoring"),
            "CARD-08": _anon("Complete heart block — awaiting PPM implant"),
            "CARD-09": _anon("Endocarditis — IV antibiotics Day 5"),
            "CARD-10": _anon("Stable angina — elective angiogram tomorrow"),
            "CARD-11": _anon("Cardiac arrest survivor — electrophysiology workup"),
            "CARD-12": _anon("Takotsubo cardiomyopathy — supportive care"),
            "CARD-13": _anon("VT storm — amiodarone load"),
            "CARD-14": _anon("Aortic stenosis — TAVR prep"),
            "CARD-15": _CLEAN,
            "CARD-16": _CLEAN,
            "CARD-17": _AVAIL,
            "CARD-18": _AVAIL,
            "CARD-19": _AVAIL,
            "CARD-20": _AVAIL,
        },
    },

    # ── Neurology (16 beds) ──────────────────────────────────────────────────
    "Neurology": {
        "capacity": 16,
        "bed_type": "general",
        "floor": "5",
        "nurse_station": "Neurology Ward 5B",
        "beds": {
            "NEUR-01": _anon("Ischaemic stroke — Day 3 post-tPA"),
            "NEUR-02": _anon("Generalised tonic-clonic seizure — levetiracetam load"),
            "NEUR-03": _anon("Multiple sclerosis relapse — IV methylprednisolone"),
            "NEUR-04": _anon("Guillain-Barré syndrome — IVIG Day 2"),
            "NEUR-05": _occ("P004", "Intractable migraine — IV DHE protocol", "2026-02-20 06:15"),
            "NEUR-06": _anon("Myasthenic crisis — plasmapheresis"),
            "NEUR-07": _anon("SAH — Hunt-Hess Grade 2, nimodipine"),
            "NEUR-08": _anon("Parkinson's crisis — medication adjustment"),
            "NEUR-09": _anon("Transient ischaemic attack — ABCD2 score 5"),
            "NEUR-10": _anon("Encephalitis — IV acyclovir, LP pending"),
            "NEUR-11": _CLEAN,
            "NEUR-12": _AVAIL,
            "NEUR-13": _AVAIL,
            "NEUR-14": _AVAIL,
            "NEUR-15": _AVAIL,
            "NEUR-16": _MAINT,
        },
    },

    # ── Oncology (20 beds) ───────────────────────────────────────────────────
    "Oncology": {
        "capacity": 20,
        "bed_type": "general",
        "floor": "6",
        "nurse_station": "Oncology Ward 6A",
        "beds": {
            "ONCO-01": _anon("NSCLC Stage IV — pembrolizumab cycle 4"),
            "ONCO-02": _anon("AML induction — Day 14 post-chemotherapy"),
            "ONCO-03": _anon("Breast cancer — post-mastectomy Day 2"),
            "ONCO-04": _anon("Colorectal cancer — FOLFOX cycle 6 infusion"),
            "ONCO-05": _anon("Febrile neutropenia — broad-spectrum IV antibiotics"),
            "ONCO-06": _anon("Lymphoma — R-CHOP Day 1"),
            "ONCO-07": _anon("Multiple myeloma — bone pain management"),
            "ONCO-08": _anon("Ovarian cancer — carboplatin/paclitaxel"),
            "ONCO-09": _anon("Prostate cancer — bone met pain, zoledronic acid"),
            "ONCO-10": _anon("Pancreatic cancer — palliative symptom control"),
            "ONCO-11": _anon("Renal cell carcinoma — sunitinib side effects"),
            "ONCO-12": _anon("Head & neck SCC — cisplatin/5-FU"),
            "ONCO-13": _anon("DLBCL — CAR-T cell therapy monitoring"),
            "ONCO-14": _anon("Glioblastoma — post-craniotomy Day 4"),
            "ONCO-15": _anon("Cervical cancer — concurrent chemoradiation"),
            "ONCO-16": _CLEAN,
            "ONCO-17": _CLEAN,
            "ONCO-18": _AVAIL,
            "ONCO-19": _AVAIL,
            "ONCO-20": _AVAIL,
        },
    },

    # ── General Medicine (30 beds) ───────────────────────────────────────────
    "General_Medicine": {
        "capacity": 30,
        "bed_type": "general",
        "floor": "3",
        "nurse_station": "Gen Med Ward 3A/3B",
        "beds": {
            "GM-01": _occ("P001", "Uncontrolled T2DM + HTN — medication review", "2026-02-19 10:45"),
            "GM-02": _anon("Community-acquired pneumonia — IV amoxicillin-clavulanate"),
            "GM-03": _anon("Acute gout flare — colchicine + NSAIDs"),
            "GM-04": _anon("Cellulitis — IV flucloxacillin"),
            "GM-05": _anon("Anaemia workup — transfusion pre-assessment"),
            "GM-06": _anon("Syncope — tilt table test pending"),
            "GM-07": _anon("Dehydration — IV fluid resuscitation"),
            "GM-08": _anon("Hyponatraemia — fluid restriction + monitoring"),
            "GM-09": _anon("Urinary tract infection — IV nitrofurantoin"),
            "GM-10": _anon("DVT — anticoagulation initiation"),
            "GM-11": _anon("Exacerbation of COPD — nebulisers + steroids"),
            "GM-12": _anon("Delirium — elderly fall, investigation"),
            "GM-13": _anon("Thyroid storm — PTU + propranolol"),
            "GM-14": _anon("Pulmonary embolism — LMWH bridging"),
            "GM-15": _anon("Fever of unknown origin — blood cultures, imaging"),
            "GM-16": _anon("Hyperglycaemic hyperosmolar state — fluid protocol"),
            "GM-17": _anon("Alcohol withdrawal — CIWA protocol"),
            "GM-18": _anon("Falls assessment — physiotherapy referral"),
            "GM-19": _anon("New AF — rate control achieved", "2026-02-18 16:30"),
            "GM-20": _anon("Hypokalaemia — IV potassium replacement"),
            "GM-21": _CLEAN,
            "GM-22": _CLEAN,
            "GM-23": _CLEAN,
            "GM-24": _AVAIL,
            "GM-25": _AVAIL,
            "GM-26": _AVAIL,
            "GM-27": _AVAIL,
            "GM-28": _AVAIL,
            "GM-29": _AVAIL,
            "GM-30": _AVAIL,
        },
    },

    # ── Psychiatry (15 beds) ─────────────────────────────────────────────────
    "Psychiatry": {
        "capacity": 15,
        "bed_type": "psychiatric",
        "floor": "7",
        "nurse_station": "Psychiatry Ward 7 (Secure)",
        "beds": {
            "PSY-01": _anon("Major depressive episode — suicidal ideation, 1:1 obs"),
            "PSY-02": _anon("Bipolar I — manic episode, olanzapine load"),
            "PSY-03": _anon("Schizophrenia — first episode psychosis"),
            "PSY-04": _anon("Anorexia nervosa — medical stabilisation"),
            "PSY-05": _anon("OCD — residential exposure therapy"),
            "PSY-06": _anon("Acute PTSD — crisis stabilisation"),
            "PSY-07": _anon("Alcohol use disorder — detox Day 2"),
            "PSY-08": _anon("Borderline PD crisis — DBT skills group"),
            "PSY-09": _anon("Schizoaffective disorder — clozapine titration"),
            "PSY-10": _anon("Panic disorder — acute admission"),
            "PSY-11": _CLEAN,
            "PSY-12": _AVAIL,
            "PSY-13": _AVAIL,
            "PSY-14": _AVAIL,
            "PSY-15": _AVAIL,
        },
    },

    # ── Pediatrics (20 beds) ─────────────────────────────────────────────────
    "Pediatrics": {
        "capacity": 20,
        "bed_type": "pediatric",
        "floor": "3",
        "nurse_station": "Paeds Ward 3C",
        "beds": {
            "PED-01": _anon("Acute asthma — salbutamol nebs, age 8"),
            "PED-02": _anon("Febrile seizure — observation, age 2"),
            "PED-03": _anon("Bronchiolitis — high-flow O2, age 4 months"),
            "PED-04": _anon("Appendicitis — post-laparoscopic surgery Day 1"),
            "PED-05": _anon("Meningitis — IV ceftriaxone, age 5"),
            "PED-06": _anon("Croup — racemic epinephrine, observation"),
            "PED-07": _anon("Diabetic ketoacidosis — T1DM, age 12"),
            "PED-08": _anon("Kawasaki disease — IVIG Day 1, age 3"),
            "PED-09": _anon("Sickle cell crisis — analgesia, IV fluids"),
            "PED-10": _anon("RSV bronchiolitis — oxygen therapy, age 6 weeks"),
            "PED-11": _anon("Intussusception — post-air enema, observation"),
            "PED-12": _anon("Failure to thrive — nutritional assessment"),
            "PED-13": _CLEAN,
            "PED-14": _CLEAN,
            "PED-15": _AVAIL,
            "PED-16": _AVAIL,
            "PED-17": _AVAIL,
            "PED-18": _AVAIL,
            "PED-19": _AVAIL,
            "PED-20": _AVAIL,
        },
    },

    # ── Orthopedics (20 beds) ────────────────────────────────────────────────
    "Orthopedics": {
        "capacity": 20,
        "bed_type": "surgical",
        "floor": "4",
        "nurse_station": "Ortho Ward 4B",
        "beds": {
            "ORTH-01": _anon("NOF fracture — awaiting hemi-arthroplasty"),
            "ORTH-02": _anon("TKR post-op Day 1 — physiotherapy started"),
            "ORTH-03": _anon("THR post-op Day 2 — weight-bearing as tolerated"),
            "ORTH-04": _anon("Open tibia fracture — ORIF post-op Day 3"),
            "ORTH-05": _anon("Septic arthritis — IV antibiotics + washout"),
            "ORTH-06": _occ("P005", "Acute L4-L5 disc herniation — conservative management", "2026-02-20 08:00"),
            "ORTH-07": _anon("Distal radius fracture — ORIF planned"),
            "ORTH-08": _anon("Spinal stenosis — L3-S1 laminectomy post-op Day 1"),
            "ORTH-09": _anon("Periprosthetic joint infection — revision planned"),
            "ORTH-10": _anon("Traumatic shoulder dislocation — reduction done, sling"),
            "ORTH-11": _anon("Osteomyelitis — IV cefazolin"),
            "ORTH-12": _anon("Compartment syndrome — fasciotomy post-op"),
            "ORTH-13": _CLEAN,
            "ORTH-14": _CLEAN,
            "ORTH-15": _AVAIL,
            "ORTH-16": _AVAIL,
            "ORTH-17": _AVAIL,
            "ORTH-18": _AVAIL,
            "ORTH-19": _AVAIL,
            "ORTH-20": _AVAIL,
        },
    },

    # ── General Surgery (18 beds) ────────────────────────────────────────────
    "General_Surgery": {
        "capacity": 18,
        "bed_type": "surgical",
        "floor": "4",
        "nurse_station": "Gen Surg Ward 4C",
        "beds": {
            "GS-01": _anon("Laparoscopic appendicectomy post-op Day 1"),
            "GS-02": _anon("Hartmann's reversal — stoma takedown post-op"),
            "GS-03": _anon("Laparoscopic cholecystectomy post-op — Day 1"),
            "GS-04": _anon("Bowel obstruction — conservative management"),
            "GS-05": _anon("Incisional hernia repair post-op"),
            "GS-06": _anon("Perforated peptic ulcer — post-laparotomy Day 2"),
            "GS-07": _anon("Thyroidectomy post-op — monitoring Ca2+"),
            "GS-08": _anon("Strangulated inguinal hernia — post-repair Day 1"),
            "GS-09": _anon("Abdominal abscess — CT-guided drain in situ"),
            "GS-10": _anon("GI bleed — upper endoscopy scheduled"),
            "GS-11": _anon("Sigmoid volvulus — flexible sigmoidoscopy done"),
            "GS-12": _anon("Traumatic splenectomy — post-op Day 3"),
            "GS-13": _CLEAN,
            "GS-14": _CLEAN,
            "GS-15": _AVAIL,
            "GS-16": _AVAIL,
            "GS-17": _AVAIL,
            "GS-18": _AVAIL,
        },
    },

    # ── Gynecology (15 beds) ─────────────────────────────────────────────────
    "Gynecology": {
        "capacity": 15,
        "bed_type": "general",
        "floor": "5",
        "nurse_station": "Gynae Ward 5A",
        "beds": {
            "GYN-01": _occ("P002", "PCOS — hormonal evaluation + anaemia treatment", "2026-02-19 14:20"),
            "GYN-02": _anon("Ectopic pregnancy — post-salpingectomy Day 1"),
            "GYN-03": _anon("Endometriosis — laparoscopic excision post-op"),
            "GYN-04": _anon("Miscarriage — surgical evacuation, observation"),
            "GYN-05": _anon("Cervical cancer — pre-op staging"),
            "GYN-06": _anon("Ovarian cyst rupture — pain management, obs"),
            "GYN-07": _anon("Pelvic inflammatory disease — IV antibiotics"),
            "GYN-08": _anon("Post-hysterectomy Day 2 — recovery"),
            "GYN-09": _anon("Hyperemesis gravidarum — IV hydration"),
            "GYN-10": _anon("Fibroids — uterine artery embolisation post-proc"),
            "GYN-11": _CLEAN,
            "GYN-12": _AVAIL,
            "GYN-13": _AVAIL,
            "GYN-14": _AVAIL,
            "GYN-15": _AVAIL,
        },
    },

    # ── Nephrology (14 beds) ─────────────────────────────────────────────────
    "Nephrology": {
        "capacity": 14,
        "bed_type": "general",
        "floor": "6",
        "nurse_station": "Nephrology Ward 6B",
        "beds": {
            "NEPH-01": _occ("P008", "SLE Lupus Nephritis Class III — IV methylprednisolone", "2026-02-18 11:00"),
            "NEPH-02": _anon("AKI on CKD — volume resuscitation"),
            "NEPH-03": _anon("Hyperkalaemia — insulin + dextrose, cardiac monitoring"),
            "NEPH-04": _anon("Haemodialysis fistula thrombosis — urgent intervention"),
            "NEPH-05": _anon("Nephrotic syndrome — albumin infusion"),
            "NEPH-06": _anon("Renal transplant rejection — pulse steroids"),
            "NEPH-07": _anon("IgA nephropathy flare — ACEi uptitration"),
            "NEPH-08": _anon("Hypertensive nephrosclerosis — BP optimisation"),
            "NEPH-09": _anon("ESRD — tunnelled line insertion for HD initiation"),
            "NEPH-10": _CLEAN,
            "NEPH-11": _AVAIL,
            "NEPH-12": _AVAIL,
            "NEPH-13": _AVAIL,
            "NEPH-14": _AVAIL,
        },
    },

    # ── Pulmonology (18 beds) ────────────────────────────────────────────────
    "Pulmonology": {
        "capacity": 18,
        "bed_type": "general",
        "floor": "3",
        "nurse_station": "Respiratory Ward 3D",
        "beds": {
            "PULM-01": _occ("P006", "COPD GOLD III exacerbation — IV steroids + nebulisers", "2026-02-19 07:30"),
            "PULM-02": _anon("Severe asthma — IV magnesium, HDU step-up watch"),
            "PULM-03": _anon("Community-acquired pneumonia — IV ceftriaxone"),
            "PULM-04": _anon("PE — therapeutic anticoagulation, monitoring"),
            "PULM-05": _anon("Pleural effusion — diagnostic thoracocentesis"),
            "PULM-06": _anon("IPF exacerbation — high-dose steroids"),
            "PULM-07": _anon("Sarcoidosis — bronchoscopy BAL planned"),
            "PULM-08": _anon("Pneumothorax — chest drain in situ"),
            "PULM-09": _anon("Lung abscess — IV antibiotics Day 7"),
            "PULM-10": _anon("Sleep apnoea — CPAP titration overnight"),
            "PULM-11": _anon("COVID-19 pneumonia — HFNC"),
            "PULM-12": _anon("Hypersensitivity pneumonitis — avoidance + steroids"),
            "PULM-13": _CLEAN,
            "PULM-14": _CLEAN,
            "PULM-15": _AVAIL,
            "PULM-16": _AVAIL,
            "PULM-17": _AVAIL,
            "PULM-18": _AVAIL,
        },
    },

    # ── Gastroenterology (16 beds) ───────────────────────────────────────────
    "Gastroenterology": {
        "capacity": 16,
        "bed_type": "general",
        "floor": "3",
        "nurse_station": "GI Ward 3E",
        "beds": {
            "GI-01": _anon("Upper GI bleed — post-OGD banding, PPI infusion"),
            "GI-02": _anon("Acute pancreatitis (APACHE II 8) — IV fluids, nil by mouth"),
            "GI-03": _anon("Crohn's disease flare — IV steroids + TPN"),
            "GI-04": _anon("Acute liver failure — NAC infusion, hepatology review"),
            "GI-05": _anon("C. difficile colitis — oral vancomycin"),
            "GI-06": _anon("Oesophageal varices — octreotide infusion + banding"),
            "GI-07": _anon("Ascending cholangitis — ERCP planned"),
            "GI-08": _anon("Hepatic encephalopathy — lactulose, rifaximin"),
            "GI-09": _anon("Ulcerative colitis — infliximab rescue"),
            "GI-10": _anon("Gastroparesis — erythromycin + dietary"),
            "GI-11": _CLEAN,
            "GI-12": _AVAIL,
            "GI-13": _AVAIL,
            "GI-14": _AVAIL,
            "GI-15": _AVAIL,
            "GI-16": _AVAIL,
        },
    },

    # ── Infectious Diseases (12 beds, 4 isolation) ───────────────────────────
    "Infectious_Diseases": {
        "capacity": 12,
        "bed_type": "isolation",
        "floor": "2",
        "nurse_station": "ID Ward 2B (Negative Pressure)",
        "beds": {
            "ID-01": _anon("Pulmonary TB — HRZE Day 14, negative-pressure isolation"),
            "ID-02": _anon("MRSA bacteraemia — IV vancomycin Day 5"),
            "ID-03": _anon("Sepsis — source control achieved, antibiotics de-escalation"),
            "ID-04": _anon("Candida septicaemia — IV micafungin"),
            "ID-05": _occ("P009", "HIV with PCP — IV co-trimoxazole, new ART counselling", "2026-02-19 16:00"),
            "ID-06": _anon("CMV retinitis — IV ganciclovir"),
            "ID-07": _anon("Leptospirosis — IV penicillin"),
            "ID-08": _anon("Viral encephalitis — IV acyclovir + PCR pending"),
            "ID-09": _CLEAN,
            "ID-10": _AVAIL,
            "ID-11": _AVAIL,
            "ID-12": _AVAIL,
        },
    },

    # ── Neurosurgery (12 beds) ───────────────────────────────────────────────
    "Neurosurgery": {
        "capacity": 12,
        "bed_type": "surgical",
        "floor": "5",
        "nurse_station": "Neurosurg Ward 5C",
        "beds": {
            "NS-01": _anon("Spontaneous ICH — craniotomy evacuation post-op Day 2"),
            "NS-02": _anon("Cerebral aneurysm — post-clipping Day 3"),
            "NS-03": _anon("Spinal cord compression — laminectomy post-op"),
            "NS-04": _anon("Meningioma — post-resection Day 1"),
            "NS-05": _anon("Hydrocephalus — VP shunt revision post-op"),
            "NS-06": _anon("Glioblastoma — post-debulking Day 4"),
            "NS-07": _anon("Lumbar disc herniation — microdiscectomy post-op"),
            "NS-08": _anon("Traumatic SDH — conservative ICP monitoring"),
            "NS-09": _CLEAN,
            "NS-10": _AVAIL,
            "NS-11": _AVAIL,
            "NS-12": _AVAIL,
        },
    },

    # ── Cardiothoracic Surgery (10 beds) ─────────────────────────────────────
    "Cardiothoracic_Surgery": {
        "capacity": 10,
        "bed_type": "surgical",
        "floor": "2",
        "nurse_station": "CTS Ward 2A (Step-Down)",
        "beds": {
            "CTS-01": _anon("CABG ×3 post-op Day 3 — chest drain removed"),
            "CTS-02": _anon("Aortic valve replacement (SAVR) post-op Day 2"),
            "CTS-03": _anon("Mitral valve repair post-op — anticoagulation"),
            "CTS-04": _anon("Aortic root replacement (Bentall) — monitoring"),
            "CTS-05": _anon("Type A aortic dissection — post-emergency repair Day 4"),
            "CTS-06": _anon("LVAD implant — post-op device check Day 1"),
            "CTS-07": _anon("Heart transplant — post-op immunosuppression protocol"),
            "CTS-08": _CLEAN,
            "CTS-09": _AVAIL,
            "CTS-10": _AVAIL,
        },
    },

    # ── Hematology (14 beds) ─────────────────────────────────────────────────
    "Hematology": {
        "capacity": 14,
        "bed_type": "general",
        "floor": "6",
        "nurse_station": "Haem Ward 6C",
        "beds": {
            "HEM-01": _anon("AML induction — Day 21 bone marrow biopsy pending"),
            "HEM-02": _anon("Sickle cell vaso-occlusive crisis — analgesia + hydration"),
            "HEM-03": _anon("ITP — IV methylprednisolone + IVIG"),
            "HEM-04": _anon("CLL — ibrutinib toxicity management"),
            "HEM-05": _anon("Lymphoma — BEACOPP cycle 3, nadir watch"),
            "HEM-06": _anon("Multiple myeloma — bortezomib neuropathy assessment"),
            "HEM-07": _anon("Haemophilia A — factor VIII infusion"),
            "HEM-08": _anon("Aplastic anaemia — cyclosporin uptitration"),
            "HEM-09": _anon("PE with HIT — argatroban bridge"),
            "HEM-10": _CLEAN,
            "HEM-11": _AVAIL,
            "HEM-12": _AVAIL,
            "HEM-13": _AVAIL,
            "HEM-14": _AVAIL,
        },
    },

    # ── Rehabilitation (20 beds) ─────────────────────────────────────────────
    "Rehabilitation": {
        "capacity": 20,
        "bed_type": "rehab",
        "floor": "7",
        "nurse_station": "Rehab Ward 7A",
        "beds": {
            "REHAB-01": _anon("Post-stroke rehab — Day 8, speech + physio"),
            "REHAB-02": _anon("TKR rehab — Day 5, gait training"),
            "REHAB-03": _anon("Spinal cord injury — T6 complete, FES programme"),
            "REHAB-04": _anon("Post-CABG cardiac rehab — Day 12"),
            "REHAB-05": _anon("Traumatic brain injury — cognitive rehab"),
            "REHAB-06": _anon("Guillain-Barré — respiratory rehab, limb strengthening"),
            "REHAB-07": _anon("Amputation — lower limb, prosthetic fitting"),
            "REHAB-08": _anon("Hip fracture post-THR — functional rehab"),
            "REHAB-09": _anon("Severe ARDS survivor — pulmonary rehab"),
            "REHAB-10": _anon("Post-stroke — dysphagia, modified diet"),
            "REHAB-11": _anon("Multiple sclerosis — fatigue management programme"),
            "REHAB-12": _anon("Parkinson's — LSVT BIG & LOUD therapy"),
            "REHAB-13": _anon("Brachial plexus injury — OT + physiotherapy"),
            "REHAB-14": _anon("Post-ICU weakness — weaning ventilator dependency"),
            "REHAB-15": _CLEAN,
            "REHAB-16": _CLEAN,
            "REHAB-17": _AVAIL,
            "REHAB-18": _AVAIL,
            "REHAB-19": _AVAIL,
            "REHAB-20": _AVAIL,
        },
    },

    # ── Vascular Surgery (10 beds) ───────────────────────────────────────────
    "Vascular_Surgery": {
        "capacity": 10,
        "bed_type": "surgical",
        "floor": "4",
        "nurse_station": "Vascular Ward 4D",
        "beds": {
            "VS-01": _anon("AAA endovascular repair (EVAR) — post-op Day 2"),
            "VS-02": _anon("Critical limb ischaemia — fem-pop bypass post-op"),
            "VS-03": _anon("Carotid endarterectomy — post-op, neuro obs"),
            "VS-04": _anon("Acute limb ischaemia — embolectomy post-op Day 1"),
            "VS-05": _anon("Diabetic foot — IV antibiotics + wound VAC"),
            "VS-06": _anon("Aorto-iliac occlusion — stent graft post-op"),
            "VS-07": _anon("DVT — catheter-directed thrombolysis"),
            "VS-08": _CLEAN,
            "VS-09": _AVAIL,
            "VS-10": _AVAIL,
        },
    },
}


# =============================================================================
# WAITLIST (priority queue per ward)
# =============================================================================
_WAITLIST: dict[str, list] = {ward: [] for ward in _BED_DB}

# =============================================================================
# ADMISSION LOG (audit trail)
# =============================================================================
_ADMISSION_LOG: list[dict] = []


# =============================================================================
# HELPERS
# =============================================================================

def _count_beds(ward_data: dict) -> tuple[int, int, int, int]:
    """Returns (occupied, cleaning, maintenance, available) counts."""
    occ = cln = mnt = avl = 0
    for bed in ward_data["beds"].values():
        s = bed["status"]
        if s == "occupied":
            occ += 1
        elif s == "cleaning":
            cln += 1
        elif s == "maintenance":
            mnt += 1
        else:
            avl += 1
    return occ, cln, mnt, avl


def _find_patient_bed(patient_id: str) -> tuple[Optional[str], Optional[str]]:
    """Finds (ward_name, bed_id) for a patient. Returns (None, None) if not found."""
    for ward_name, ward_data in _BED_DB.items():
        for bed_id, bed in ward_data["beds"].items():
            if bed["patient_id"] == patient_id:
                return ward_name, bed_id
    return None, None


def _first_available_bed(ward_name: str) -> Optional[str]:
    """Returns the first available bed_id in a ward, or None."""
    ward = _BED_DB.get(ward_name)
    if not ward:
        return None
    for bed_id, bed in ward["beds"].items():
        if bed["status"] == "available":
            return bed_id
    return None


def _normalise_ward(ward: str) -> Optional[str]:
    """Case-insensitive, space/hyphen-tolerant ward name lookup."""
    normalised = ward.strip().replace(" ", "_").replace("-", "_")
    for key in _BED_DB:
        if key.lower() == normalised.lower():
            return key
    return None


def _log_event(event_type: str, patient_id: str, ward: str, bed_id: str,
               details: str) -> None:
    _ADMISSION_LOG.append({
        "event_type": event_type,
        "patient_id": patient_id,
        "ward": ward,
        "bed_id": bed_id,
        "details": details,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })


# =============================================================================
# TOOL FUNCTIONS
# =============================================================================

def get_hospital_dashboard() -> dict:
    """Generates a real-time hospital-wide bed management dashboard.

    Displays occupancy across all 20 inpatient wards as a formatted markdown
    table with colour-coded status counts and hospital-level statistics.
    Always call this to give a full hospital capacity overview.

    Returns:
        dict: Dashboard markdown string, per-ward statistics, and hospital-level
              summary including total capacity, occupancy rate, and ward alerts.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    total_cap = total_occ = total_cln = total_mnt = total_avl = 0
    rows = []
    critical_wards = []

    for ward_name, ward_data in _BED_DB.items():
        occ, cln, mnt, avl = _count_beds(ward_data)
        cap = ward_data["capacity"]
        pct = round((occ / cap) * 100) if cap else 0
        total_cap += cap
        total_occ += occ
        total_cln += cln
        total_mnt += mnt
        total_avl += avl

        display = ward_name.replace("_", " ")
        alert = " ⚠️" if pct >= 90 else ""
        rows.append(
            f"| {display:<25} | {cap:^7} | {occ:^11} | {cln:^11} | {mnt:^8} | {avl:^12} | {pct:>4}%{alert:<3} |"
        )
        if pct >= 90:
            critical_wards.append(f"{display} ({pct}%)")

    total_pct = round((total_occ / total_cap) * 100) if total_cap else 0
    waitlist_total = sum(len(wl) for wl in _WAITLIST.values())

    header = (
        f"\n## 🏥 AGENTIC HOSPITAL — BED MANAGEMENT DASHBOARD\n"
        f"**Date:** {now}  |  "
        f"**Total Capacity:** {total_cap}  |  "
        f"**Occupied:** {total_occ}  |  "
        f"**Available:** {total_avl}  |  "
        f"**Occupancy:** {total_pct}%  |  "
        f"**Waitlist:** {waitlist_total} patient(s)\n\n"
    )

    table_header = (
        "| Ward                      | Capacity | 🔴 Occupied | 🟡 Cleaning | 🔧 Maint | 🟢 Available | Occ%    |\n"
        "|---------------------------|----------|-------------|-------------|----------|--------------|---------|"
    )
    totals_row = (
        f"| **{'HOSPITAL TOTAL':<25}** | **{total_cap:^7}** | **{total_occ:^11}** | "
        f"**{total_cln:^11}** | **{total_mnt:^8}** | **{total_avl:^12}** | **{total_pct}%**  |"
    )

    dashboard_md = header + table_header + "\n" + "\n".join(rows) + "\n|" + "-" * 95 + "|\n" + totals_row

    alerts = []
    if critical_wards:
        alerts.append(f"⚠️ **Near-capacity wards (≥90%):** {', '.join(critical_wards)}")
    if waitlist_total:
        alerts.append(f"📋 **{waitlist_total} patient(s) on waitlist** — check `get_waitlist_status` for details.")
    if total_pct >= 85:
        alerts.append("🚨 **Hospital approaching capacity** — consider escalation protocols.")

    return {
        "status": "success",
        "dashboard_markdown": dashboard_md,
        "alerts": alerts,
        "hospital_statistics": {
            "total_capacity": total_cap,
            "total_occupied": total_occ,
            "total_available": total_avl,
            "total_cleaning": total_cln,
            "total_maintenance": total_mnt,
            "overall_occupancy_pct": total_pct,
            "waitlist_total": waitlist_total,
            "critical_wards": critical_wards,
        },
        "timestamp": now,
        "note": (
            "Render `dashboard_markdown` in your response. "
            "Outpatient-only services (Radiology, Pathology, Nuclear Medicine, "
            "Anaesthesiology, Radiation Oncology) do not have inpatient ward beds."
        ),
    }


def get_ward_visualization(ward: str) -> dict:
    """Generates an ASCII floor-plan visualisation for a specific inpatient ward.

    Shows every bed with its status, occupying patient (name + diagnosis),
    and admission time. Use after any bed state change to confirm the update.

    Args:
        ward: Ward name (e.g., 'ICU', 'Cardiology', 'General_Medicine').
              Case-insensitive; spaces and hyphens are accepted.

    Returns:
        dict: ASCII ward map string, bed-level detail list, and occupancy summary.
    """
    ward_key = _normalise_ward(ward)
    if not ward_key:
        available = list(_BED_DB.keys())
        return {
            "status": "not_found",
            "message": f"Ward '{ward}' not recognised.",
            "available_wards": available,
        }

    ward_data = _BED_DB[ward_key]
    occ, cln, mnt, avl = _count_beds(ward_data)
    cap = ward_data["capacity"]
    pct = round((occ / cap) * 100) if cap else 0
    display_name = ward_key.replace("_", " ")
    waitlist_count = len(_WAITLIST.get(ward_key, []))

    STATUS_ICONS = {
        "occupied":    "🔴 OCCUPIED  ",
        "available":   "🟢 AVAILABLE ",
        "cleaning":    "🟡 CLEANING  ",
        "maintenance": "🔧 MAINT     ",
    }

    width = 66
    border_top    = "╔" + "═" * width + "╗"
    border_mid    = "╠" + "═" * width + "╣"
    border_bot    = "╚" + "═" * width + "╝"
    border_inner  = "║" + "─" * width + "║"

    def row(text: str) -> str:
        return f"║  {text:<{width - 2}}║"

    lines = [border_top]
    title = f"🏥 {display_name} Ward — Agentic Hospital"
    sub   = f"Floor {ward_data['floor']} | Nurse Station: {ward_data['nurse_station']}"
    occ_line = f"Beds: {cap} total | 🔴 {occ} occupied | 🟡 {cln} cleaning | 🟢 {avl} available ({pct}% occupancy)"
    lines += [row(title), row(sub), border_mid, row(occ_line), border_mid]

    beds_detail = []
    for bed_id, bed in ward_data["beds"].items():
        icon = STATUS_ICONS.get(bed["status"], "❓ UNKNOWN    ")
        lines.append(row(f"[{bed_id}] {icon}│ {bed['patient_name'] or 'Empty'}"))
        if bed["status"] == "occupied":
            if bed["diagnosis"]:
                lines.append(row(f"{'':>16}   │ Dx: {bed['diagnosis'][:42]}"))
            if bed["admitted"]:
                lines.append(row(f"{'':>16}   │ Admitted: {bed['admitted']}"))
        elif bed["notes"]:
            lines.append(row(f"{'':>16}   │ {bed['notes']}"))
        lines.append(border_inner)
        beds_detail.append({
            "bed_id": bed_id,
            "status": bed["status"],
            "patient_id": bed["patient_id"],
            "patient_name": bed["patient_name"],
            "diagnosis": bed["diagnosis"],
            "admitted": bed["admitted"],
        })

    if lines and lines[-1] == border_inner:
        lines[-1] = border_bot
    else:
        lines.append(border_bot)

    # Footer
    footer_parts = [f"Occupancy: {occ}/{cap}"]
    if avl:
        footer_parts.append(f"Available now: {avl}")
    if waitlist_count:
        footer_parts.append(f"In queue: {waitlist_count} patient(s)")
    lines.append("  " + "  |  ".join(footer_parts))

    return {
        "status": "success",
        "ward": ward_key,
        "ward_map": "\n".join(lines),
        "beds_detail": beds_detail,
        "summary": {
            "capacity": cap,
            "occupied": occ,
            "available": avl,
            "cleaning": cln,
            "maintenance": mnt,
            "occupancy_pct": pct,
            "waitlist": waitlist_count,
        },
        "note": "Render `ward_map` verbatim inside a code block in your response for best display.",
    }


def check_bed_availability(ward: str = "all") -> dict:
    """Checks bed availability for one specific ward or across all wards.

    Use before attempting admission to confirm capacity. Returns counts and
    lists of available bed IDs for precise allocation planning.

    Args:
        ward: Ward name to check (e.g., 'ICU', 'Cardiology'), or 'all'
              for a hospital-wide summary (default).

    Returns:
        dict: Available bed counts and IDs, occupancy percentage, and
              waitlist size for the requested ward(s).
    """
    if ward.lower() == "all":
        result = {}
        for ward_name, ward_data in _BED_DB.items():
            occ, cln, mnt, avl = _count_beds(ward_data)
            available_ids = [bid for bid, b in ward_data["beds"].items() if b["status"] == "available"]
            result[ward_name] = {
                "capacity": ward_data["capacity"],
                "occupied": occ,
                "available": avl,
                "cleaning": cln,
                "waitlist": len(_WAITLIST.get(ward_name, [])),
                "available_bed_ids": available_ids,
                "bed_type": ward_data["bed_type"],
            }
        return {
            "status": "success",
            "scope": "all_wards",
            "ward_availability": result,
            "hospital_total_available": sum(v["available"] for v in result.values()),
        }

    ward_key = _normalise_ward(ward)
    if not ward_key:
        return {
            "status": "not_found",
            "message": f"Ward '{ward}' not recognised.",
            "available_wards": list(_BED_DB.keys()),
        }

    ward_data = _BED_DB[ward_key]
    occ, cln, mnt, avl = _count_beds(ward_data)
    available_ids = [bid for bid, b in ward_data["beds"].items() if b["status"] == "available"]
    pct = round((occ / ward_data["capacity"]) * 100)

    return {
        "status": "success",
        "ward": ward_key,
        "bed_type": ward_data["bed_type"],
        "capacity": ward_data["capacity"],
        "occupied": occ,
        "available": avl,
        "cleaning": cln,
        "maintenance": mnt,
        "occupancy_pct": pct,
        "available_bed_ids": available_ids,
        "waitlist_count": len(_WAITLIST.get(ward_key, [])),
        "can_admit": avl > 0,
        "recommendation": (
            f"✅ {avl} bed(s) available in {ward_key.replace('_',' ')}. Proceed with assign_bed."
            if avl > 0 else
            f"❌ No beds available in {ward_key.replace('_',' ')}. Use add_to_waitlist."
        ),
    }


def assign_bed(
    patient_id: str,
    ward: str,
    reason: str,
    priority: str = "routine",
) -> dict:
    """Admits a patient and assigns them to the next available bed in a ward.

    Looks up patient details from the patient registry, assigns the first
    available bed, and records the admission event. If no bed is available,
    automatically adds the patient to the priority waitlist.

    Args:
        patient_id: Patient identifier (P001–P010 or any registered ID).
        ward: Target ward name (e.g., 'ICU', 'Cardiology', 'Neurology').
        reason: Clinical reason for admission (diagnosis or chief complaint).
        priority: Admission priority — 'emergency', 'urgent', or 'routine'.

    Returns:
        dict: Bed assignment confirmation with bed_id, ward, admission time,
              or waitlist position if no bed is available.
    """
    ward_key = _normalise_ward(ward)
    if not ward_key:
        return {
            "status": "error",
            "message": f"Ward '{ward}' not recognised. Available: {list(_BED_DB.keys())}",
        }

    # Check if already admitted
    existing_ward, existing_bed = _find_patient_bed(patient_id)
    if existing_ward:
        return {
            "status": "already_admitted",
            "message": (
                f"Patient {patient_id} is already in {existing_ward} / {existing_bed}. "
                "Use transfer_patient_bed to move them."
            ),
            "current_ward": existing_ward,
            "current_bed": existing_bed,
        }

    patient = _PATIENT_DB.get(patient_id, {})
    patient_name = patient.get("name", patient_id)
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    bed_id = _first_available_bed(ward_key)
    if bed_id is None:
        # Auto-waitlist
        wl_result = add_to_waitlist(patient_id, ward_key, priority, reason)
        return {
            "status": "waitlisted",
            "message": (
                f"No beds available in {ward_key.replace('_',' ')}. "
                f"{patient_name} added to waitlist at position {wl_result.get('waitlist_position', '?')}."
            ),
            "waitlist_details": wl_result,
        }

    # Assign the bed
    _BED_DB[ward_key]["beds"][bed_id] = _make_bed(
        "occupied", patient_id, patient_name, now_str, reason,
    )

    _log_event("ADMISSION", patient_id, ward_key, bed_id,
               f"Admitted: {reason} | Priority: {priority}")

    occ, cln, mnt, avl = _count_beds(_BED_DB[ward_key])

    return {
        "status": "admitted",
        "patient_id": patient_id,
        "patient_name": patient_name,
        "bed_id": bed_id,
        "ward": ward_key,
        "floor": _BED_DB[ward_key]["floor"],
        "nurse_station": _BED_DB[ward_key]["nurse_station"],
        "bed_type": _BED_DB[ward_key]["bed_type"],
        "diagnosis_on_admission": reason,
        "priority": priority,
        "admission_time": now_str,
        "ward_occupancy_after": f"{occ}/{_BED_DB[ward_key]['capacity']}",
        "patient_allergies": patient.get("allergies", []),
        "patient_medications": patient.get("current_medications", []),
        "message": (
            f"✅ {patient_name} admitted to {ward_key.replace('_',' ')} — Bed {bed_id} "
            f"(Floor {_BED_DB[ward_key]['floor']}) at {now_str}."
        ),
        "next_action": f"Call get_ward_visualization('{ward_key}') to confirm bed assignment.",
    }


def discharge_patient_from_bed(
    patient_id: str,
    discharge_notes: str = "",
) -> dict:
    """Discharges a patient, freeing their bed for cleaning and re-allocation.

    Sets the bed status to 'cleaning' (simulating housekeeping turnover).
    Automatically checks the ward waitlist and notifies the next patient
    in queue that a bed will be available shortly.

    Args:
        patient_id: Patient identifier of the patient to discharge.
        discharge_notes: Optional discharge summary or reason for discharge.

    Returns:
        dict: Discharge confirmation with length of stay, freed bed details,
              and waitlist notification if applicable.
    """
    ward_key, bed_id = _find_patient_bed(patient_id)
    if not ward_key:
        return {
            "status": "not_found",
            "message": f"Patient '{patient_id}' is not currently admitted to any ward.",
        }

    bed = _BED_DB[ward_key]["beds"][bed_id]
    patient_name = bed["patient_name"]
    admitted_str = bed["admitted"]
    diagnosis = bed["diagnosis"]
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    # Calculate length of stay
    los_str = "Unknown"
    try:
        admitted_dt = datetime.datetime.strptime(admitted_str, "%Y-%m-%d %H:%M")
        delta = now - admitted_dt
        days = delta.days
        hours = delta.seconds // 3600
        los_str = f"{days}d {hours}h"
    except (ValueError, TypeError):
        pass

    # Free the bed → cleaning
    _BED_DB[ward_key]["beds"][bed_id] = _make_bed(
        "cleaning", notes="Post-discharge cleaning — ready ~15 min"
    )
    _log_event("DISCHARGE", patient_id, ward_key, bed_id,
               f"Discharged. LoS: {los_str}. Notes: {discharge_notes or 'None'}")

    # Check waitlist
    waitlist_notification = None
    wl = _WAITLIST.get(ward_key, [])
    if wl:
        next_patient = wl[0]
        waitlist_notification = {
            "next_patient_id": next_patient["patient_id"],
            "next_patient_name": next_patient.get("patient_name", next_patient["patient_id"]),
            "priority": next_patient["priority"],
            "reason": next_patient["reason"],
            "message": (
                f"📋 Waitlist notification: {next_patient.get('patient_name', next_patient['patient_id'])} "
                f"(priority: {next_patient['priority']}) is next in queue for {ward_key.replace('_',' ')}. "
                f"Bed {bed_id} will be ready after cleaning (~15 min). "
                "Call assign_bed to complete their admission."
            ),
        }

    occ, cln, mnt, avl = _count_beds(_BED_DB[ward_key])

    return {
        "status": "discharged",
        "patient_id": patient_id,
        "patient_name": patient_name,
        "ward": ward_key,
        "bed_id": bed_id,
        "primary_diagnosis": diagnosis,
        "discharge_time": now_str,
        "length_of_stay": los_str,
        "discharge_notes": discharge_notes or "No additional notes.",
        "bed_status_now": "cleaning",
        "ward_occupancy_after": f"{occ}/{_BED_DB[ward_key]['capacity']}",
        "waitlist_notification": waitlist_notification,
        "message": (
            f"✅ {patient_name} discharged from {ward_key.replace('_',' ')} / {bed_id} "
            f"at {now_str}. Length of stay: {los_str}. "
            f"Bed set to cleaning — available for new admission in ~15 min."
        ),
        "next_action": f"Call get_ward_visualization('{ward_key}') to see updated ward status.",
    }


def transfer_patient_bed(
    patient_id: str,
    target_ward: str,
    reason: str,
) -> dict:
    """Transfers a patient from their current bed to an available bed in a target ward.

    Frees the original bed (set to 'cleaning') and assigns the first available
    bed in the target ward. Records the inter-ward transfer in the audit log.

    Args:
        patient_id: Patient identifier of the patient to transfer.
        target_ward: Destination ward name (e.g., 'General_Medicine', 'Rehabilitation').
        reason: Clinical reason for the transfer (e.g., 'Clinically stable, step-down from ICU').

    Returns:
        dict: Transfer confirmation with old and new bed details, transfer time,
              or error if no bed is available in the target ward.
    """
    # Find current location
    source_ward, source_bed = _find_patient_bed(patient_id)
    if not source_ward:
        return {
            "status": "not_found",
            "message": f"Patient '{patient_id}' is not currently admitted to any ward.",
        }

    target_key = _normalise_ward(target_ward)
    if not target_key:
        return {
            "status": "error",
            "message": f"Target ward '{target_ward}' not recognised.",
            "available_wards": list(_BED_DB.keys()),
        }

    if source_ward == target_key:
        return {
            "status": "error",
            "message": f"Patient is already in {target_key.replace('_',' ')}. No transfer needed.",
        }

    new_bed_id = _first_available_bed(target_key)
    if new_bed_id is None:
        return {
            "status": "no_capacity",
            "message": (
                f"No available beds in {target_key.replace('_',' ')}. "
                "Call add_to_waitlist or check another ward."
            ),
            "target_ward": target_key,
        }

    bed = _BED_DB[source_ward]["beds"][source_bed]
    patient_name = bed["patient_name"]
    original_admission = bed["admitted"]
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Free source bed
    _BED_DB[source_ward]["beds"][source_bed] = _make_bed(
        "cleaning", notes=f"Post-transfer cleaning — patient moved to {target_key.replace('_',' ')}"
    )

    # Assign target bed (preserve original admission time)
    _BED_DB[target_key]["beds"][new_bed_id] = _make_bed(
        "occupied", patient_id, patient_name, original_admission, reason,
    )

    _log_event("TRANSFER", patient_id, f"{source_ward} → {target_key}",
               f"{source_bed} → {new_bed_id}", reason)

    src_occ, *_ = _count_beds(_BED_DB[source_ward])
    tgt_occ, *_ = _count_beds(_BED_DB[target_key])

    return {
        "status": "transferred",
        "patient_id": patient_id,
        "patient_name": patient_name,
        "from_ward": source_ward,
        "from_bed": source_bed,
        "to_ward": target_key,
        "to_bed": new_bed_id,
        "to_floor": _BED_DB[target_key]["floor"],
        "to_nurse_station": _BED_DB[target_key]["nurse_station"],
        "transfer_reason": reason,
        "transfer_time": now_str,
        "source_ward_occupancy_after": f"{src_occ}/{_BED_DB[source_ward]['capacity']}",
        "target_ward_occupancy_after": f"{tgt_occ}/{_BED_DB[target_key]['capacity']}",
        "message": (
            f"✅ {patient_name} transferred from {source_ward.replace('_',' ')}/{source_bed} "
            f"→ {target_key.replace('_',' ')}/{new_bed_id} (Floor {_BED_DB[target_key]['floor']}) "
            f"at {now_str}."
        ),
        "next_action": (
            f"Call get_ward_visualization('{source_ward}') and "
            f"get_ward_visualization('{target_key}') to confirm both wards."
        ),
    }


def add_to_waitlist(
    patient_id: str,
    ward: str,
    priority: str,
    reason: str,
) -> dict:
    """Adds a patient to the waitlist for a specific ward when no bed is available.

    Patients are queued by priority (emergency → urgent → routine) and then
    by arrival time within each priority tier.

    Args:
        patient_id: Patient identifier.
        ward: Desired ward name.
        priority: Admission urgency — 'emergency', 'urgent', or 'routine'.
        reason: Clinical reason for admission (used for bed assignment when a bed opens).

    Returns:
        dict: Waitlist confirmation with queue position, patients ahead,
              and estimated wait time.
    """
    ward_key = _normalise_ward(ward)
    if not ward_key:
        return {
            "status": "error",
            "message": f"Ward '{ward}' not recognised.",
            "available_wards": list(_BED_DB.keys()),
        }

    priority = priority.lower().strip()
    if priority not in _PRIORITY_ORDER:
        priority = "routine"

    patient = _PATIENT_DB.get(patient_id, {})
    patient_name = patient.get("name", patient_id)
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if already on waitlist for this ward
    wl = _WAITLIST[ward_key]
    for entry in wl:
        if entry["patient_id"] == patient_id:
            pos = wl.index(entry) + 1
            return {
                "status": "already_waitlisted",
                "message": f"{patient_name} is already on the {ward_key.replace('_',' ')} waitlist at position {pos}.",
                "waitlist_position": pos,
            }

    entry = {
        "patient_id": patient_id,
        "patient_name": patient_name,
        "priority": priority,
        "reason": reason,
        "added_at": now_str,
        "priority_order": _PRIORITY_ORDER[priority],
    }
    wl.append(entry)
    # Sort by priority then arrival time
    wl.sort(key=lambda x: (x["priority_order"], x["added_at"]))
    _WAITLIST[ward_key] = wl

    position = wl.index(entry) + 1
    ahead = position - 1
    # Estimate wait: ~45 min per patient ahead + 30 min base for cleaning
    est_minutes = 30 + (ahead * 45)
    est_hours = est_minutes // 60
    est_min_rem = est_minutes % 60
    est_wait = f"~{est_hours}h {est_min_rem}min" if est_hours else f"~{est_min_rem} min"

    return {
        "status": "waitlisted",
        "patient_id": patient_id,
        "patient_name": patient_name,
        "ward": ward_key,
        "priority": priority,
        "reason": reason,
        "waitlist_position": position,
        "patients_ahead": ahead,
        "estimated_wait": est_wait,
        "total_waitlist_size": len(wl),
        "message": (
            f"📋 {patient_name} added to {ward_key.replace('_',' ')} waitlist. "
            f"Position: {position} (priority: {priority}). "
            f"Estimated wait: {est_wait}."
        ),
    }


def get_waitlist_status(ward: str = "all") -> dict:
    """Retrieves the current waitlist for one or all wards.

    Shows patients queued for admission, ordered by priority then arrival time.

    Args:
        ward: Ward name to check, or 'all' for hospital-wide waitlist (default).

    Returns:
        dict: Waitlist entries per ward with patient details, priority,
              position, and estimated wait times.
    """
    if ward.lower() == "all":
        result = {}
        total = 0
        for ward_name, wl in _WAITLIST.items():
            if wl:
                result[ward_name] = [
                    {
                        "position": i + 1,
                        "patient_id": e["patient_id"],
                        "patient_name": e["patient_name"],
                        "priority": e["priority"],
                        "reason": e["reason"],
                        "added_at": e["added_at"],
                        "est_wait": f"~{30 + i * 45} min",
                    }
                    for i, e in enumerate(wl)
                ]
                total += len(wl)
        if not result:
            return {"status": "clear", "message": "✅ No patients on any waitlist.", "total_waiting": 0}
        return {
            "status": "waitlists_active",
            "total_waiting": total,
            "waitlists": result,
            "note": "Ordered by priority (emergency first) then arrival time.",
        }

    ward_key = _normalise_ward(ward)
    if not ward_key:
        return {"status": "error", "message": f"Ward '{ward}' not recognised."}

    wl = _WAITLIST.get(ward_key, [])
    if not wl:
        return {
            "status": "clear",
            "ward": ward_key,
            "message": f"✅ No patients waiting for {ward_key.replace('_',' ')}.",
            "total_waiting": 0,
        }

    entries = [
        {
            "position": i + 1,
            "patient_id": e["patient_id"],
            "patient_name": e["patient_name"],
            "priority": e["priority"],
            "reason": e["reason"],
            "added_at": e["added_at"],
            "est_wait": f"~{30 + i * 45} min",
        }
        for i, e in enumerate(wl)
    ]

    return {
        "status": "waitlist_active",
        "ward": ward_key,
        "total_waiting": len(wl),
        "waitlist": entries,
        "note": "Call assign_bed when a bed becomes available to admit the next patient.",
    }
