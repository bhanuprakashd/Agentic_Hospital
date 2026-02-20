"""Common tools shared across all medical department agents."""

import datetime
from typing import Optional


# =============================================================================
# PATIENT DATABASE (10 diverse patients)
# =============================================================================
_PATIENT_DB = {
    "P001": {
        "name": "John Smith",
        "age": 55,
        "gender": "Male",
        "blood_type": "A+",
        "allergies": ["Penicillin"],
        "chronic_conditions": ["Hypertension", "Type 2 Diabetes"],
        "current_medications": ["Metformin 500mg twice daily", "Lisinopril 10mg daily",
                                 "Atorvastatin 20mg daily"],
        "emergency_contact": "Jane Smith (Wife) - 555-0101",
        "insurance": "BlueCross PPO",
        "primary_care": "Dr. Williams",
    },
    "P002": {
        "name": "Sarah Johnson",
        "age": 34,
        "gender": "Female",
        "blood_type": "O-",
        "allergies": [],
        "chronic_conditions": ["PCOS", "Iron-deficiency Anemia"],
        "current_medications": ["Metformin 500mg daily", "Combined oral contraceptive pill",
                                 "Ferrous sulfate 325mg daily"],
        "emergency_contact": "Mike Johnson (Husband) - 555-0202",
        "insurance": "Aetna HMO",
        "primary_care": "Dr. Patel",
    },
    "P003": {
        "name": "Robert Chen",
        "age": 68,
        "gender": "Male",
        "blood_type": "B+",
        "allergies": ["Sulfa drugs", "Iodine contrast (mild reaction)"],
        "chronic_conditions": ["COPD (GOLD Stage II)", "Atrial Fibrillation", "Chronic Heart Failure (EF 40%)"],
        "current_medications": ["Warfarin 5mg daily", "Tiotropium 18mcg inhaler daily",
                                 "Albuterol inhaler PRN", "Metoprolol succinate 25mg daily",
                                 "Furosemide 40mg daily", "Spironolactone 25mg daily"],
        "emergency_contact": "Lisa Chen (Daughter) - 555-0303",
        "insurance": "Medicare Part B",
        "primary_care": "Dr. Garcia",
    },
    "P004": {
        "name": "Emily Davis",
        "age": 28,
        "gender": "Female",
        "blood_type": "AB+",
        "allergies": ["Latex"],
        "chronic_conditions": ["Migraines"],
        "current_medications": ["Sumatriptan 50mg PRN"],
        "emergency_contact": "Tom Davis (Father) - 555-0404",
        "insurance": "United Healthcare",
        "primary_care": "Dr. Kim",
    },
    "P005": {
        "name": "Michael Brown",
        "age": 45,
        "gender": "Male",
        "blood_type": "O+",
        "allergies": ["Aspirin (GI intolerance)", "Codeine"],
        "chronic_conditions": ["Chronic Lower Back Pain (L4-L5 disc herniation)", "Generalized Anxiety Disorder"],
        "current_medications": ["Gabapentin 300mg three times daily", "Sertraline 50mg daily",
                                 "Cyclobenzaprine 5mg PRN"],
        "emergency_contact": "Karen Brown (Wife) - 555-0505",
        "insurance": "Cigna PPO",
        "primary_care": "Dr. Thompson",
    },
    "P006": {
        "name": "Margaret Wilson",
        "age": 68,
        "gender": "Female",
        "blood_type": "A-",
        "allergies": ["NSAIDs (asthma exacerbation)"],
        "chronic_conditions": ["COPD (GOLD Stage III)", "Osteoporosis", "Major Depressive Disorder",
                                "Gastroesophageal Reflux Disease"],
        "current_medications": ["Fluticasone/Salmeterol inhaler twice daily",
                                 "Tiotropium 18mcg daily", "Albuterol PRN",
                                 "Alendronate 70mg weekly", "Escitalopram 10mg daily",
                                 "Omeprazole 20mg daily", "Calcium + Vitamin D supplement"],
        "emergency_contact": "David Wilson (Son) - 555-0606",
        "insurance": "Medicare Advantage",
        "primary_care": "Dr. Nguyen",
    },
    "P007": {
        "name": "Carlos Rivera",
        "age": 34,
        "gender": "Male",
        "blood_type": "O+",
        "allergies": ["Amoxicillin (rash)"],
        "chronic_conditions": ["Type 1 Diabetes Mellitus (since age 12)", "Diabetic Retinopathy (non-proliferative)"],
        "current_medications": ["Insulin glargine 24 units at bedtime",
                                 "Insulin lispro (bolus, carb ratio 1:10)",
                                 "Lisinopril 5mg daily", "Atorvastatin 40mg daily"],
        "emergency_contact": "Maria Rivera (Wife) - 555-0707",
        "insurance": "Kaiser Permanente",
        "primary_care": "Dr. Okonkwo",
    },
    "P008": {
        "name": "Linda Park",
        "age": 55,
        "gender": "Female",
        "blood_type": "B-",
        "allergies": ["Sulfonamides", "Fluoroquinolones (tendinopathy)"],
        "chronic_conditions": ["Systemic Lupus Erythematosus (SLE)", "Lupus Nephritis (Class III)",
                                "Hypertension", "Secondary Sjögren's Syndrome"],
        "current_medications": ["Hydroxychloroquine 200mg twice daily",
                                 "Mycophenolate mofetil 1500mg twice daily",
                                 "Prednisone 10mg daily", "Amlodipine 5mg daily",
                                 "Losartan 50mg daily", "Belimumab 200mg SC monthly",
                                 "Calcium + Vitamin D", "Trimethoprim-sulfamethoxazole (PCP prophylaxis)"],
        "emergency_contact": "James Park (Husband) - 555-0808",
        "insurance": "BlueCross PPO",
        "primary_care": "Dr. Ramirez",
    },
    "P009": {
        "name": "Andre Williams",
        "age": 45,
        "gender": "Male",
        "blood_type": "A+",
        "allergies": ["Abacavir (HLA-B*5701 positive — absolute contraindication)"],
        "chronic_conditions": ["HIV-1 (undetectable viral load on ART)",
                                "Generalized Anxiety Disorder", "Hepatitis B co-infection (treated)"],
        "current_medications": ["Bictegravir/emtricitabine/tenofovir alafenamide (Biktarvy) once daily",
                                 "Sertraline 100mg daily"],
        "emergency_contact": "Patricia Williams (Sister) - 555-0909",
        "insurance": "Medicaid",
        "primary_care": "Dr. Hassan",
    },
    "P010": {
        "name": "George Thompson",
        "age": 72,
        "gender": "Male",
        "blood_type": "AB+",
        "allergies": ["ACE inhibitors (angioedema — use ARB instead)", "Clopidogrel (poor metabolizer, CYP2C19)"],
        "chronic_conditions": ["Post-CABG (3-vessel, 3 years ago)", "Persistent Atrial Fibrillation",
                                "Systolic Heart Failure (EF 35%)", "CKD Stage 3b (eGFR 34 mL/min)",
                                "Type 2 Diabetes", "Hypertension"],
        "current_medications": ["Warfarin 7.5mg daily (INR target 2.0–3.0)",
                                 "Amiodarone 200mg daily",
                                 "Carvedilol 12.5mg twice daily",
                                 "Losartan 100mg daily",
                                 "Furosemide 80mg daily",
                                 "Spironolactone 25mg daily",
                                 "Insulin glargine 30 units nightly",
                                 "Atorvastatin 40mg daily",
                                 "Aspirin 81mg daily"],
        "emergency_contact": "Helen Thompson (Wife) - 555-1010",
        "insurance": "Medicare + Medigap",
        "primary_care": "Dr. Fernandez",
    },
}


# =============================================================================
# LAB RESULTS DATABASE (full panels for all 10 patients)
# =============================================================================
_LAB_DB = {
    "P001": {
        "CBC": {"WBC": 7.2, "RBC": 4.8, "Hemoglobin": 14.5, "Hematocrit": 43.2,
                "MCV": 88, "Platelets": 250, "status": "Normal"},
        "BMP": {"Glucose": 148, "BUN": 19, "Creatinine": 1.1, "eGFR": 68,
                "Sodium": 140, "Potassium": 4.2, "Chloride": 102, "CO2": 24,
                "Calcium": 9.2, "status": "Glucose mildly elevated"},
        "Lipid Panel": {"Total_Cholesterol": 238, "LDL": 158, "HDL": 42,
                        "Triglycerides": 192, "status": "Elevated LDL and Triglycerides"},
        "HbA1c": {"value": 7.4, "unit": "%", "status": "Above target (goal <7.0 for most T2DM)"},
        "LFTs": {"ALT": 28, "AST": 24, "Alk_Phos": 82, "Total_Bilirubin": 0.8,
                 "Albumin": 4.1, "status": "Normal"},
        "TSH": {"value": 2.1, "unit": "mIU/L", "status": "Normal (0.4–4.0)"},
        "Urine_Microalbumin": {"value": 42, "unit": "mg/g creatinine",
                               "status": "Microalbuminuria — early diabetic nephropathy"},
    },
    "P002": {
        "CBC": {"WBC": 6.8, "RBC": 4.0, "Hemoglobin": 10.8, "Hematocrit": 32.5,
                "MCV": 72, "MCH": 21, "Platelets": 310, "status": "Microcytic anemia (iron deficiency)"},
        "BMP": {"Glucose": 92, "BUN": 12, "Creatinine": 0.7, "eGFR": ">60",
                "Sodium": 138, "Potassium": 3.9, "Chloride": 101, "CO2": 25,
                "Calcium": 9.0, "status": "Normal"},
        "Iron_Studies": {"Serum_Iron": 42, "TIBC": 480, "Ferritin": 6, "Transferrin_Sat": 9,
                         "status": "Iron deficiency confirmed"},
        "Hormone_Panel": {"FSH": 6.2, "LH": 8.4, "Testosterone_total": 68, "DHEA_S": 210,
                          "Prolactin": 12, "status": "Androgens mildly elevated — consistent with PCOS"},
        "LFTs": {"ALT": 22, "AST": 18, "Alk_Phos": 74, "Total_Bilirubin": 0.6,
                 "Albumin": 4.3, "status": "Normal"},
        "TSH": {"value": 1.8, "unit": "mIU/L", "status": "Normal"},
    },
    "P003": {
        "CBC": {"WBC": 6.5, "RBC": 4.0, "Hemoglobin": 12.4, "Hematocrit": 37.8,
                "MCV": 90, "Platelets": 172, "status": "Normocytic mild anemia (chronic disease)"},
        "BMP": {"Glucose": 102, "BUN": 24, "Creatinine": 1.4, "eGFR": 52,
                "Sodium": 137, "Potassium": 4.6, "Chloride": 100, "CO2": 26,
                "Calcium": 9.0, "status": "CKD Stage 3a; borderline potassium"},
        "INR": {"value": 2.4, "therapeutic_range": "2.0–3.0", "status": "Therapeutic — AF on Warfarin"},
        "BNP": {"value": 420, "unit": "pg/mL", "status": "Elevated — heart failure monitoring"},
        "LFTs": {"ALT": 30, "AST": 27, "Alk_Phos": 88, "Total_Bilirubin": 1.1,
                 "Albumin": 3.7, "status": "Mild hypoalbuminemia"},
        "PFTs": {"FEV1": 1.52, "FVC": 2.80, "FEV1_FVC_ratio": 0.54,
                 "FEV1_percent_predicted": 52, "DLCO_percent": 58,
                 "status": "Moderate obstructive pattern consistent with GOLD II/III COPD"},
        "Lipid_Panel": {"Total_Cholesterol": 195, "LDL": 110, "HDL": 38,
                        "Triglycerides": 235, "status": "Low HDL, high TG — metabolic concern"},
    },
    "P004": {
        "CBC": {"WBC": 7.0, "RBC": 4.6, "Hemoglobin": 13.2, "Hematocrit": 39.8,
                "MCV": 85, "Platelets": 265, "status": "Normal"},
        "BMP": {"Glucose": 88, "BUN": 10, "Creatinine": 0.8, "eGFR": ">60",
                "Sodium": 139, "Potassium": 4.0, "Chloride": 103, "CO2": 25,
                "Calcium": 9.3, "status": "Normal"},
        "LFTs": {"ALT": 19, "AST": 16, "Alk_Phos": 68, "Total_Bilirubin": 0.5,
                 "Albumin": 4.4, "status": "Normal"},
        "TSH": {"value": 1.5, "unit": "mIU/L", "status": "Normal"},
        "Urine_Pregnancy_Test": {"value": "Negative", "status": "Not pregnant"},
    },
    "P005": {
        "CBC": {"WBC": 7.8, "RBC": 4.9, "Hemoglobin": 15.1, "Hematocrit": 44.8,
                "MCV": 87, "Platelets": 235, "status": "Normal"},
        "BMP": {"Glucose": 96, "BUN": 14, "Creatinine": 1.0, "eGFR": ">60",
                "Sodium": 141, "Potassium": 4.1, "Chloride": 104, "CO2": 24,
                "Calcium": 9.4, "status": "Normal"},
        "LFTs": {"ALT": 32, "AST": 28, "Alk_Phos": 78, "Total_Bilirubin": 0.7,
                 "Albumin": 4.2, "status": "Normal"},
        "TSH": {"value": 2.4, "unit": "mIU/L", "status": "Normal"},
        "Drug_Screen": {"Gabapentin": "Therapeutic", "Sertraline": "Therapeutic",
                        "Illicit_substances": "Not detected", "status": "Compliant with prescribed medications"},
    },
    "P006": {
        "CBC": {"WBC": 7.4, "RBC": 3.8, "Hemoglobin": 11.6, "Hematocrit": 35.0,
                "MCV": 88, "Platelets": 198, "status": "Mild normocytic anemia (chronic disease/COPD)"},
        "BMP": {"Glucose": 105, "BUN": 20, "Creatinine": 1.0, "eGFR": 62,
                "Sodium": 138, "Potassium": 4.3, "Chloride": 101, "CO2": 28,
                "Calcium": 9.1, "status": "Mildly elevated CO2 — CO2 retention (COPD)"},
        "PFTs": {"FEV1": 0.98, "FVC": 1.85, "FEV1_FVC_ratio": 0.53,
                 "FEV1_percent_predicted": 38, "DLCO_percent": 44,
                 "status": "Severe obstructive pattern — GOLD Stage III COPD"},
        "DEXA_Scan": {"Lumbar_T_score": -2.6, "Femoral_neck_T_score": -2.4,
                      "status": "Osteoporosis — T-score below -2.5"},
        "LFTs": {"ALT": 24, "AST": 20, "Alk_Phos": 92, "Total_Bilirubin": 0.9,
                 "Albumin": 3.6, "status": "Mild hypoalbuminemia"},
        "TSH": {"value": 3.8, "unit": "mIU/L", "status": "High-normal — monitor"},
        "VitD_25OH": {"value": 18, "unit": "ng/mL", "status": "Insufficient (<20 ng/mL) — supplement"},
        "PHQ9_Score": {"value": 14, "status": "Moderate depression — optimize antidepressant"},
    },
    "P007": {
        "CBC": {"WBC": 6.9, "RBC": 4.7, "Hemoglobin": 14.8, "Hematocrit": 43.0,
                "MCV": 86, "Platelets": 242, "status": "Normal"},
        "BMP": {"Glucose": 168, "BUN": 15, "Creatinine": 0.9, "eGFR": ">60",
                "Sodium": 139, "Potassium": 4.0, "Chloride": 102, "CO2": 23,
                "Calcium": 9.2, "status": "Glucose elevated — T1DM suboptimal control"},
        "HbA1c": {"value": 8.1, "unit": "%", "status": "Above target (goal <7.0–7.5 for T1DM) — intensify regimen"},
        "Lipid_Panel": {"Total_Cholesterol": 185, "LDL": 98, "HDL": 55,
                        "Triglycerides": 160, "status": "Borderline LDL — already on statin"},
        "LFTs": {"ALT": 26, "AST": 22, "Alk_Phos": 75, "Total_Bilirubin": 0.6,
                 "Albumin": 4.3, "status": "Normal"},
        "Urine_Microalbumin": {"value": 35, "unit": "mg/g creatinine",
                               "status": "Microalbuminuria — early diabetic nephropathy"},
        "Retinal_Exam": {"finding": "Non-proliferative diabetic retinopathy (NPDR), mild",
                         "status": "Annual ophthalmology follow-up required"},
        "TSH": {"value": 2.0, "unit": "mIU/L", "status": "Normal"},
    },
    "P008": {
        "CBC": {"WBC": 3.8, "RBC": 3.5, "Hemoglobin": 10.2, "Hematocrit": 30.5,
                "MCV": 84, "Platelets": 98,
                "status": "Leukopenia + thrombocytopenia — immunosuppression / SLE-related"},
        "BMP": {"Glucose": 118, "BUN": 28, "Creatinine": 1.6, "eGFR": 38,
                "Sodium": 136, "Potassium": 4.8, "Chloride": 99, "CO2": 22,
                "Calcium": 8.8, "status": "CKD Stage 3b (lupus nephritis) — close monitoring"},
        "Immunology": {"ANA": "Positive (1:320 speckled)", "Anti_dsDNA": 245,
                       "Anti_Smith": "Positive", "Complement_C3": 62, "Complement_C4": 8,
                       "status": "Active lupus serology — flare markers elevated"},
        "Urinalysis": {"Protein": "3+", "RBC_casts": "Present", "WBC": "5–10/hpf",
                       "status": "Active nephritis — nephrotic range proteinuria with casts"},
        "Urine_Protein_Creatinine": {"ratio": 2.8, "unit": "g/g",
                                     "status": "Nephrotic range (>3.5 g/day equivalent)"},
        "LFTs": {"ALT": 34, "AST": 29, "Alk_Phos": 96, "Total_Bilirubin": 1.2,
                 "Albumin": 2.9, "status": "Hypoalbuminemia — nephrotic syndrome"},
        "DEXA_Scan": {"Lumbar_T_score": -1.8, "Femoral_neck_T_score": -1.6,
                      "status": "Osteopenia — chronic steroid use risk"},
    },
    "P009": {
        "CBC": {"WBC": 5.8, "RBC": 4.5, "Hemoglobin": 13.6, "Hematocrit": 40.2,
                "MCV": 92, "Platelets": 210, "status": "Normal — HIV well-controlled"},
        "BMP": {"Glucose": 94, "BUN": 13, "Creatinine": 1.0, "eGFR": ">60",
                "Sodium": 140, "Potassium": 4.1, "Chloride": 103, "CO2": 25,
                "Calcium": 9.3, "status": "Normal"},
        "HIV_Panel": {"CD4_count": 620, "CD4_percent": 32, "Viral_Load": "<20 copies/mL",
                      "status": "Excellent HIV control — virologically suppressed"},
        "Hepatitis_B": {"HBsAg": "Negative", "Anti_HBs": "Positive (>10 mIU/mL)",
                        "HBV_DNA": "Undetectable", "status": "HBV suppressed on TAF-containing regimen"},
        "LFTs": {"ALT": 38, "AST": 32, "Alk_Phos": 84, "Total_Bilirubin": 0.9,
                 "Albumin": 4.1, "status": "Mildly elevated transaminases — monitor (TAF/HBV)"},
        "Lipid_Panel": {"Total_Cholesterol": 215, "LDL": 130, "HDL": 48,
                        "Triglycerides": 185, "status": "Borderline elevated LDL — consider statin"},
        "STI_Screen": {"Syphilis_RPR": "Non-reactive", "Gonorrhea": "Negative",
                       "Chlamydia": "Negative", "status": "Negative — routine annual screening"},
    },
    "P010": {
        "CBC": {"WBC": 7.1, "RBC": 4.1, "Hemoglobin": 12.8, "Hematocrit": 38.5,
                "MCV": 89, "Platelets": 188,
                "status": "Mild anemia of chronic disease; platelets low-normal"},
        "BMP": {"Glucose": 154, "BUN": 38, "Creatinine": 1.9, "eGFR": 34,
                "Sodium": 138, "Potassium": 5.1, "Chloride": 100, "CO2": 23,
                "Calcium": 8.9, "status": "CKD 3b; hyperglycemia; borderline high potassium (Warfarin + Losartan + Spiro)"},
        "INR": {"value": 3.8, "therapeutic_range": "2.0–3.0",
                "status": "SUPRATHERAPEUTIC — increased bleeding risk; Warfarin dose adjustment needed"},
        "BNP": {"value": 890, "unit": "pg/mL",
                "status": "Significantly elevated — heart failure decompensation risk"},
        "HbA1c": {"value": 8.6, "unit": "%", "status": "Poorly controlled T2DM — intensify insulin regimen"},
        "Lipid_Panel": {"Total_Cholesterol": 178, "LDL": 88, "HDL": 36,
                        "Triglycerides": 270, "status": "LDL at goal on statin; high TG — dietary counseling"},
        "LFTs": {"ALT": 36, "AST": 31, "Alk_Phos": 98, "Total_Bilirubin": 1.4,
                 "Albumin": 3.5, "status": "Borderline hypoalbuminemia — heart failure/CKD"},
        "Thyroid": {"TSH": 2.8, "status": "Normal — Amiodarone can suppress TSH; monitor every 6 months"},
        "Echo_Summary": {"EF": 35, "LV_dilation": "Moderate", "Wall_motion": "Diffuse hypokinesis",
                         "status": "Systolic dysfunction — optimize GDMT"},
    },
}


# =============================================================================
# DRUG INTERACTION DATABASE (150+ entries)
# =============================================================================
_DRUG_INTERACTIONS: dict[tuple, dict] = {
    # ---- WARFARIN interactions ----
    ("Warfarin", "Aspirin"):           {"severity": "HIGH",     "effect": "Increased bleeding risk. Avoid unless specifically indicated (e.g., mechanical heart valve)."},
    ("Warfarin", "Ibuprofen"):         {"severity": "HIGH",     "effect": "Increased bleeding risk + GI mucosal damage. Avoid NSAIDs; use acetaminophen."},
    ("Warfarin", "Naproxen"):          {"severity": "HIGH",     "effect": "Increased bleeding risk. Avoid concurrent use."},
    ("Warfarin", "Amiodarone"):        {"severity": "HIGH",     "effect": "Amiodarone inhibits CYP2C9 — dramatically increases INR. Reduce Warfarin 30–50%. Monitor weekly."},
    ("Warfarin", "Fluconazole"):       {"severity": "HIGH",     "effect": "CYP2C9 inhibition — major INR elevation. Reduce Warfarin dose and monitor closely."},
    ("Warfarin", "Metronidazole"):     {"severity": "HIGH",     "effect": "CYP2C9 inhibition — increases INR significantly. Monitor INR every 2–3 days."},
    ("Warfarin", "Ciprofloxacin"):     {"severity": "HIGH",     "effect": "Potentiates Warfarin effect; INR may rise significantly."},
    ("Warfarin", "Clarithromycin"):    {"severity": "HIGH",     "effect": "CYP3A4 inhibition + gut flora alteration — INR elevation."},
    ("Warfarin", "Trimethoprim"):      {"severity": "HIGH",     "effect": "Inhibits Warfarin metabolism; monitor INR frequently."},
    ("Warfarin", "Sertraline"):        {"severity": "MODERATE", "effect": "Mild CYP2C9 inhibition — may increase INR. Monitor."},
    ("Warfarin", "Fluoxetine"):        {"severity": "MODERATE", "effect": "CYP2C9 inhibition — increases INR. Monitor."},
    ("Warfarin", "Simvastatin"):       {"severity": "MODERATE", "effect": "Some statins enhance anticoagulant effect. Monitor INR."},
    ("Warfarin", "Levothyroxine"):     {"severity": "MODERATE", "effect": "Hyperthyroid state accelerates clotting factor catabolism — increases INR."},
    ("Warfarin", "Rifampin"):          {"severity": "HIGH",     "effect": "CYP inducer — dramatically decreases Warfarin effect. May need 2–5x Warfarin dose."},
    ("Warfarin", "Carbamazepine"):     {"severity": "HIGH",     "effect": "CYP inducer — reduces Warfarin effect. Monitor INR."},
    ("Warfarin", "Vitamin K"):         {"severity": "MODERATE", "effect": "Dietary Vitamin K antagonizes Warfarin. Counsel on consistent leafy green intake."},
    ("Warfarin", "Fish Oil"):          {"severity": "MODERATE", "effect": "High-dose fish oil (>3g/day) may increase bleeding risk."},
    # ---- SSRI / SNRI interactions ----
    ("Sertraline", "Tramadol"):        {"severity": "HIGH",     "effect": "Serotonin syndrome risk. Avoid combination."},
    ("Sertraline", "Linezolid"):       {"severity": "HIGH",     "effect": "Serotonin syndrome — life-threatening. Contraindicated."},
    ("Sertraline", "MAOIs"):           {"severity": "CRITICAL", "effect": "Serotonin syndrome — potentially fatal. 14-day washout required."},
    ("Sertraline", "Lithium"):         {"severity": "MODERATE", "effect": "Additive serotonergic effect; lithium toxicity risk. Monitor levels."},
    ("Sertraline", "St. John's Wort"): {"severity": "HIGH",     "effect": "Serotonin syndrome risk. Avoid herbal supplement."},
    ("Sertraline", "Fentanyl"):        {"severity": "MODERATE", "effect": "Weak serotonergic interaction; monitor for serotonin syndrome signs."},
    ("Sertraline", "Sumatriptan"):     {"severity": "MODERATE", "effect": "Serotonin syndrome risk with triptans. Use lowest effective doses."},
    ("Sertraline", "Metoclopramide"):  {"severity": "MODERATE", "effect": "Increased risk of extrapyramidal effects and serotonin toxicity."},
    ("Fluoxetine", "Tamoxifen"):       {"severity": "HIGH",     "effect": "Fluoxetine (CYP2D6 inhibitor) reduces Tamoxifen efficacy. Use Venlafaxine instead."},
    ("Fluoxetine", "Codeine"):         {"severity": "HIGH",     "effect": "CYP2D6 inhibition — reduces conversion to morphine (analgesic failure); may still cause OD in some."},
    ("Fluoxetine", "MAOIs"):           {"severity": "CRITICAL", "effect": "Serotonin syndrome — fatal. 5-week washout for fluoxetine (long half-life)."},
    # ---- OPIOID interactions ----
    ("Gabapentin", "Opioids"):         {"severity": "HIGH",     "effect": "Synergistic CNS/respiratory depression — increased overdose mortality 49%. Avoid or use minimal doses."},
    ("Gabapentin", "Benzodiazepines"): {"severity": "HIGH",     "effect": "Additive CNS and respiratory depression. Avoid combination."},
    ("Opioids", "Benzodiazepines"):    {"severity": "HIGH",     "effect": "Synergistic respiratory depression — FDA Black Box Warning. Avoid concurrent use."},
    ("Opioids", "Alcohol"):            {"severity": "HIGH",     "effect": "Synergistic CNS depression; fatal respiratory depression risk."},
    ("Opioids", "MAOIs"):             {"severity": "CRITICAL", "effect": "Serotonin syndrome + cardiovascular instability. Contraindicated."},
    ("Morphine", "Naltrexone"):        {"severity": "HIGH",     "effect": "Naltrexone blocks opioid effect; causes acute withdrawal. Do not combine."},
    ("Methadone", "QT-prolonging drugs"): {"severity": "HIGH", "effect": "Additive QT prolongation — torsades de pointes risk. Monitor ECG."},
    # ---- ACE INHIBITOR / ARB interactions ----
    ("Lisinopril", "Potassium Supplements"): {"severity": "MODERATE", "effect": "Hyperkalemia risk. Monitor K+ levels."},
    ("Lisinopril", "NSAIDs"):          {"severity": "MODERATE", "effect": "Reduced antihypertensive effect; acute kidney injury risk in susceptible patients."},
    ("Lisinopril", "Spironolactone"):  {"severity": "MODERATE", "effect": "Hyperkalemia risk — monitor potassium, especially in CKD/HF."},
    ("Lisinopril", "Lithium"):         {"severity": "MODERATE", "effect": "ACE inhibitors reduce lithium excretion — toxicity risk. Monitor lithium levels."},
    ("Lisinopril", "Aliskiren"):       {"severity": "HIGH",     "effect": "Dual RAAS blockade increases hypotension, hyperkalemia, and renal failure. Avoid in T2DM/CKD."},
    ("Losartan", "NSAIDs"):            {"severity": "MODERATE", "effect": "Blunted antihypertensive effect; risk of AKI. Avoid in CKD."},
    ("Losartan", "Potassium"):         {"severity": "MODERATE", "effect": "ARBs reduce K+ excretion — hyperkalemia with supplementation."},
    ("Losartan", "Spironolactone"):    {"severity": "MODERATE", "effect": "Hyperkalemia risk — monitor in HF/CKD."},
    # ---- STATIN interactions ----
    ("Simvastatin", "Amiodarone"):     {"severity": "HIGH",     "effect": "Simvastatin dose capped at 20mg with amiodarone — myopathy/rhabdomyolysis risk."},
    ("Simvastatin", "Clarithromycin"): {"severity": "HIGH",     "effect": "CYP3A4 inhibition → marked statin level increase → myopathy risk. Hold statin during course."},
    ("Simvastatin", "Fluconazole"):    {"severity": "HIGH",     "effect": "CYP3A4 inhibition — statin toxicity. Use rosuvastatin or pravastatin instead."},
    ("Atorvastatin", "Clarithromycin"): {"severity": "MODERATE","effect": "CYP3A4 inhibition increases atorvastatin levels. Monitor for myopathy."},
    ("Atorvastatin", "Cyclosporine"):  {"severity": "HIGH",     "effect": "Significant statin level increase — myopathy/rhabdomyolysis. Max atorvastatin 10mg."},
    ("Rosuvastatin", "Cyclosporine"):  {"severity": "HIGH",     "effect": "OATP1B1 inhibition increases rosuvastatin levels — myopathy risk. Avoid or max 5mg."},
    ("Simvastatin", "Gemfibrozil"):    {"severity": "HIGH",     "effect": "Rhabdomyolysis risk — avoid combination. Use fenofibrate if needed."},
    ("Atorvastatin", "Niacin"):        {"severity": "MODERATE", "effect": "Additive myopathy risk at high niacin doses."},
    ("Simvastatin", "Colchicine"):     {"severity": "MODERATE", "effect": "Myopathy risk — monitor CK. Reduce statin dose if possible."},
    # ---- METFORMIN interactions ----
    ("Metformin", "Contrast Dye"):     {"severity": "MODERATE", "effect": "Contrast-induced AKI → lactic acidosis. Hold Metformin 48h before and after contrast."},
    ("Metformin", "Alcohol"):          {"severity": "MODERATE", "effect": "Increased lactic acidosis risk + hypoglycemia. Counsel on alcohol limits."},
    ("Metformin", "Topiramate"):       {"severity": "MODERATE", "effect": "Additive lactic acidosis risk. Monitor renal function."},
    ("Metformin", "Vancomycin"):       {"severity": "MODERATE", "effect": "IV vancomycin may impair renal function → metformin accumulation → lactic acidosis."},
    # ---- DIGOXIN interactions ----
    ("Digoxin", "Amiodarone"):         {"severity": "HIGH",     "effect": "Amiodarone inhibits P-gp + renal clearance — digoxin toxicity. Reduce digoxin 50% and monitor levels."},
    ("Digoxin", "Verapamil"):          {"severity": "HIGH",     "effect": "Verapamil reduces digoxin clearance by 50% — toxicity. Reduce digoxin dose."},
    ("Digoxin", "Spironolactone"):     {"severity": "MODERATE", "effect": "Spironolactone may increase digoxin levels. Monitor."},
    ("Digoxin", "Clarithromycin"):     {"severity": "HIGH",     "effect": "P-gp inhibition — significant digoxin level increase → toxicity."},
    ("Digoxin", "Quinidine"):          {"severity": "HIGH",     "effect": "Quinidine doubles digoxin levels. Reduce digoxin 50%."},
    ("Digoxin", "Rifampin"):           {"severity": "MODERATE", "effect": "P-gp induction reduces digoxin levels — therapeutic failure."},
    ("Digoxin", "Erythromycin"):       {"severity": "MODERATE", "effect": "Gut flora alteration + P-gp inhibition — digoxin level increase."},
    # ---- QT PROLONGATION interactions ----
    ("Azithromycin", "Amiodarone"):    {"severity": "HIGH",     "effect": "Additive QT prolongation — torsades de pointes risk. Avoid. Use azithromycin alternative."},
    ("Amiodarone", "Sotalol"):         {"severity": "HIGH",     "effect": "Additive QT prolongation. Contraindicated combination."},
    ("Haloperidol", "Ondansetron"):    {"severity": "HIGH",     "effect": "Additive QT prolongation — cardiac arrhythmia risk."},
    ("Ciprofloxacin", "Ondansetron"):  {"severity": "MODERATE", "effect": "Additive QT prolongation. Monitor ECG."},
    ("Methadone", "Amiodarone"):       {"severity": "HIGH",     "effect": "Extreme QT prolongation. Avoid concurrent use."},
    ("Quetiapine", "Amiodarone"):      {"severity": "HIGH",     "effect": "Additive QT prolongation. Avoid."},
    ("Erythromycin", "Amiodarone"):    {"severity": "HIGH",     "effect": "Additive QT prolongation. Use alternative antibiotic."},
    # ---- ANTICOAGULANT / ANTIPLATELET ----
    ("Clopidogrel", "Omeprazole"):     {"severity": "MODERATE", "effect": "Omeprazole inhibits CYP2C19 — reduces clopidogrel activation. Use pantoprazole."},
    ("Clopidogrel", "Fluoxetine"):     {"severity": "MODERATE", "effect": "CYP2C19 inhibition reduces antiplatelet effect."},
    ("Rivaroxaban", "Ketoconazole"):   {"severity": "HIGH",     "effect": "CYP3A4 + P-gp inhibition — major NOAC level increase → bleeding risk. Avoid."},
    ("Apixaban", "Rifampin"):          {"severity": "HIGH",     "effect": "CYP3A4 induction — significant reduction in apixaban levels. Avoid."},
    ("Dabigatran", "Dronedarone"):     {"severity": "HIGH",     "effect": "P-gp inhibition — dabigatran level doubles. Reduce dose or avoid."},
    ("Aspirin", "Clopidogrel"):        {"severity": "MODERATE", "effect": "Dual antiplatelet therapy increases bleeding risk. Use only when indicated (e.g., ACS, stenting)."},
    ("Aspirin", "Heparin"):            {"severity": "MODERATE", "effect": "Additive bleeding risk. Monitor closely."},
    # ---- ANTIEPILEPTIC interactions ----
    ("Carbamazepine", "Valproate"):    {"severity": "MODERATE", "effect": "Carbamazepine increases valproate metabolism; epoxide metabolite accumulation → toxicity."},
    ("Phenytoin", "Valproate"):        {"severity": "MODERATE", "effect": "Valproate displaces phenytoin + inhibits metabolism — complex interaction. Monitor free phenytoin."},
    ("Carbamazepine", "Oral Contraceptives"): {"severity": "HIGH", "effect": "CYP3A4 induction reduces OCP efficacy — contraception failure. Use non-hormonal method."},
    ("Phenytoin", "Oral Contraceptives"): {"severity": "HIGH",  "effect": "CYP induction reduces OCP efficacy. Backup contraception required."},
    ("Phenytoin", "Warfarin"):         {"severity": "HIGH",     "effect": "Complex interaction: initial inhibition then induction. Monitor INR closely."},
    ("Carbamazepine", "Lithium"):      {"severity": "MODERATE", "effect": "Neurotoxicity risk despite normal lithium levels. Monitor closely."},
    ("Valproate", "Lamotrigine"):      {"severity": "MODERATE", "effect": "Valproate inhibits lamotrigine glucuronidation — lamotrigine levels double. Reduce lamotrigine dose."},
    ("Topiramate", "Valproate"):       {"severity": "MODERATE", "effect": "Hyperammonemia risk. Monitor ammonia if encephalopathy symptoms."},
    # ---- ANTIBIOTIC interactions ----
    ("Ciprofloxacin", "Antacids"):     {"severity": "MODERATE", "effect": "Divalent cations chelate fluoroquinolones — reduced absorption. Space by 2 hours."},
    ("Tetracycline", "Antacids"):      {"severity": "MODERATE", "effect": "Calcium/magnesium/iron chelation — markedly reduced tetracycline absorption."},
    ("Ciprofloxacin", "Theophylline"): {"severity": "HIGH",     "effect": "CYP1A2 inhibition — theophylline toxicity (seizures, arrhythmias). Monitor levels."},
    ("Erythromycin", "Carbamazepine"): {"severity": "HIGH",     "effect": "CYP3A4 inhibition — carbamazepine toxicity. Monitor levels."},
    ("Rifampin", "Oral Contraceptives"): {"severity": "HIGH",   "effect": "CYP3A4 induction — OCP failure. Use barrier method during and 1 month after rifampin."},
    ("Rifampin", "HIV Antiretrovirals"): {"severity": "HIGH",   "effect": "Major CYP3A4 induction reduces most ARVs. Use rifabutin as substitute."},
    ("Metronidazole", "Alcohol"):      {"severity": "HIGH",     "effect": "Disulfiram-like reaction: flushing, vomiting, tachycardia. Avoid alcohol during and 48h after."},
    ("Trimethoprim", "Methotrexate"):  {"severity": "HIGH",     "effect": "Additive folate antagonism — severe bone marrow suppression. Avoid."},
    # ---- IMMUNOSUPPRESSANT interactions ----
    ("Cyclosporine", "Tacrolimus"):    {"severity": "HIGH",     "effect": "Additive nephrotoxicity. Do not combine."},
    ("Cyclosporine", "Statins"):       {"severity": "HIGH",     "effect": "OATP1B1 inhibition — dramatic statin level increase → rhabdomyolysis risk."},
    ("Cyclosporine", "Azithromycin"):  {"severity": "MODERATE", "effect": "P-gp inhibition may increase cyclosporine levels. Monitor levels."},
    ("Tacrolimus", "Azole antifungals"): {"severity": "HIGH",   "effect": "CYP3A4 inhibition — major tacrolimus level increase → nephrotoxicity. Monitor levels."},
    ("Tacrolimus", "Rifampin"):        {"severity": "HIGH",     "effect": "CYP3A4 induction — major tacrolimus level decrease → rejection risk."},
    ("Mycophenolate", "Rifampin"):     {"severity": "HIGH",     "effect": "Rifampin reduces mycophenolate levels by 70% — rejection risk."},
    ("Methotrexate", "NSAIDs"):        {"severity": "HIGH",     "effect": "NSAIDs reduce methotrexate renal excretion → toxicity risk. Avoid, especially at high MTX doses."},
    ("Methotrexate", "Trimethoprim"):  {"severity": "HIGH",     "effect": "Additive antifolate effect → pancytopenia. Contraindicated."},
    # ---- CHEMOTHERAPY interactions ----
    ("Tamoxifen", "Paroxetine"):       {"severity": "HIGH",     "effect": "Paroxetine (strong CYP2D6 inhibitor) reduces tamoxifen → endoxifen conversion → reduced efficacy."},
    ("Irinotecan", "Ketoconazole"):    {"severity": "HIGH",     "effect": "CYP3A4 inhibition → dramatically increased irinotecan toxicity (severe diarrhea, neutropenia)."},
    ("Vincristine", "Azole antifungals"): {"severity": "HIGH",  "effect": "CYP3A4 inhibition → increased vincristine exposure → severe neurotoxicity."},
    ("Cyclophosphamide", "Allopurinol"): {"severity": "MODERATE","effect": "Allopurinol inhibits cyclophosphamide metabolism → increased toxicity."},
    ("Capecitabine", "Warfarin"):      {"severity": "HIGH",     "effect": "Major INR elevation. Monitor INR weekly."},
    # ---- CARDIAC MEDICATIONS ----
    ("Amiodarone", "Simvastatin"):     {"severity": "HIGH",     "effect": "CYP3A4 inhibition → myopathy. Cap simvastatin at 20mg."},
    ("Amiodarone", "Digoxin"):         {"severity": "HIGH",     "effect": "Digoxin toxicity — reduce digoxin dose by 50%."},
    ("Amiodarone", "Warfarin"):        {"severity": "HIGH",     "effect": "Potentiates Warfarin — monitor INR weekly; reduce dose 30–50%."},
    ("Verapamil", "Beta-blockers"):    {"severity": "HIGH",     "effect": "Additive AV conduction delay — complete heart block risk. Avoid non-DHP CCB + BB combination."},
    ("Diltiazem", "Simvastatin"):      {"severity": "MODERATE", "effect": "CYP3A4 inhibition → increased statin exposure → myopathy."},
    ("Furosemide", "Lithium"):         {"severity": "HIGH",     "effect": "Furosemide-induced Na+ and volume depletion → lithium toxicity. Monitor levels."},
    ("Furosemide", "Aminoglycosides"): {"severity": "HIGH",     "effect": "Additive ototoxicity and nephrotoxicity. Avoid concurrent use."},
    ("Spironolactone", "ACE Inhibitors"): {"severity": "MODERATE","effect": "Hyperkalemia risk — monitor K+ in HF/CKD."},
    ("Spironolactone", "NSAIDs"):      {"severity": "MODERATE", "effect": "Reduced diuretic effect and increased hyperkalemia risk."},
    # ---- DIABETES MEDICATIONS ----
    ("Sulfonylureas", "Fluconazole"):  {"severity": "HIGH",     "effect": "CYP2C9 inhibition → hypoglycemia. Monitor glucose."},
    ("Insulin", "Beta-blockers"):      {"severity": "MODERATE", "effect": "Beta-blockers mask hypoglycemia symptoms (tachycardia). Use with caution; monitor glucose."},
    ("Insulin", "Alcohol"):            {"severity": "HIGH",     "effect": "Hypoglycemia risk — alcohol inhibits hepatic gluconeogenesis. Counsel patients."},
    ("GLP-1 Agonists", "Insulin"):     {"severity": "MODERATE", "effect": "Additive hypoglycemia risk. Reduce insulin dose when initiating GLP-1 agonist."},
    # ---- PSYCHIATRIC MEDICATIONS ----
    ("Lithium", "NSAIDs"):             {"severity": "HIGH",     "effect": "NSAIDs reduce lithium renal clearance → toxicity (tremor, confusion, renal failure)."},
    ("Lithium", "Thiazide Diuretics"): {"severity": "HIGH",     "effect": "Sodium depletion increases lithium reabsorption → toxicity."},
    ("Lithium", "ACE Inhibitors"):     {"severity": "MODERATE", "effect": "Reduced lithium excretion → toxicity risk. Monitor levels."},
    ("Clozapine", "Ciprofloxacin"):    {"severity": "MODERATE", "effect": "CYP1A2 inhibition → elevated clozapine levels → seizures, sedation."},
    ("Clozapine", "Valproate"):        {"severity": "MODERATE", "effect": "Additive seizure threshold lowering + bone marrow suppression."},
    ("MAOIs", "Meperidine"):           {"severity": "CRITICAL", "effect": "Life-threatening serotonin syndrome/hyperpyrexia. Absolutely contraindicated."},
    ("MAOIs", "Tyramine-rich foods"):  {"severity": "HIGH",     "effect": "Hypertensive crisis. Avoid aged cheeses, cured meats, fermented foods."},
    # ---- HIV ANTIRETROVIRALS ----
    ("HIV Antiretrovirals", "Rifampin"): {"severity": "HIGH",   "effect": "Rifampin is a potent CYP3A4 inducer — drastically reduces most ARV levels. Use rifabutin."},
    ("Protease Inhibitors", "Statins"): {"severity": "HIGH",    "effect": "CYP3A4 inhibition → marked statin level increase → myopathy. Use pravastatin or low-dose rosuvastatin."},
    ("Efavirenz", "Oral Contraceptives"): {"severity": "MODERATE","effect": "CYP3A4 induction may reduce OCP levels. Use additional contraception."},
    ("Tenofovir", "NSAIDs"):           {"severity": "MODERATE", "effect": "Additive nephrotoxicity risk. Monitor renal function."},
    # ---- THYROID ----
    ("Levothyroxine", "Antacids"):     {"severity": "MODERATE", "effect": "Calcium/magnesium/aluminum reduce levothyroxine absorption. Space by 4 hours."},
    ("Levothyroxine", "Calcium"):      {"severity": "MODERATE", "effect": "Calcium chelates levothyroxine — reduces absorption. Take on empty stomach, space supplements 4 hours."},
    ("Levothyroxine", "Iron"):         {"severity": "MODERATE", "effect": "Iron reduces levothyroxine absorption. Space by 4 hours."},
    # ---- GOUT ----
    ("Allopurinol", "Azathioprine"):   {"severity": "HIGH",     "effect": "Allopurinol inhibits xanthine oxidase → azathioprine (and 6-MP) toxicity. Reduce azathioprine dose to 25%."},
    ("Allopurinol", "6-Mercaptopurine"): {"severity": "HIGH",   "effect": "Bone marrow suppression — reduce 6-MP dose to 25% of usual."},
    ("Colchicine", "Clarithromycin"):  {"severity": "HIGH",     "effect": "P-gp + CYP3A4 inhibition → colchicine toxicity (myopathy, neuropathy). Fatal cases reported."},
    ("Colchicine", "Cyclosporine"):    {"severity": "HIGH",     "effect": "Major colchicine level increase → toxicity. Dose adjust or avoid."},
    # ---- PULMONARY ----
    ("Theophylline", "Ciprofloxacin"): {"severity": "HIGH",     "effect": "CYP1A2 inhibition → theophylline toxicity (seizures, arrhythmias)."},
    ("Theophylline", "Erythromycin"):  {"severity": "HIGH",     "effect": "CYP1A2 inhibition → theophylline toxicity. Monitor levels."},
    ("Theophylline", "Cimetidine"):    {"severity": "MODERATE", "effect": "CYP inhibition → increased theophylline levels."},
}

# Appointment schedule (runtime list)
_APPOINTMENTS: list[dict] = []

# SOAP notes store
_SOAP_NOTES: list[dict] = []


# =============================================================================
# MEDICATION DOSING DATABASE
# =============================================================================
_MED_DOSING: dict[str, dict] = {
    "amoxicillin": {
        "class": "Penicillin antibiotic",
        "standard_adult": "500 mg every 8 hours or 875 mg every 12 hours",
        "standard_adult_severe": "875–1000 mg every 8 hours",
        "pediatric": "25–45 mg/kg/day divided every 8–12 hours (max 90 mg/kg/day for AOM)",
        "renal_adjust": {
            "egfr_30_60": "No adjustment",
            "egfr_10_30": "250–500 mg every 12 hours",
            "egfr_lt_10": "250–500 mg every 24 hours",
        },
        "hepatic_adjust": "Use with caution in severe hepatic impairment",
        "max_dose": "3 g/day (standard); 4 g/day in severe infections",
        "monitoring": ["Signs of allergic reaction", "Rash (maculopapular 3–7 days)"],
        "contraindications": ["Penicillin allergy (cross-reactivity ~1–2% with cephalosporins)"],
        "food": "Can be taken with food",
    },
    "metformin": {
        "class": "Biguanide (antidiabetic)",
        "standard_adult": "500 mg twice daily with meals; titrate by 500 mg/week",
        "standard_adult_severe": "Maximum 2550 mg/day (extended-release 2000 mg/day)",
        "pediatric": "500 mg twice daily (age ≥10); max 2000 mg/day",
        "renal_adjust": {
            "egfr_30_60": "Dose with caution; reassess frequently. eGFR 30–45: not recommended to initiate",
            "egfr_10_30": "Contraindicated (lactic acidosis risk)",
            "egfr_lt_10": "Contraindicated",
        },
        "hepatic_adjust": "Avoid in significant hepatic impairment (lactic acidosis risk)",
        "max_dose": "2550 mg/day (immediate release)",
        "monitoring": ["eGFR (annually or more often)", "Vitamin B12 (annually)", "Lactic acidosis symptoms"],
        "contraindications": ["eGFR <30 mL/min", "Acute/chronic metabolic acidosis", "IV contrast within 48h"],
        "food": "Take with meals to reduce GI side effects",
    },
    "lisinopril": {
        "class": "ACE Inhibitor (antihypertensive/cardiac)",
        "standard_adult": "Hypertension: 10 mg daily; titrate to 20–40 mg daily",
        "standard_adult_severe": "Heart failure: start 2.5–5 mg daily, target 40 mg daily",
        "pediatric": "0.07–0.6 mg/kg/day (age ≥6 years)",
        "renal_adjust": {
            "egfr_30_60": "Reduce initial dose to 5 mg; monitor Cr and K+",
            "egfr_10_30": "Initial dose 2.5 mg; titrate carefully. Monitor closely",
            "egfr_lt_10": "Use with caution; risk of hyperkalemia and worsening renal function",
        },
        "hepatic_adjust": "No dose adjustment required",
        "max_dose": "40 mg/day (hypertension); 40 mg/day (heart failure)",
        "monitoring": ["Blood pressure", "Serum creatinine + potassium within 1–2 weeks of initiation",
                       "Angioedema symptoms (especially early)"],
        "contraindications": ["Pregnancy (Category D)", "History of angioedema with ACE inhibitor",
                               "Concurrent aliskiren in T2DM/CKD"],
        "food": "Can be taken with or without food",
    },
    "warfarin": {
        "class": "Vitamin K antagonist (anticoagulant)",
        "standard_adult": "Individualized; start 2–5 mg daily; adjust to INR target",
        "standard_adult_severe": "INR target 2.0–3.0 (AF, VTE, mechanical valves: 2.5–3.5)",
        "pediatric": "0.05–0.34 mg/kg/day; highly individualized",
        "renal_adjust": {
            "egfr_30_60": "No dose adjustment but increased bleeding risk — monitor INR closely",
            "egfr_10_30": "Use with extra caution; CKD affects protein binding and bleeding risk",
            "egfr_lt_10": "Consider alternative anticoagulant; consult hematology",
        },
        "hepatic_adjust": "Extreme caution — hepatic failure reduces clotting factor synthesis (already anticoagulated)",
        "max_dose": "No fixed maximum — INR-guided",
        "monitoring": ["INR (weekly initially, monthly when stable)", "Signs of bleeding",
                       "Drug and food interactions (Vitamin K)"],
        "contraindications": ["Pregnancy", "Active bleeding", "Recent CNS/eye/spinal surgery",
                               "Hemorrhagic stroke within 3 months"],
        "food": "Consistent Vitamin K intake; avoid major changes in diet",
    },
    "furosemide": {
        "class": "Loop diuretic",
        "standard_adult": "20–80 mg/day PO; IV: 20–40 mg bolus",
        "standard_adult_severe": "Acute pulmonary edema: 40–80 mg IV; may double every 2 hours (max 600 mg IV/day)",
        "pediatric": "1–2 mg/kg/dose every 6–12 hours (max 6 mg/kg/day)",
        "renal_adjust": {
            "egfr_30_60": "May require higher doses for diuretic effect",
            "egfr_10_30": "High doses needed; response reduced; consider IV route",
            "egfr_lt_10": "Large doses required (loop diuretics still effective in CKD; thiazides ineffective)",
        },
        "hepatic_adjust": "Caution in cirrhosis — electrolyte imbalance and encephalopathy risk",
        "max_dose": "600 mg/day IV (acute); 600 mg/day PO (chronic resistant edema)",
        "monitoring": ["Electrolytes (Na+, K+, Mg2+)", "Creatinine", "Blood pressure", "Urine output",
                       "Weight (daily)"],
        "contraindications": ["Anuria", "Sulfonamide allergy (cross-reactivity ~1%)"],
        "food": "Take in morning to avoid nocturia",
    },
    "amlodipine": {
        "class": "Dihydropyridine calcium channel blocker",
        "standard_adult": "5 mg once daily; may increase to 10 mg after 7–14 days",
        "standard_adult_severe": "10 mg/day (hypertension/angina)",
        "pediatric": "0.1–0.3 mg/kg/day (age 6–17); max 10 mg/day",
        "renal_adjust": {
            "egfr_30_60": "No adjustment needed",
            "egfr_10_30": "No adjustment needed",
            "egfr_lt_10": "No adjustment needed",
        },
        "hepatic_adjust": "Start 2.5 mg; titrate slowly in severe hepatic impairment",
        "max_dose": "10 mg/day",
        "monitoring": ["Blood pressure", "Peripheral edema (dose-dependent)", "Liver function"],
        "contraindications": ["Amlodipine allergy"],
        "food": "Can be taken with or without food",
    },
    "atorvastatin": {
        "class": "HMG-CoA reductase inhibitor (statin)",
        "standard_adult": "10–20 mg once daily; high-intensity: 40–80 mg daily",
        "standard_adult_severe": "80 mg daily for very high CV risk / post-ACS",
        "pediatric": "10–20 mg/day (familial hypercholesterolemia, age ≥10)",
        "renal_adjust": {
            "egfr_30_60": "No adjustment",
            "egfr_10_30": "No adjustment (atorvastatin not renally excreted)",
            "egfr_lt_10": "Use with caution; CKD increases myopathy risk",
        },
        "hepatic_adjust": "Contraindicated in active hepatic disease or unexplained persistent LFT elevations",
        "max_dose": "80 mg/day",
        "monitoring": ["LFTs (baseline, if symptoms)", "CK (if myopathy symptoms)", "LDL-C at 4–12 weeks"],
        "contraindications": ["Active liver disease", "Pregnancy/breastfeeding"],
        "food": "Can be taken at any time of day (unlike some other statins)",
    },
    "gabapentin": {
        "class": "Anticonvulsant / neuropathic pain agent",
        "standard_adult": "300 mg on day 1; 300 mg BID day 2; 300 mg TID day 3; titrate to 900–3600 mg/day in divided doses",
        "standard_adult_severe": "1800–3600 mg/day in 3 divided doses",
        "pediatric": "Children ≥3: 10–15 mg/kg/day divided TID; adolescents: adult dosing",
        "renal_adjust": {
            "egfr_30_60": "300–700 mg twice daily",
            "egfr_10_30": "200–700 mg daily",
            "egfr_lt_10": "100–300 mg daily (post-dialysis supplemental dose if on HD)",
        },
        "hepatic_adjust": "No adjustment required (not hepatically metabolized)",
        "max_dose": "3600 mg/day (3 divided doses)",
        "monitoring": ["Sedation", "Respiratory depression (especially with CNS depressants/opioids)",
                       "Renal function", "Suicidality (AED class warning)"],
        "contraindications": ["Hypersensitivity to gabapentin"],
        "food": "Can be taken with food to reduce GI effects",
    },
    "sertraline": {
        "class": "SSRI (antidepressant/anxiolytic)",
        "standard_adult": "50 mg once daily; titrate by 50 mg/day at weekly intervals",
        "standard_adult_severe": "100–200 mg/day",
        "pediatric": "MDD (age ≥6): 25 mg/day; OCD (age ≥6): 25 mg/day, titrate to 200 mg/day max",
        "renal_adjust": {
            "egfr_30_60": "No adjustment",
            "egfr_10_30": "No adjustment",
            "egfr_lt_10": "No adjustment (but accumulation of inactive metabolites — use caution)",
        },
        "hepatic_adjust": "Use lower doses (25 mg) and slower titration in hepatic impairment",
        "max_dose": "200 mg/day",
        "monitoring": ["Suicidality (first weeks — Black Box Warning in <25 years)", "Serotonin syndrome symptoms",
                       "Activation/insomnia", "QTc prolongation (at high doses)"],
        "contraindications": ["MAOIs within 14 days", "Linezolid", "Methylene blue IV"],
        "food": "Take with food to reduce GI side effects (especially nausea)",
    },
    "hydroxychloroquine": {
        "class": "Antimalarial / DMARD",
        "standard_adult": "Lupus/RA: 200–400 mg/day; max 5 mg/kg/day (lean body weight) to limit retinal toxicity",
        "standard_adult_severe": "400 mg/day (do not exceed 5 mg/kg/day LBW)",
        "pediatric": "Malaria prophylaxis: 6.5 mg/kg/week (max 400 mg)",
        "renal_adjust": {
            "egfr_30_60": "No adjustment",
            "egfr_10_30": "Use with caution; hydroxychloroquine excreted renally",
            "egfr_lt_10": "Use with extreme caution; consider dose reduction",
        },
        "hepatic_adjust": "Use with caution; hepatic impairment may slow metabolism",
        "max_dose": "400 mg/day (do not exceed 5 mg/kg/day to prevent retinopathy)",
        "monitoring": ["Annual ophthalmologic exam (retinopathy risk after 5 years)", "ECG (QTc)",
                       "CBC", "LFTs"],
        "contraindications": ["4-aminoquinoline hypersensitivity", "Pre-existing maculopathy"],
        "food": "Take with food or milk to reduce GI effects",
    },
    "amiodarone": {
        "class": "Class III antiarrhythmic",
        "standard_adult": "Loading: 800–1600 mg/day for 1–3 weeks; Maintenance: 100–400 mg/day",
        "standard_adult_severe": "IV bolus (VF/VT): 300 mg IV; maintenance infusion 1 mg/min x 6h then 0.5 mg/min",
        "pediatric": "5 mg/kg IV bolus for VT/VF; 5 mg/kg/day PO (divided doses)",
        "renal_adjust": {
            "egfr_30_60": "No dose adjustment",
            "egfr_10_30": "No dose adjustment (not renally excreted primarily)",
            "egfr_lt_10": "No dose adjustment required",
        },
        "hepatic_adjust": "Use with caution; hepatotoxicity possible. Reduce dose if LFTs >2x ULN",
        "max_dose": "400 mg/day maintenance; loading 1600 mg/day x3 weeks",
        "monitoring": ["TFTs every 6 months (hypo/hyperthyroidism)", "LFTs every 6 months",
                       "CXR annually (pulmonary toxicity)", "Ophthalmology annually (corneal deposits)",
                       "INR (inhibits Warfarin metabolism)", "QTc"],
        "contraindications": ["Sinus node dysfunction/AV block without pacemaker", "Iodine allergy",
                               "Severe pulmonary toxicity", "Thyroid dysfunction (relative)"],
        "food": "Grapefruit juice inhibits metabolism — avoid. Take with food to reduce GI effects",
    },
}


# =============================================================================
# TOOL FUNCTIONS
# =============================================================================

def get_patient_info(patient_id: str) -> dict:
    """Retrieves patient demographics, medical history, allergies, and current medications.

    Args:
        patient_id: The patient identifier (e.g., 'P001' through 'P010').

    Returns:
        dict: Patient information including name, age, gender, allergies, conditions, and medications.
    """
    if patient_id in _PATIENT_DB:
        patient = _PATIENT_DB[patient_id]
        return {
            "status": "success",
            "patient": patient,
            "message": f"Patient record found for {patient['name']}.",
        }
    return {
        "status": "not_found",
        "message": f"No patient found with ID '{patient_id}'. Available IDs: {', '.join(_PATIENT_DB.keys())}",
    }


def record_vitals(
    patient_id: str,
    blood_pressure: str,
    heart_rate: int,
    temperature: float,
    spo2: int,
    respiratory_rate: Optional[int] = None,
    pain_level: Optional[int] = None,
) -> dict:
    """Records patient vital signs and performs automated clinical analysis.

    Args:
        patient_id: The patient identifier.
        blood_pressure: Blood pressure reading in 'systolic/diastolic' format (e.g., '120/80').
        heart_rate: Heart rate in beats per minute.
        temperature: Body temperature in Fahrenheit.
        spo2: Oxygen saturation percentage (SpO2).
        respiratory_rate: Breaths per minute (optional, normal 12–20).
        pain_level: Pain scale 0–10 (optional; ≥7 is severe).

    Returns:
        dict: Vitals record with automated clinical analysis and alert level.
    """
    analysis = []
    alert_level = "NORMAL"

    # Blood pressure
    try:
        systolic, diastolic = map(int, blood_pressure.split("/"))
        if systolic >= 180 or diastolic >= 120:
            analysis.append("CRITICAL: Hypertensive crisis — immediate intervention needed (IV labetalol/nicardipine)")
            alert_level = "CRITICAL"
        elif systolic >= 160 or diastolic >= 100:
            analysis.append("WARNING: Hypertension Stage 2 — consider urgent medication")
            alert_level = max(alert_level, "WARNING")
        elif systolic >= 130 or diastolic >= 80:
            analysis.append("ELEVATED: Hypertension Stage 1")
            alert_level = max(alert_level, "ELEVATED")
        elif systolic < 70:
            analysis.append("CRITICAL: Severe hypotension / shock — immediate fluid resuscitation")
            alert_level = "CRITICAL"
        elif systolic < 90 or diastolic < 60:
            analysis.append("WARNING: Hypotension — assess volume status and cause")
            alert_level = max(alert_level, "WARNING")
        else:
            analysis.append("BP: Normal")

        # MAP calculation
        map_value = round((systolic + 2 * diastolic) / 3)
        if map_value < 65:
            analysis.append(f"WARNING: MAP {map_value} mmHg — below perfusion threshold (target ≥65)")
            alert_level = max(alert_level, "WARNING")
        else:
            analysis.append(f"MAP: {map_value} mmHg (normal ≥65)")

    except (ValueError, TypeError):
        analysis.append("BP: Unable to parse — verify format 'systolic/diastolic'")

    # Heart rate
    if heart_rate > 150:
        analysis.append("CRITICAL: Severe tachycardia — 12-lead ECG immediately")
        alert_level = "CRITICAL"
    elif heart_rate > 100:
        analysis.append("WARNING: Tachycardia — evaluate for pain, fever, dehydration, arrhythmia")
        alert_level = max(alert_level, "WARNING")
    elif heart_rate < 40:
        analysis.append("CRITICAL: Severe bradycardia — consider atropine/pacing if symptomatic")
        alert_level = "CRITICAL"
    elif heart_rate < 60:
        analysis.append("NOTE: Bradycardia — may be normal (athletes) or medication effect")
    else:
        analysis.append("HR: Normal")

    # Temperature
    if temperature >= 104.0:
        analysis.append("CRITICAL: Hyperpyrexia — aggressive cooling, blood cultures, antibiotics")
        alert_level = "CRITICAL"
    elif temperature >= 100.4:
        analysis.append("WARNING: Fever — evaluate for infection source; blood cultures if T≥38.5°C")
        alert_level = max(alert_level, "WARNING")
    elif temperature < 95.0:
        analysis.append("WARNING: Hypothermia — warm blankets, warm IV fluids, identify cause")
        alert_level = max(alert_level, "WARNING")
    else:
        analysis.append("Temp: Normal (36.1–38.0°C / 97.0–100.4°F)")

    # SpO2
    if spo2 < 88:
        analysis.append("CRITICAL: Severe hypoxemia — immediate supplemental O2, prepare for intubation")
        alert_level = "CRITICAL"
    elif spo2 < 92:
        analysis.append("WARNING: Hypoxemia — high-flow O2, evaluate for respiratory failure")
        alert_level = max(alert_level, "WARNING")
    elif spo2 < 95:
        analysis.append("ELEVATED: Low-normal SpO2 — supplemental O2 and monitoring")
        alert_level = max(alert_level, "ELEVATED")
    else:
        analysis.append("SpO2: Normal (≥95%)")

    # Respiratory rate
    if respiratory_rate is not None:
        if respiratory_rate > 30:
            analysis.append("CRITICAL: Respiratory distress (RR >30) — immediate evaluation")
            alert_level = "CRITICAL"
        elif respiratory_rate > 20:
            analysis.append("WARNING: Tachypnea — assess for underlying cause (infection, metabolic, cardiac)")
            alert_level = max(alert_level, "WARNING")
        elif respiratory_rate < 8:
            analysis.append("CRITICAL: Bradypnea — risk of respiratory arrest; consider opioid reversal")
            alert_level = "CRITICAL"
        else:
            analysis.append("RR: Normal (12–20 breaths/min)")

    # Pain
    if pain_level is not None:
        if pain_level >= 8:
            analysis.append(f"Pain Level {pain_level}/10: Severe pain — requires immediate analgesic intervention")
        elif pain_level >= 5:
            analysis.append(f"Pain Level {pain_level}/10: Moderate pain — assess and treat")
        elif pain_level > 0:
            analysis.append(f"Pain Level {pain_level}/10: Mild pain")

    # Early Warning Score (simple NEWS-lite)
    news_points = 0
    try:
        systolic, _ = map(int, blood_pressure.split("/"))
        if systolic <= 90 or systolic >= 220:
            news_points += 3
        elif systolic <= 100:
            news_points += 2
        elif systolic <= 110:
            news_points += 1
    except (ValueError, TypeError):
        pass
    if heart_rate <= 40 or heart_rate >= 131:
        news_points += 3
    elif heart_rate <= 50 or heart_rate >= 111:
        news_points += 2
    if spo2 < 92:
        news_points += 3
    elif spo2 < 94:
        news_points += 2
    elif spo2 < 96:
        news_points += 1
    if temperature < 35.1 or temperature >= 104.0:
        news_points += 3
    elif temperature < 36.1 or temperature >= 101.1:
        news_points += 1

    return {
        "status": "recorded",
        "patient_id": patient_id,
        "vitals_recorded": {
            "blood_pressure": blood_pressure,
            "heart_rate": heart_rate,
            "temperature_F": temperature,
            "spo2_percent": spo2,
            "respiratory_rate": respiratory_rate,
            "pain_level": pain_level,
        },
        "clinical_analysis": analysis,
        "overall_alert_level": alert_level,
        "early_warning_score": news_points,
        "ews_interpretation": (
            "Low risk" if news_points <= 4 else
            "Medium risk — increase monitoring frequency" if news_points <= 6 else
            "HIGH risk — urgent clinical review required"
        ),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def check_drug_interactions(medications: list[str]) -> dict:
    """Checks for known drug interactions between a list of medications.

    Searches a comprehensive database of 150+ clinically significant drug pairs.

    Args:
        medications: List of medication names to check for interactions.
                     Include just the drug name (e.g., ['Warfarin', 'Amiodarone', 'Aspirin']).

    Returns:
        dict: Found interactions with severity levels, clinical effects, and recommendations.
    """
    interactions_found = []
    medications_normalized = [m.split()[0].strip().title() for m in medications]

    for i in range(len(medications_normalized)):
        for j in range(i + 1, len(medications_normalized)):
            med1 = medications_normalized[i]
            med2 = medications_normalized[j]

            key1 = (med1, med2)
            key2 = (med2, med1)

            interaction = _DRUG_INTERACTIONS.get(key1) or _DRUG_INTERACTIONS.get(key2)
            if interaction:
                interactions_found.append({
                    "drug_1": medications[i],
                    "drug_2": medications[j],
                    **interaction,
                })

    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MODERATE": 2, "LOW": 3}
    interactions_found.sort(key=lambda x: severity_order.get(x.get("severity", "LOW"), 3))

    if interactions_found:
        critical_count = sum(1 for x in interactions_found if x.get("severity") == "CRITICAL")
        high_count = sum(1 for x in interactions_found if x.get("severity") == "HIGH")
        return {
            "status": "interactions_found",
            "count": len(interactions_found),
            "critical_count": critical_count,
            "high_severity_count": high_count,
            "interactions": interactions_found,
            "recommendation": (
                "CRITICAL interactions present — do not administer without specialist review."
                if critical_count > 0 else
                "HIGH severity interactions found — consult prescribing physician before dispensing."
                if high_count > 0 else
                "Moderate interactions found — monitor patient and consider alternatives."
            ),
        }
    return {
        "status": "no_interactions",
        "message": f"No known interactions found among: {', '.join(medications)}",
        "note": "Database covers 150+ common clinical drug pairs. Novel combinations may not be listed.",
    }


def schedule_appointment(department: str, urgency: str, patient_id: str, reason: str) -> dict:
    """Schedules a follow-up appointment for a patient.

    Args:
        department: The department name (e.g., 'Cardiology', 'Nephrology').
        urgency: Urgency level — 'routine', 'urgent', or 'emergency'.
        patient_id: The patient identifier.
        reason: Reason for the appointment.

    Returns:
        dict: Appointment confirmation with scheduled timeframe and ID.
    """
    scheduling = {
        "emergency": {"timeframe": "Today (immediate)", "priority": 1},
        "urgent":    {"timeframe": "Within 24–48 hours", "priority": 2},
        "routine":   {"timeframe": "Within 1–2 weeks", "priority": 3},
    }

    sched = scheduling.get(urgency.lower(), {"timeframe": "Within 1–2 weeks", "priority": 3})

    appointment = {
        "appointment_id": f"APT-{len(_APPOINTMENTS) + 1001}",
        "patient_id": patient_id,
        "department": department,
        "urgency": urgency,
        "timeframe": sched["timeframe"],
        "priority": sched["priority"],
        "reason": reason,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "instructions": {
            "emergency": "Patient should proceed to the department NOW. Alert charge nurse.",
            "urgent": "Patient will be contacted within 2 hours to confirm appointment slot.",
            "routine": "Patient will receive confirmation by phone/email within 24 hours.",
        }.get(urgency.lower(), "Standard booking confirmation will be sent."),
    }
    _APPOINTMENTS.append(appointment)

    return {
        "status": "scheduled",
        "appointment": appointment,
        "message": f"Appointment scheduled with {department} ({sched['timeframe']}) for: {reason}",
    }


def get_lab_results(patient_id: str, test_type: str) -> dict:
    """Retrieves laboratory test results for a patient.

    Args:
        patient_id: The patient identifier (P001–P010).
        test_type: Type of lab test. Available: 'CBC', 'BMP', 'Lipid Panel', 'HbA1c',
                   'INR', 'BNP', 'LFTs', 'TSH', 'Iron Studies', 'PFTs', 'DEXA Scan',
                   'Immunology', 'Urinalysis', 'HIV Panel', 'Drug Screen', and more.

    Returns:
        dict: Lab test results with values and interpretation.
    """
    if patient_id not in _LAB_DB:
        return {
            "status": "not_found",
            "message": (
                f"No lab results on file for patient '{patient_id}'. "
                f"Available patients with labs: {', '.join(_LAB_DB.keys())}"
            ),
        }

    patient_labs = _LAB_DB[patient_id]

    # Case-insensitive, partial match lookup
    matched_key = None
    test_lower = test_type.lower().replace(" ", "_")
    for key in patient_labs:
        if key.lower().replace(" ", "_") == test_lower or test_lower in key.lower().replace(" ", "_"):
            matched_key = key
            break

    if matched_key:
        return {
            "status": "success",
            "patient_id": patient_id,
            "test_type": matched_key,
            "results": patient_labs[matched_key],
            "retrieved_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

    available = ", ".join(patient_labs.keys())
    return {
        "status": "test_not_found",
        "message": f"No '{test_type}' results for patient '{patient_id}'. Available tests: {available}",
    }


def generate_soap_note(patient_id: str, chief_complaint: str, subjective: str,
                       objective_findings: dict, assessment: str,
                       plan: list[str]) -> dict:
    """Generates a structured SOAP clinical note for documentation.

    Args:
        patient_id: The patient identifier.
        chief_complaint: One-sentence reason for today's visit (e.g., 'Chest pain x 2 hours').
        subjective: Patient's reported symptoms, history of present illness, and relevant ROS.
        objective_findings: Dict of objective data (vitals, exam findings, labs).
                             Example: {'vitals': {'BP': '140/90', 'HR': 88},
                                       'physical_exam': 'Regular rate and rhythm, no murmurs',
                                       'labs': 'Troponin negative x2, BNP 380'}.
        assessment: Clinical assessment / working diagnosis with reasoning.
        plan: List of planned actions (medications, orders, referrals, follow-up).

    Returns:
        dict: Formatted SOAP note with timestamp, ready for EHR documentation.
    """
    patient = _PATIENT_DB.get(patient_id, {})
    patient_name = patient.get("name", f"Unknown (ID: {patient_id})")
    patient_age = patient.get("age", "Unknown")
    patient_gender = patient.get("gender", "Unknown")
    allergies = patient.get("allergies", [])
    medications = patient.get("current_medications", [])

    note_id = f"SOAP-{patient_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"

    # Format objective section
    obj_text = []
    for k, v in objective_findings.items():
        if isinstance(v, dict):
            sub = "; ".join(f"{sk}: {sv}" for sk, sv in v.items())
            obj_text.append(f"  {k.replace('_', ' ').title()}: {sub}")
        else:
            obj_text.append(f"  {k.replace('_', ' ').title()}: {v}")

    formatted_note = f"""
=== CLINICAL SOAP NOTE ===
Note ID: {note_id}
Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

PATIENT: {patient_name} | Age: {patient_age} | Gender: {patient_gender} | ID: {patient_id}
Allergies: {', '.join(allergies) if allergies else 'NKDA'}
Current Medications: {', '.join(medications) if medications else 'None'}

CHIEF COMPLAINT:
  {chief_complaint}

SUBJECTIVE:
  {subjective}

OBJECTIVE:
{chr(10).join(obj_text) if obj_text else '  No objective data provided.'}

ASSESSMENT:
  {assessment}

PLAN:
{chr(10).join(f'  {i+1}. {step}' for i, step in enumerate(plan))}

Electronically generated by Agentic Hospital AI — For educational/informational purposes.
Patient must be seen by licensed healthcare professional for definitive care.
"""

    # Store note
    note_record = {
        "note_id": note_id,
        "patient_id": patient_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "chief_complaint": chief_complaint,
        "subjective": subjective,
        "objective_findings": objective_findings,
        "assessment": assessment,
        "plan": plan,
        "formatted_text": formatted_note.strip(),
    }
    _SOAP_NOTES.append(note_record)

    return {
        "status": "generated",
        "note_id": note_id,
        "patient_name": patient_name,
        "formatted_soap_note": formatted_note.strip(),
        "summary": f"SOAP note generated for {patient_name} — Chief complaint: {chief_complaint}",
    }


def calculate_medication_dose(medication: str, weight_kg: float, age_years: int,
                               renal_egfr: float, hepatic_impairment: str) -> dict:
    """Calculates adjusted medication dosing based on patient-specific factors.

    Applies weight-based, age-adjusted, renal-adjusted, and hepatic-adjusted dosing.

    Args:
        medication: Generic medication name (e.g., 'amoxicillin', 'metformin', 'lisinopril',
                    'warfarin', 'furosemide', 'amlodipine', 'atorvastatin', 'gabapentin',
                    'sertraline', 'hydroxychloroquine', 'amiodarone').
        weight_kg: Patient weight in kilograms.
        age_years: Patient age in years.
        renal_egfr: Estimated GFR in mL/min/1.73m² (use 90 if normal, <15 if dialysis-dependent).
        hepatic_impairment: Degree of liver impairment: 'none', 'mild', 'moderate', or 'severe'.

    Returns:
        dict: Recommended dosing, adjustments, monitoring parameters, and contraindication flags.
    """
    med_key = medication.lower().strip()
    med_data = _MED_DOSING.get(med_key)

    if not med_data:
        return {
            "status": "not_found",
            "message": (
                f"Dosing data not available for '{medication}'. "
                f"Available medications: {', '.join(_MED_DOSING.keys())}. "
                "Consult pharmacy or prescribing reference for other medications."
            ),
        }

    # Determine renal adjustment tier
    if renal_egfr >= 60:
        renal_tier = "normal"
        renal_note = "Normal renal function — standard dosing."
        renal_adjustment = med_data["standard_adult"]
    elif renal_egfr >= 30:
        renal_tier = "moderate_ckd"
        renal_note = f"eGFR {renal_egfr} mL/min (CKD Stage 3) — dose adjustment may be required."
        renal_adjustment = med_data["renal_adjust"].get("egfr_30_60", med_data["standard_adult"])
    elif renal_egfr >= 10:
        renal_tier = "severe_ckd"
        renal_note = f"eGFR {renal_egfr} mL/min (CKD Stage 4) — significant dose reduction required."
        renal_adjustment = med_data["renal_adjust"].get("egfr_10_30", "Consult nephrology/pharmacy")
    else:
        renal_tier = "dialysis"
        renal_note = f"eGFR {renal_egfr} mL/min (CKD Stage 5 / ESRD) — consult nephrology."
        renal_adjustment = med_data["renal_adjust"].get("egfr_lt_10", "Consult nephrology/pharmacy")

    # Hepatic adjustment
    hepatic_note = med_data.get("hepatic_adjust", "No hepatic adjustment data available.")
    hepatic_caution = hepatic_impairment in ("moderate", "severe")

    # Age-specific flags
    age_flags = []
    if age_years >= 65:
        age_flags.append("Elderly patient (≥65): start at lower end of dosing range; monitor closely for adverse effects.")
        age_flags.append("Consider: Beers Criteria medications to avoid in elderly.")
    if age_years < 18:
        ped_dose = med_data.get("pediatric", "Pediatric dosing not established — consult pediatric pharmacist.")
        age_flags.append(f"Pediatric dosing: {ped_dose}")

    # Weight-based check (for weight-dosed medications)
    weight_note = None
    if med_key == "hydroxychloroquine":
        max_safe = weight_kg * 5  # 5 mg/kg/day max
        weight_note = f"Based on weight {weight_kg} kg: max safe dose = {round(max_safe)} mg/day (5 mg/kg/day to prevent retinopathy)."

    # Contraindication checks
    contraindications_triggered = []
    for contra in med_data.get("contraindications", []):
        if "egfr" in contra.lower() and "<30" in contra.lower() and renal_egfr < 30:
            contraindications_triggered.append(f"⚠ CONTRAINDICATED: {contra}")
        if "pregnan" in contra.lower():
            contraindications_triggered.append(f"⚠ CAUTION: {contra}")

    return {
        "status": "calculated",
        "medication": medication,
        "drug_class": med_data.get("class", "Unknown"),
        "patient_factors": {
            "weight_kg": weight_kg,
            "age_years": age_years,
            "renal_egfr": renal_egfr,
            "hepatic_impairment": hepatic_impairment,
        },
        "recommended_dosing": renal_adjustment,
        "standard_adult_dose": med_data["standard_adult"],
        "max_dose": med_data.get("max_dose", "Per clinical indication"),
        "renal_adjustment": {
            "tier": renal_tier,
            "note": renal_note,
            "adjusted_dose": renal_adjustment,
        },
        "hepatic_adjustment": {
            "impairment_level": hepatic_impairment,
            "note": hepatic_note,
            "caution_flag": hepatic_caution,
        },
        "age_specific_notes": age_flags,
        "weight_based_note": weight_note,
        "contraindications": contraindications_triggered,
        "monitoring_parameters": med_data.get("monitoring", []),
        "food_interactions": med_data.get("food", "No specific food interactions"),
        "disclaimer": "AI-calculated dosing for reference only. Always confirm with clinical pharmacist and prescriber.",
    }


def triage_assessment(symptoms: list[str], duration: str, severity: str) -> dict:
    """Performs initial triage assessment to determine urgency and recommended department.

    Args:
        symptoms: List of patient symptoms (e.g., ['chest pain', 'shortness of breath']).
        duration: How long symptoms have been present (e.g., '2 hours', '3 days', '1 week').
        severity: Patient-reported severity ('mild', 'moderate', 'severe', 'critical').

    Returns:
        dict: Triage result with urgency level, recommended department, triage score, and reasoning.
    """
    # Comprehensive symptom-to-department mapping with clinical priority scores (1–10)
    symptom_mapping = {
        # --- CARDIOLOGY ---
        "chest pain":                  ("Cardiology", 9),
        "chest tightness":             ("Cardiology", 8),
        "chest pressure":              ("Cardiology", 9),
        "palpitations":                ("Cardiology", 7),
        "heart palpitations":          ("Cardiology", 7),
        "irregular heartbeat":         ("Cardiology", 7),
        "arrhythmia":                  ("Cardiology", 7),
        "high blood pressure":         ("Cardiology", 6),
        "hypertension":                ("Cardiology", 6),
        "low blood pressure":          ("Cardiology", 8),
        "syncope":                     ("Cardiology", 8),
        "fainting":                    ("Cardiology", 7),
        "leg swelling":                ("Cardiology", 5),
        "bilateral leg swelling":      ("Cardiology", 6),
        "orthopnea":                   ("Cardiology", 7),
        "paroxysmal nocturnal dyspnea": ("Cardiology", 7),
        "cardiac arrest":              ("Emergency Medicine", 10),
        "heart failure":               ("Cardiology", 8),
        "pacemaker problem":           ("Cardiology", 8),
        # --- PULMONOLOGY ---
        "shortness of breath":         ("Pulmonology", 8),
        "dyspnea":                     ("Pulmonology", 8),
        "cough":                       ("Pulmonology", 4),
        "chronic cough":               ("Pulmonology", 5),
        "coughing up blood":           ("Pulmonology", 9),
        "hemoptysis":                  ("Pulmonology", 9),
        "wheezing":                    ("Pulmonology", 6),
        "stridor":                     ("Emergency Medicine", 9),
        "asthma":                      ("Pulmonology", 6),
        "copd":                        ("Pulmonology", 6),
        "breathing difficulty":        ("Pulmonology", 8),
        "respiratory distress":        ("Emergency Medicine", 10),
        "sleep apnea":                 ("Pulmonology", 5),
        "snoring":                     ("Pulmonology", 3),
        "pleural pain":                ("Pulmonology", 6),
        "pleuritic pain":              ("Pulmonology", 6),
        # --- NEUROLOGY ---
        "headache":                    ("Neurology", 5),
        "severe headache":             ("Neurology", 8),
        "thunderclap headache":        ("Emergency Medicine", 10),
        "migraine":                    ("Neurology", 5),
        "seizure":                     ("Neurology", 9),
        "convulsion":                  ("Neurology", 9),
        "epilepsy":                    ("Neurology", 7),
        "dizziness":                   ("Neurology", 6),
        "vertigo":                     ("Neurology", 6),
        "numbness":                    ("Neurology", 7),
        "tingling":                    ("Neurology", 6),
        "weakness":                    ("Neurology", 7),
        "confusion":                   ("Neurology", 8),
        "altered consciousness":       ("Emergency Medicine", 9),
        "memory loss":                 ("Neurology", 6),
        "dementia":                    ("Neurology", 5),
        "tremor":                      ("Neurology", 5),
        "speech difficulty":           ("Neurology", 8),
        "slurred speech":              ("Neurology", 8),
        "facial droop":                ("Emergency Medicine", 9),
        "arm weakness":                ("Emergency Medicine", 9),
        "stroke":                      ("Emergency Medicine", 10),
        "tia":                         ("Neurology", 8),
        "balance problem":             ("Neurology", 6),
        "vision change":               ("Neurology", 7),
        "double vision":               ("Neurology", 7),
        # --- NEPHROLOGY ---
        "kidney pain":                 ("Nephrology", 7),
        "flank pain":                  ("Nephrology", 6),
        "blood in urine":              ("Nephrology", 7),
        "hematuria":                   ("Nephrology", 7),
        "swelling":                    ("Nephrology", 5),
        "edema":                       ("Nephrology", 5),
        "urination problems":          ("Nephrology", 5),
        "decreased urination":         ("Nephrology", 8),
        "no urination":                ("Emergency Medicine", 9),
        "foamy urine":                 ("Nephrology", 6),
        "proteinuria":                 ("Nephrology", 6),
        "kidney stone":                ("Nephrology", 7),
        "dialysis":                    ("Nephrology", 7),
        # --- GASTROENTEROLOGY ---
        "abdominal pain":              ("Gastroenterology", 6),
        "stomach pain":                ("Gastroenterology", 6),
        "nausea":                      ("Gastroenterology", 4),
        "vomiting":                    ("Gastroenterology", 5),
        "diarrhea":                    ("Gastroenterology", 4),
        "blood in stool":              ("Gastroenterology", 8),
        "rectal bleeding":             ("Gastroenterology", 8),
        "black stool":                 ("Emergency Medicine", 9),
        "melena":                      ("Emergency Medicine", 9),
        "vomiting blood":              ("Emergency Medicine", 10),
        "hematemesis":                 ("Emergency Medicine", 10),
        "constipation":                ("Gastroenterology", 3),
        "heartburn":                   ("Gastroenterology", 4),
        "reflux":                      ("Gastroenterology", 4),
        "jaundice":                    ("Gastroenterology", 7),
        "yellow skin":                 ("Gastroenterology", 7),
        "liver pain":                  ("Gastroenterology", 6),
        "hepatitis":                   ("Gastroenterology", 6),
        "bloating":                    ("Gastroenterology", 3),
        "difficulty swallowing":       ("Gastroenterology", 6),
        "dysphagia":                   ("Gastroenterology", 6),
        # --- ORTHOPEDICS ---
        "joint pain":                  ("Orthopedics", 5),
        "back pain":                   ("Orthopedics", 5),
        "knee pain":                   ("Orthopedics", 5),
        "hip pain":                    ("Orthopedics", 5),
        "shoulder pain":               ("Orthopedics", 5),
        "fracture":                    ("Orthopedics", 8),
        "broken bone":                 ("Emergency Medicine", 9),
        "bone pain":                   ("Orthopedics", 6),
        "neck pain":                   ("Orthopedics", 5),
        "sports injury":               ("Orthopedics", 5),
        "ligament tear":               ("Orthopedics", 7),
        "tendon pain":                 ("Orthopedics", 5),
        "muscle weakness":             ("Orthopedics", 5),
        "scoliosis":                   ("Orthopedics", 4),
        "spinal pain":                 ("Orthopedics", 6),
        "radiculopathy":               ("Orthopedics", 6),
        "sciatica":                    ("Orthopedics", 6),
        # --- DERMATOLOGY ---
        "rash":                        ("Dermatology", 4),
        "skin rash":                   ("Dermatology", 4),
        "skin lesion":                 ("Dermatology", 5),
        "mole change":                 ("Dermatology", 6),
        "itching":                     ("Dermatology", 3),
        "pruritus":                    ("Dermatology", 3),
        "acne":                        ("Dermatology", 2),
        "eczema":                      ("Dermatology", 4),
        "psoriasis":                   ("Dermatology", 4),
        "hives":                       ("Dermatology", 5),
        "urticaria":                   ("Dermatology", 5),
        "skin infection":              ("Dermatology", 5),
        "hair loss":                   ("Dermatology", 3),
        "alopecia":                    ("Dermatology", 3),
        "nail problem":                ("Dermatology", 2),
        "wound":                       ("General Medicine", 4),
        "blistering rash":             ("Emergency Medicine", 8),
        # --- ENT ---
        "ear pain":                    ("ENT", 4),
        "earache":                     ("ENT", 4),
        "hearing loss":                ("ENT", 6),
        "tinnitus":                    ("ENT", 5),
        "ringing in ears":             ("ENT", 5),
        "sore throat":                 ("ENT", 3),
        "hoarseness":                  ("ENT", 5),
        "voice change":                ("ENT", 5),
        "nasal congestion":            ("ENT", 3),
        "sinus pain":                  ("ENT", 4),
        "sinusitis":                   ("ENT", 4),
        "nosebleed":                   ("ENT", 5),
        "epistaxis":                   ("ENT", 5),
        "swollen gland":               ("ENT", 4),
        "neck lump":                   ("ENT", 6),
        "swallowing difficulty":       ("ENT", 6),
        # --- PSYCHOLOGY ---
        "anxiety":                     ("Psychology", 5),
        "depression":                  ("Psychology", 6),
        "suicidal thoughts":           ("Psychology", 10),
        "self harm":                   ("Psychology", 9),
        "panic attack":                ("Psychology", 7),
        "panic":                       ("Psychology", 6),
        "insomnia":                    ("Psychology", 4),
        "sleep problems":              ("Psychology", 4),
        "hallucinations":              ("Psychology", 8),
        "delusions":                   ("Psychology", 8),
        "psychosis":                   ("Psychology", 9),
        "mood swings":                 ("Psychology", 5),
        "bipolar":                     ("Psychology", 7),
        "ptsd":                        ("Psychology", 6),
        "eating disorder":             ("Psychology", 6),
        "substance abuse":             ("Psychology", 6),
        "addiction":                   ("Psychology", 5),
        "stress":                      ("Psychology", 4),
        # --- GYNECOLOGY ---
        "menstrual problems":          ("Gynecology", 5),
        "menstrual pain":              ("Gynecology", 5),
        "abnormal period":             ("Gynecology", 5),
        "vaginal bleeding":            ("Gynecology", 7),
        "heavy bleeding":              ("Emergency Medicine", 9),
        "pregnancy":                   ("Gynecology", 6),
        "pregnant":                    ("Gynecology", 6),
        "prenatal":                    ("Gynecology", 5),
        "pelvic pain":                 ("Gynecology", 6),
        "ovarian pain":                ("Gynecology", 6),
        "breast lump":                 ("Gynecology", 7),
        "breast pain":                 ("Gynecology", 5),
        "vaginal discharge":           ("Gynecology", 4),
        "fertility":                   ("Gynecology", 5),
        "menopause":                   ("Gynecology", 4),
        # --- ONCOLOGY ---
        "lump":                        ("Oncology", 7),
        "mass":                        ("Oncology", 7),
        "unexplained weight loss":     ("Oncology", 7),
        "night sweats":                ("Oncology", 6),
        "cancer":                      ("Oncology", 8),
        "tumor":                       ("Oncology", 8),
        "lymph node swelling":         ("Oncology", 7),
        "bone pain at night":          ("Oncology", 7),
        "abnormal bleeding":           ("Oncology", 7),
        # --- GENERAL MEDICINE ---
        "fever":                       ("General Medicine", 5),
        "fatigue":                     ("General Medicine", 3),
        "tiredness":                   ("General Medicine", 3),
        "malaise":                     ("General Medicine", 4),
        "cold":                        ("General Medicine", 2),
        "flu":                         ("General Medicine", 4),
        "flu symptoms":                ("General Medicine", 4),
        "covid":                       ("General Medicine", 5),
        "infection":                   ("General Medicine", 5),
        "weight gain":                 ("General Medicine", 3),
        "obesity":                     ("General Medicine", 3),
        "preventive care":             ("General Medicine", 2),
        "checkup":                     ("General Medicine", 2),
        "vaccination":                 ("General Medicine", 2),
        # --- ENDOCRINOLOGY ---
        "diabetes":                    ("Endocrinology", 5),
        "high blood sugar":            ("Endocrinology", 6),
        "thyroid problem":             ("Endocrinology", 5),
        "thyroid swelling":            ("Endocrinology", 6),
        "hormonal problem":            ("Endocrinology", 5),
        "polydipsia":                  ("Endocrinology", 6),
        "polyuria":                    ("Endocrinology", 6),
        "heat intolerance":            ("Endocrinology", 5),
        "cold intolerance":            ("Endocrinology", 4),
        "adrenal":                     ("Endocrinology", 6),
        "cushing":                     ("Endocrinology", 6),
        "goiter":                      ("Endocrinology", 5),
        # --- HEMATOLOGY ---
        "anemia":                      ("Hematology", 6),
        "bleeding disorder":           ("Hematology", 7),
        "easy bruising":               ("Hematology", 5),
        "bruising":                    ("Hematology", 5),
        "blood clot":                  ("Hematology", 7),
        "dvt":                         ("Hematology", 8),
        "clotting problem":            ("Hematology", 7),
        "low platelets":               ("Hematology", 7),
        "sickle cell":                 ("Hematology", 7),
        # --- INFECTIOUS DISEASES ---
        "recurrent infection":         ("Infectious Diseases", 6),
        "hiv":                         ("Infectious Diseases", 7),
        "sepsis":                      ("Emergency Medicine", 10),
        "antibiotic resistant":        ("Infectious Diseases", 7),
        "tuberculosis":                ("Infectious Diseases", 7),
        "meningitis":                  ("Emergency Medicine", 10),
        "travel infection":            ("Infectious Diseases", 6),
        "malaria":                     ("Infectious Diseases", 7),
        # --- UROLOGY ---
        "urinary pain":                ("Urology", 5),
        "painful urination":           ("Urology", 5),
        "prostate problem":            ("Urology", 5),
        "urinary frequency":           ("Urology", 4),
        "testicular pain":             ("Urology", 7),
        "testicular swelling":         ("Urology", 7),
        "erectile dysfunction":        ("Urology", 4),
        "urinary retention":           ("Emergency Medicine", 8),
        # --- RHEUMATOLOGY ---
        "joint swelling":              ("Rheumatology", 6),
        "multiple joint pain":         ("Rheumatology", 6),
        "morning stiffness":           ("Rheumatology", 5),
        "autoimmune":                  ("Rheumatology", 6),
        "lupus":                       ("Rheumatology", 7),
        "rheumatoid":                  ("Rheumatology", 6),
        "fibromyalgia":                ("Rheumatology", 5),
        "gout":                        ("Rheumatology", 6),
        # --- OPHTHALMOLOGY ---
        "eye pain":                    ("Ophthalmology", 6),
        "vision loss":                 ("Ophthalmology", 8),
        "sudden vision loss":          ("Emergency Medicine", 10),
        "eye redness":                 ("Ophthalmology", 4),
        "blurred vision":              ("Ophthalmology", 6),
        "floaters":                    ("Ophthalmology", 7),
        "flashing lights":             ("Ophthalmology", 7),
        "eye injury":                  ("Ophthalmology", 8),
        "glaucoma":                    ("Ophthalmology", 7),
        # --- EMERGENCY MEDICINE ---
        "trauma":                      ("Emergency Medicine", 10),
        "accident":                    ("Emergency Medicine", 9),
        "overdose":                    ("Emergency Medicine", 10),
        "poisoning":                   ("Emergency Medicine", 10),
        "allergic reaction":           ("Emergency Medicine", 9),
        "anaphylaxis":                 ("Emergency Medicine", 10),
        "shock":                       ("Emergency Medicine", 10),
        "unconscious":                 ("Emergency Medicine", 10),
        "collapse":                    ("Emergency Medicine", 9),
        "burn":                        ("Emergency Medicine", 8),
        # --- PEDIATRICS ---
        "child illness":               ("Pediatrics", 5),
        "child fever":                 ("Pediatrics", 6),
        "developmental delay":         ("Pediatrics", 5),
        "vaccination child":           ("Pediatrics", 3),
        "infant feeding":              ("Pediatrics", 4),
        "growth concern":              ("Pediatrics", 4),
        # --- VASCULAR ---
        "leg pain walking":            ("Vascular Surgery", 6),
        "claudication":                ("Vascular Surgery", 6),
        "cold limb":                   ("Emergency Medicine", 9),
        "varicose veins":              ("Vascular Surgery", 3),
        "aortic aneurysm":             ("Vascular Surgery", 8),
        # --- NEUROSURGERY ---
        "brain tumor":                 ("Neurosurgery", 8),
        "spinal cord injury":          ("Neurosurgery", 9),
        "disc herniation":             ("Orthopedics", 6),
        "cauda equina":                ("Emergency Medicine", 10),
    }

    severity_multiplier = {
        "mild":     0.5,
        "moderate": 1.0,
        "severe":   1.5,
        "critical": 2.0,
    }

    department_scores: dict[str, float] = {}
    matched_symptoms = []
    multiplier = severity_multiplier.get(severity.lower(), 1.0)

    for symptom in symptoms:
        symptom_lower = symptom.lower().strip()
        for key, (dept, score) in symptom_mapping.items():
            if key in symptom_lower or symptom_lower in key:
                adjusted_score = score * multiplier
                department_scores[dept] = department_scores.get(dept, 0) + adjusted_score
                if symptom not in [m["symptom"] for m in matched_symptoms]:
                    matched_symptoms.append({
                        "symptom": symptom,
                        "matched_key": key,
                        "maps_to": dept,
                        "priority_score": adjusted_score,
                    })
                break  # use first match per symptom

    if not department_scores:
        return {
            "status": "assessed",
            "urgency": "routine",
            "recommended_department": "General Medicine",
            "triage_score": 3,
            "reasoning": "Symptoms don't match a specific specialty pattern. Recommend General Medicine for initial evaluation.",
            "matched_symptoms": [],
        }

    primary_dept = max(department_scores, key=lambda k: department_scores[k])
    max_score = department_scores[primary_dept]

    if max_score >= 15 or severity.lower() == "critical":
        urgency = "emergency"
    elif max_score >= 9 or severity.lower() == "severe":
        urgency = "urgent"
    else:
        urgency = "routine"

    all_depts_sorted = dict(sorted(department_scores.items(), key=lambda x: x[1], reverse=True))

    return {
        "status": "assessed",
        "urgency": urgency,
        "recommended_department": primary_dept,
        "triage_score": round(max_score, 1),
        "severity_input": severity,
        "duration": duration,
        "all_departments_involved": all_depts_sorted,
        "matched_symptoms": matched_symptoms,
        "reasoning": (
            f"Primary concern maps to {primary_dept} with triage score {max_score:.1f} "
            f"(severity: {severity}, duration: {duration}). "
            f"{len(matched_symptoms)} symptom(s) identified across "
            f"{len(department_scores)} department(s)."
        ),
    }


# =============================================================================
# EPISODIC PATIENT MEMORY
# =============================================================================
_PATIENT_ENCOUNTERS: dict[str, list] = {}


def record_patient_encounter(
    patient_id: str,
    department: str,
    chief_complaint: str,
    diagnosis: str,
    plan: list[str],
    follow_up_date: Optional[str] = None,
) -> dict:
    """Records a completed clinical encounter to the patient's longitudinal history.

    Call this at the END of every consultation to preserve clinical context for future visits.

    Args:
        patient_id: The patient identifier (P001–P010).
        department: Name of the treating department (e.g., 'Cardiology', 'Neurology').
        chief_complaint: One-sentence reason for today's visit.
        diagnosis: Working or confirmed diagnosis from this encounter.
        plan: List of planned actions (medications, referrals, follow-up steps).
        follow_up_date: Optional target follow-up date (e.g., '4 weeks', '2026-03-15').

    Returns:
        dict: Encounter record confirmation with encounter ID and longitudinal summary.
    """
    encounter = {
        "encounter_id": f"ENC-{patient_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
        "patient_id": patient_id,
        "department": department,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "chief_complaint": chief_complaint,
        "diagnosis": diagnosis,
        "plan": plan,
        "follow_up_date": follow_up_date or "As clinically indicated",
    }

    if patient_id not in _PATIENT_ENCOUNTERS:
        _PATIENT_ENCOUNTERS[patient_id] = []
    _PATIENT_ENCOUNTERS[patient_id].append(encounter)

    total_encounters = len(_PATIENT_ENCOUNTERS[patient_id])
    patient_name = _PATIENT_DB.get(patient_id, {}).get("name", patient_id)

    return {
        "status": "recorded",
        "encounter_id": encounter["encounter_id"],
        "patient_name": patient_name,
        "total_encounters_on_file": total_encounters,
        "encounter_summary": {
            "department": department,
            "diagnosis": diagnosis,
            "plan_steps": len(plan),
            "follow_up": follow_up_date or "As clinically indicated",
        },
        "message": (
            f"Encounter recorded for {patient_name}. "
            f"This patient now has {total_encounters} encounter(s) on file."
        ),
    }


def get_patient_encounter_history(
    patient_id: str,
    last_n: int = 5,
    department_filter: Optional[str] = None,
) -> dict:
    """Retrieves a patient's longitudinal encounter history for clinical context.

    Call this at the START of every consultation to provide continuity of care.

    Args:
        patient_id: The patient identifier (P001–P010).
        last_n: Number of most recent encounters to retrieve (default 5, max 20).
        department_filter: Optional — filter to a specific department (e.g., 'Cardiology').

    Returns:
        dict: Chronological encounter history with diagnoses, plans, and follow-up dates.
    """
    if patient_id not in _PATIENT_ENCOUNTERS or not _PATIENT_ENCOUNTERS[patient_id]:
        patient_name = _PATIENT_DB.get(patient_id, {}).get("name", patient_id)
        return {
            "status": "no_history",
            "patient_id": patient_id,
            "patient_name": patient_name,
            "encounters": [],
            "message": (
                f"No prior encounter history for {patient_name}. "
                "This appears to be their first recorded visit in the system."
            ),
        }

    encounters = _PATIENT_ENCOUNTERS[patient_id]

    if department_filter:
        encounters = [
            e for e in encounters
            if department_filter.lower() in e["department"].lower()
        ]

    last_n = min(last_n, 20)
    recent = encounters[-last_n:][::-1]  # most recent first

    departments_seen = list({e["department"] for e in encounters})
    diagnoses_list = list({e["diagnosis"] for e in encounters if e["diagnosis"]})
    patient_name = _PATIENT_DB.get(patient_id, {}).get("name", patient_id)

    return {
        "status": "found",
        "patient_id": patient_id,
        "patient_name": patient_name,
        "total_encounters": len(_PATIENT_ENCOUNTERS[patient_id]),
        "encounters_returned": len(recent),
        "departments_seen": departments_seen,
        "prior_diagnoses": diagnoses_list,
        "encounters": recent,
        "clinical_context": (
            f"{patient_name} has {len(_PATIENT_ENCOUNTERS[patient_id])} prior encounter(s). "
            f"Departments visited: {', '.join(departments_seen)}. "
            f"Prior diagnoses include: {', '.join(diagnoses_list[:5]) if diagnoses_list else 'None recorded'}."
        ),
    }


# =============================================================================
# MDT (MULTI-DISCIPLINARY TEAM) CONSULTATION
# =============================================================================

_VALID_DEPARTMENTS = {
    "allergy_immunology", "anesthesiology", "cardiology", "cardiothoracic_surgery",
    "colorectal_surgery", "critical_care", "dermatology", "emergency_medicine",
    "endocrinology", "ent", "gastroenterology", "general_medicine", "general_surgery",
    "gynecology", "hematology", "infectious_diseases", "nephrology", "neurology",
    "neurosurgery", "nuclear_medicine", "oncology", "ophthalmology", "orthopedics",
    "pathology", "pediatrics", "physical_medicine_rehab", "plastic_surgery",
    "psychology", "pulmonology", "radiation_oncology", "radiology", "rheumatology",
    "thoracic_surgery", "urology", "vascular_surgery",
}

_MDT_CONSULTATIONS: list[dict] = []


def request_mdt_consultation(
    patient_id: str,
    departments: list[str],
    clinical_question: str,
    urgency: str = "routine",
) -> dict:
    """Initiates a Multi-Disciplinary Team (MDT) consultation for complex cases.

    Use when a patient's presentation spans multiple organ systems or requires
    input from more than one specialty simultaneously (e.g., diabetic foot ulcer
    needing Vascular Surgery + Infectious Diseases + Endocrinology + Nephrology).

    The coordinator will then route to each listed department agent in turn and
    synthesize a unified care plan from all specialist responses.

    Args:
        patient_id: The patient identifier (P001–P010).
        departments: List of department names to consult (e.g., ['cardiology', 'nephrology']).
                     Use snake_case department names.
        clinical_question: The specific question or decision requiring multi-specialist input.
        urgency: Consultation urgency — 'routine', 'urgent', or 'emergency'.

    Returns:
        dict: MDT consultation request with routing plan, rationale, and coordination notes.
    """
    patient = _PATIENT_DB.get(patient_id, {})
    patient_name = patient.get("name", patient_id)

    # Validate and normalize departments
    valid = []
    invalid = []
    for dept in departments:
        normalized = dept.lower().replace(" ", "_").replace("-", "_")
        if normalized in _VALID_DEPARTMENTS:
            valid.append(normalized)
        else:
            # Try partial match
            matches = [d for d in _VALID_DEPARTMENTS if normalized in d or d in normalized]
            if matches:
                valid.append(matches[0])
            else:
                invalid.append(dept)

    if not valid:
        return {
            "status": "error",
            "message": f"No valid departments found. Please use department names from: {', '.join(sorted(_VALID_DEPARTMENTS))}",
        }

    consultation_id = f"MDT-{patient_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Build per-department focus areas
    dept_focus_map = {
        "cardiology":          "Cardiac function, arrhythmia management, hemodynamic optimization",
        "nephrology":          "Renal function, electrolytes, medication dosing in CKD, dialysis planning",
        "endocrinology":       "Glycemic control, thyroid/adrenal function, metabolic optimization",
        "hematology":          "Anticoagulation management, blood dyscrasias, transfusion planning",
        "infectious_diseases": "Antimicrobial selection, stewardship, infection source control",
        "oncology":            "Tumor staging, treatment eligibility, chemotherapy planning",
        "pulmonology":         "Respiratory optimization, ventilator weaning, obstructive/restrictive disease",
        "neurology":           "Neurological risk, seizure management, stroke prevention",
        "vascular_surgery":    "Vascular access, ischemia assessment, revascularization planning",
        "general_surgery":     "Surgical risk, operative planning, wound management",
        "rheumatology":        "Autoimmune flare management, immunosuppression adjustment",
        "gastroenterology":    "GI bleed risk, liver function, nutrition support",
        "critical_care":       "ICU-level monitoring, organ support, sepsis management",
        "radiology":           "Imaging selection, image-guided procedures",
        "pathology":           "Biopsy interpretation, lab critical values",
        "anesthesiology":      "Perioperative risk, anesthetic planning",
    }

    routing_plan = []
    for dept in valid:
        focus = dept_focus_map.get(dept, f"Specialist evaluation from {dept.replace('_', ' ').title()}")
        routing_plan.append({
            "department": dept.replace("_", " ").title(),
            "agent": f"{dept}_agent",
            "focus_area": focus,
        })

    urgency_instructions = {
        "emergency": "ACTIVATE NOW — all specialists to be contacted simultaneously within 30 minutes.",
        "urgent":    "All specialists to respond within 2–4 hours. Coordinate via charge nurse.",
        "routine":   "MDT meeting to be scheduled within 48–72 hours. Coordinator to compile responses.",
    }

    record = {
        "consultation_id": consultation_id,
        "patient_id": patient_id,
        "patient_name": patient_name,
        "urgency": urgency,
        "clinical_question": clinical_question,
        "departments_requested": valid,
        "routing_plan": routing_plan,
        "requested_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    _MDT_CONSULTATIONS.append(record)

    return {
        "status": "mdt_initiated",
        "consultation_id": consultation_id,
        "patient_name": patient_name,
        "departments_to_consult": len(valid),
        "routing_plan": routing_plan,
        "clinical_question": clinical_question,
        "urgency": urgency,
        "coordination_instructions": urgency_instructions.get(urgency, urgency_instructions["routine"]),
        "invalid_departments": invalid if invalid else None,
        "coordinator_action": (
            f"Route {patient_name} ({patient_id}) to each of the {len(valid)} specialist agents listed "
            f"in routing_plan, asking each to address their focus_area in the context of: "
            f"'{clinical_question}'. Synthesize all responses into a unified MDT care plan."
        ),
    }


# =============================================================================
# EVIDENCE-BASED TREATMENT PROTOCOL GENERATOR
# =============================================================================

_TREATMENT_PROTOCOLS: dict[str, dict] = {
    # ── CARDIOLOGY ──────────────────────────────────────────────────────────
    "stemi": {
        "full_name": "ST-Elevation Myocardial Infarction",
        "department": "Cardiology",
        "emergency": True,
        "first_line": [
            "Activate cardiac catheterization lab immediately (door-to-balloon time <90 min)",
            "Dual antiplatelet: Aspirin 325 mg PO stat + Ticagrelor 180 mg PO (or Clopidogrel 600 mg if ticagrelor unavailable)",
            "Anticoagulation: Heparin UFH 60 units/kg IV bolus (max 4000 units) + infusion",
            "Primary PCI (preferred) or thrombolytics if PCI not available within 120 min",
            "High-intensity statin: Atorvastatin 80 mg PO stat",
            "Beta-blocker (if no contraindication): Metoprolol 25–50 mg PO",
        ],
        "second_line": [
            "If PCI not feasible within 120 min: Tenecteplase weight-based IV bolus",
            "Consider GP IIb/IIIa inhibitor (eptifibatide) for high thrombus burden",
            "ACE inhibitor within 24h if LVEF <40%: Lisinopril 2.5–5 mg PO, uptitrate",
        ],
        "monitoring": [
            "Troponin I/T every 3–6 hours (peak at 12–24h)",
            "12-lead ECG every 30 min until ST resolution",
            "Continuous cardiac monitoring in CCU",
            "Daily CBC, BMP, lipid panel",
            "Echocardiogram within 24h (assess EF, wall motion, mechanical complications)",
        ],
        "follow_up": "Cardiology clinic 1–2 weeks post-discharge; cardiac rehab referral",
        "evidence_grade": "Class I, Level A — ACC/AHA STEMI Guidelines 2022",
    },
    "atrial_fibrillation": {
        "full_name": "Atrial Fibrillation",
        "department": "Cardiology",
        "emergency": False,
        "first_line": [
            "Rate control (target HR <80 bpm at rest): Metoprolol succinate 25–200 mg daily or Diltiazem 120–360 mg daily (if no HFrEF)",
            "Anticoagulation if CHA₂DS₂-VASc ≥2 (males) or ≥3 (females): DOAC preferred (Apixaban 5 mg BID, Rivaroxaban 20 mg daily with evening meal)",
            "Warfarin if DOAC contraindicated (target INR 2.0–3.0)",
            "Lifestyle: alcohol cessation, weight loss, treat sleep apnea, manage hypertension",
        ],
        "second_line": [
            "Rhythm control (if symptomatic despite rate control): Flecainide, Propafenone (no structural disease), or Amiodarone (structural disease)",
            "DC cardioversion if hemodynamically unstable or <48h duration with anticoagulation",
            "Catheter ablation for symptomatic paroxysmal AF failing antiarrhythmic drugs",
        ],
        "monitoring": [
            "INR weekly until stable (if on Warfarin), then monthly",
            "Annual renal function (DOAC dose adjustment)",
            "ECG at each visit; Holter if symptom recurrence",
            "Thyroid function (TSH) — hyperthyroidism as precipitant",
        ],
        "follow_up": "Cardiology follow-up 4–6 weeks; annual thereafter if stable",
        "evidence_grade": "Class I, Level A — ACC/AHA/HRS AF Guidelines 2023",
    },
    "heart_failure_hfref": {
        "full_name": "Heart Failure with Reduced EF (HFrEF, EF <40%)",
        "department": "Cardiology",
        "emergency": False,
        "first_line": [
            "ACE inhibitor (or ARB if ACE intolerant): Lisinopril titrate to 40 mg daily",
            "Beta-blocker: Carvedilol 3.125 mg BID titrate to 25 mg BID, or Metoprolol succinate",
            "Mineralocorticoid antagonist (if eGFR >30 + K+ <5.0): Spironolactone 25–50 mg daily",
            "SGLT2 inhibitor: Dapagliflozin 10 mg daily or Empagliflozin 10 mg daily",
            "ARNI (preferred over ACE/ARB): Sacubitril/Valsartan (Entresto) 49/51 mg BID if tolerating ACEi",
            "Diuresis for fluid overload: Furosemide titrate to symptom-free euvolemia",
        ],
        "second_line": [
            "Ivabradine if HR >70 bpm on max beta-blocker and LVEF ≤35%",
            "Hydralazine + nitrate (if ACE/ARB/ARNI not tolerated, especially in Black patients)",
            "ICD if LVEF ≤35% despite 3+ months GDMT (if EF doesn't improve)",
            "CRT if LBBB + QRS ≥150 ms + LVEF ≤35%",
        ],
        "monitoring": [
            "BMP (renal function + electrolytes) within 1–2 weeks of ACEi/ARB start or dose change",
            "Daily weights — instruct patient to call if +2 lbs in 1 day or +5 lbs in 1 week",
            "BNP/NT-proBNP at baseline and if acute decompensation",
            "Echocardiogram 3–6 months after starting GDMT",
        ],
        "follow_up": "HF clinic every 2–4 weeks until stable; then every 3–6 months",
        "evidence_grade": "Class I, Level A — ACC/AHA/HFSA HF Guidelines 2022",
    },
    "hypertension": {
        "full_name": "Hypertension",
        "department": "Cardiology / General Medicine",
        "emergency": False,
        "first_line": [
            "Lifestyle modification: DASH diet, sodium restriction (<2.3 g/day), aerobic exercise 90–150 min/week, weight loss",
            "ACE inhibitor or ARB (first-line if DM or CKD): Lisinopril 10 mg daily, uptitrate to 40 mg",
            "Calcium channel blocker: Amlodipine 5–10 mg daily",
            "Thiazide diuretic: Chlorthalidone 12.5–25 mg daily (preferred over HCTZ for 24h effect)",
            "BP target: <130/80 mmHg for most patients (ACC/AHA 2017)",
        ],
        "second_line": [
            "Combination therapy if BP >20/10 above target: start 2-drug combo",
            "Beta-blocker if concurrent CAD/HF/high HR: Metoprolol 25–100 mg daily",
            "Spironolactone 25 mg daily for resistant hypertension (4th-line)",
        ],
        "monitoring": [
            "BP check at 1 month after initiation; then every 3 months until at target",
            "BMP at 1 month (ACEi/ARB — creatinine + potassium)",
            "Home BP monitoring: twice daily for 1 week per month",
            "Annual: lipid panel, glucose, urine microalbumin",
        ],
        "follow_up": "1 month after any medication change; annually once stable",
        "evidence_grade": "Class I, Level A — ACC/AHA Hypertension Guidelines 2017",
    },
    # ── PULMONOLOGY ──────────────────────────────────────────────────────────
    "copd_exacerbation": {
        "full_name": "COPD Acute Exacerbation",
        "department": "Pulmonology",
        "emergency": True,
        "first_line": [
            "Short-acting bronchodilator: Albuterol 2.5 mg nebulized every 20 min x3, then q4h",
            "Short-acting anticholinergic: Ipratropium 0.5 mg nebulized q4h",
            "Systemic corticosteroid: Prednisolone 40 mg PO daily x5 days (non-inferior to longer courses)",
            "Antibiotic (if purulent sputum or clinical infection): Azithromycin 500 mg x1 then 250 mg daily x4 days or Doxycycline 100 mg BID x5 days",
            "Controlled O2 therapy: Target SpO2 88–92% (avoid hyperoxia in CO2 retainers)",
            "Consider NIV (BiPAP) if pH <7.35 + PaCO2 >45 mmHg + RR >25 despite bronchodilators",
        ],
        "second_line": [
            "IV aminophylline if inadequate response to nebulized bronchodilators",
            "Invasive mechanical ventilation if NIV fails or contraindicated",
            "Heliox (79% He / 21% O2) for severe airflow obstruction refractory to standard treatment",
        ],
        "monitoring": [
            "ABG within 1 hour of starting O2 (assess CO2 retention)",
            "SpO2 continuously; RR, HR every 30 min",
            "Repeat ABG if mental status changes or SpO2 drops",
            "Sputum culture if purulent; CXR to exclude pneumonia/pneumothorax",
        ],
        "follow_up": "Pulmonology within 2–4 weeks; COPD action plan provided",
        "evidence_grade": "Class I, Level A — GOLD COPD Guidelines 2024",
    },
    "pulmonary_embolism": {
        "full_name": "Pulmonary Embolism (PE)",
        "department": "Pulmonology / Hematology",
        "emergency": True,
        "first_line": [
            "Risk stratify: Massive (SBP <90), Submassive (RV dysfunction, elevated troponin), Low-risk (none)",
            "Anticoagulation (if no contraindication): Apixaban 10 mg BID x7 days then 5 mg BID, OR Rivaroxaban 15 mg BID x21 days then 20 mg daily",
            "Heparin bridge if using Warfarin: UFH IV weight-based or Enoxaparin 1 mg/kg SC BID",
            "Supplemental O2 to maintain SpO2 ≥95%",
            "Systemic thrombolysis (massive PE): Alteplase 100 mg IV over 2h if no contraindications",
        ],
        "second_line": [
            "Catheter-directed thrombolysis (submassive with deterioration)",
            "Surgical embolectomy if thrombolytics contraindicated and massive PE",
            "IVC filter only if anticoagulation absolutely contraindicated",
        ],
        "monitoring": [
            "Serial troponin and BNP (RV strain markers)",
            "Echocardiogram for RV function assessment",
            "Lower extremity Doppler (concurrent DVT)",
            "Renal function at 2 weeks (DOAC dose adjustment if needed)",
            "Extended anticoagulation discussion at 3 months: provoked vs unprovoked",
        ],
        "follow_up": "Pulmonology + Hematology at 3 months; consider thrombophilia workup",
        "evidence_grade": "Class I, Level A — ESC PE Guidelines 2019/AHA 2023",
    },
    # ── NEUROLOGY ────────────────────────────────────────────────────────────
    "ischemic_stroke": {
        "full_name": "Acute Ischemic Stroke",
        "department": "Neurology",
        "emergency": True,
        "first_line": [
            "Activate stroke protocol — door-to-CT <25 min, door-to-needle <60 min",
            "Non-contrast CT head immediately (rule out hemorrhage)",
            "IV alteplase 0.9 mg/kg (max 90 mg): 10% as bolus, remainder over 60 min — if within 4.5h onset + no contraindications",
            "Mechanical thrombectomy if large vessel occlusion within 24h of onset (CT perfusion guided)",
            "Aspirin 325 mg PO (if no thrombolytics given, or after 24h if thrombolytics used)",
            "Admit to stroke unit; NPO until swallow screen; HOB flat initially",
            "Blood glucose management: target 140–180 mg/dL",
        ],
        "second_line": [
            "Dual antiplatelet (Aspirin + Clopidogrel) for 21 days if minor stroke/TIA",
            "BP management: lower only if >220/120 (unless thrombolytics — then <185/110)",
            "Statin high-intensity: Atorvastatin 80 mg",
        ],
        "monitoring": [
            "Neurological checks every 1h x12h, then q2h x12h",
            "NIHSS score serially",
            "Cardiac monitoring 24–72h (detect paroxysmal AF)",
            "MRI brain with DWI within 24h",
            "Carotid imaging (ultrasound or CTA) for anterior circulation stroke",
        ],
        "follow_up": "Neurology at 1 week, 1 month, 3 months; stroke rehab referral",
        "evidence_grade": "Class I, Level A — AHA/ASA Stroke Guidelines 2019 (updated 2022)",
    },
    "epilepsy": {
        "full_name": "Epilepsy / Seizure Disorder",
        "department": "Neurology",
        "emergency": False,
        "first_line": [
            "Focal seizures: Levetiracetam 500 mg BID (titrate to 1500 mg BID) — well tolerated, minimal interactions",
            "Generalized tonic-clonic: Valproic acid 500 mg BID (avoid in women of childbearing age) or Levetiracetam",
            "Absence seizures: Ethosuximide 250 mg BID or Valproate",
            "Driving restrictions: counsel patient (varies by jurisdiction — typically 6 months seizure-free)",
        ],
        "second_line": [
            "Lamotrigine 25 mg daily (slow titration to avoid SJS, especially with Valproate)",
            "Lacosamide 50 mg BID if focal with incomplete response",
            "Surgical evaluation if 2 AEDs fail (drug-resistant epilepsy)",
        ],
        "monitoring": [
            "Seizure diary maintained by patient",
            "AED levels if toxicity suspected or poor adherence",
            "Annual: CBC, LFTs (Valproate hepatotoxicity), bone density (enzyme-inducing AEDs)",
            "EEG at baseline; repeat if clinical change",
            "MRI brain (baseline if new diagnosis to rule out structural cause)",
        ],
        "follow_up": "Neurology every 3–6 months; sooner if seizure recurrence",
        "evidence_grade": "Class I, Level A — AAN Epilepsy Practice Guidelines 2018",
    },
    # ── NEPHROLOGY ───────────────────────────────────────────────────────────
    "ckd_management": {
        "full_name": "Chronic Kidney Disease (CKD) Management",
        "department": "Nephrology",
        "emergency": False,
        "first_line": [
            "ACE inhibitor or ARB: Lisinopril/Losartan (reduce proteinuria, slow progression) — titrate to maximum tolerated dose",
            "SGLT2 inhibitor: Dapagliflozin 10 mg daily (reduces CKD progression regardless of DM — if eGFR ≥25)",
            "BP target <130/80 mmHg",
            "Dietary protein restriction: 0.8 g/kg/day (CKD 3–5)",
            "Phosphate restriction if hyperphosphatemia; Phosphate binders if needed",
            "Erythropoiesis-stimulating agent if Hgb <10 g/dL with iron repletion",
            "Bicarbonate supplementation if HCO3 <22 mEq/L",
        ],
        "second_line": [
            "Finerenone (non-steroidal MRA) for CKD with DM if tolerating max RAAS blockade",
            "Dialysis planning: refer for AV fistula when eGFR <15–20",
            "Kidney transplant evaluation when eGFR <20",
        ],
        "monitoring": [
            "BMP every 3 months (CKD 3b–4) — monitor K+, HCO3, Cr, eGFR",
            "Urine microalbumin/creatinine ratio every 6 months",
            "CBC every 6 months (anemia)",
            "Phosphorus, calcium, PTH, Vitamin D every 6–12 months (CKD 4–5)",
            "Renal ultrasound if rapid progression",
        ],
        "follow_up": "Nephrology every 3–6 months; education on dietary management",
        "evidence_grade": "Class I, Level A — KDIGO CKD Guidelines 2022",
    },
    # ── ENDOCRINOLOGY ─────────────────────────────────────────────────────────
    "type2_diabetes": {
        "full_name": "Type 2 Diabetes Mellitus",
        "department": "Endocrinology / General Medicine",
        "emergency": False,
        "first_line": [
            "Metformin 500 mg BID with meals; titrate to 2000 mg/day over 4 weeks (if eGFR ≥30)",
            "SGLT2 inhibitor (if CVD/HF/CKD): Empagliflozin 10 mg or Dapagliflozin 10 mg daily",
            "GLP-1 agonist (if obesity/CVD): Semaglutide 0.25 mg SC weekly, titrate to 1 mg",
            "HbA1c target: <7.0% (most patients); <8.0% if elderly/multiple comorbidities",
            "Lifestyle: Medical nutrition therapy, 150 min aerobic exercise/week",
            "Statin if age >40 or ASCVD risk >10%: Atorvastatin 40–80 mg",
            "ACE inhibitor if microalbuminuria or hypertension",
        ],
        "second_line": [
            "DPP-4 inhibitor (weight-neutral, well-tolerated): Sitagliptin 100 mg daily",
            "Insulin: Basal insulin (glargine) if HbA1c >10% or significant symptoms",
            "Add prandial insulin if HbA1c remains >9% on basal insulin",
        ],
        "monitoring": [
            "HbA1c every 3 months until at goal, then every 6 months",
            "Annual: fasting lipid panel, urine microalbumin, eGFR, foot exam, dilated eye exam",
            "SMBG or CGM (Dexcom/Libre) — frequency per insulin regimen",
            "BP at every visit; target <130/80",
        ],
        "follow_up": "Endocrinology/primary care every 3 months; diabetes education referral",
        "evidence_grade": "Class I, Level A — ADA Standards of Care 2024",
    },
    "hypothyroidism": {
        "full_name": "Hypothyroidism",
        "department": "Endocrinology",
        "emergency": False,
        "first_line": [
            "Levothyroxine: Start 1.6 mcg/kg/day (reduce to 1.0–1.3 mcg/kg in elderly/CAD)",
            "Take on empty stomach 30–60 min before breakfast (absorption maximized)",
            "TSH target: 0.5–2.5 mIU/L for most patients; 1.0–2.0 for pregnancy",
        ],
        "second_line": [
            "Combination T4/T3 (Levothyroxine + Liothyronine) for persistent symptoms despite normal TSH — evidence limited but may benefit some",
            "Desiccated thyroid extract (DTE) as alternative — monitor both TSH and free T4",
        ],
        "monitoring": [
            "TSH at 6 weeks after initiation or dose change",
            "TSH every 6–12 months when stable",
            "Lipid panel (hypothyroidism raises LDL)",
            "During pregnancy: TSH every 4 weeks in first trimester, 4–6 weeks thereafter",
        ],
        "follow_up": "Endocrinology at 6 weeks, then annually; sooner if symptomatic",
        "evidence_grade": "Class I, Level A — ATA Hypothyroidism Guidelines 2014 (updated)",
    },
    # ── INFECTIOUS DISEASES ───────────────────────────────────────────────────
    "community_acquired_pneumonia": {
        "full_name": "Community-Acquired Pneumonia (CAP)",
        "department": "Infectious Diseases / General Medicine",
        "emergency": False,
        "first_line": [
            "Outpatient (mild, no comorbidities): Amoxicillin 1 g TID x5 days OR Doxycycline 100 mg BID x5 days",
            "Outpatient (comorbidities/atypical): Amoxicillin-clavulanate 875/125 mg BID + Azithromycin 500 mg x1 then 250 mg daily x4 days",
            "Inpatient (non-ICU): Beta-lactam (ceftriaxone 1 g IV daily) + Azithromycin OR Respiratory fluoroquinolone (Levofloxacin 750 mg x5 days)",
            "ICU: Beta-lactam + Azithromycin + consider anti-MRSA if risk factors (Vancomycin/Linezolid)",
            "Aspiration: Add anaerobic coverage — Metronidazole 500 mg TID or Amoxicillin-clavulanate",
        ],
        "second_line": [
            "MRSA CAP: Vancomycin 15–20 mg/kg IV q8–12h or Linezolid 600 mg IV/PO BID",
            "Pseudomonal risk (structural lung disease, immunosuppression): Piperacillin-tazobactam or Cefepime",
            "Legionella (positive urinary antigen): Levofloxacin 750 mg daily x5 days",
        ],
        "monitoring": [
            "CXR at baseline; repeat at 4–6 weeks to confirm resolution (rule out malignancy if slow to clear)",
            "O2 saturation; target >94%",
            "Blood cultures x2 before antibiotics (if ICU or hospitalized)",
            "Legionella and pneumococcal urinary antigens (if hospitalized)",
            "Temperature curve, WBC trend",
        ],
        "follow_up": "GP at 4–6 weeks; repeat CXR if age >50 or smoker",
        "evidence_grade": "Class I, Level A — IDSA/ATS CAP Guidelines 2019",
    },
    "sepsis": {
        "full_name": "Sepsis / Septic Shock",
        "department": "Critical Care / Infectious Diseases",
        "emergency": True,
        "first_line": [
            "Hour-1 Sepsis Bundle (SSCG 2021):",
            "1. Blood cultures x2 BEFORE antibiotics",
            "2. Broad-spectrum antibiotics within 1 hour: Piperacillin-tazobactam 4.5 g IV q6h + Vancomycin 25 mg/kg IV",
            "3. Lactate measurement (repeat if initial >2 mmol/L)",
            "4. IV crystalloid 30 mL/kg if hypotension or lactate ≥4 mmol/L",
            "5. Norepinephrine for fluid-refractory shock (target MAP ≥65 mmHg)",
            "Vasopressin 0.03 units/min (add-on to norepinephrine)",
        ],
        "second_line": [
            "Corticosteroids (septic shock refractory to fluids + vasopressors): Hydrocortisone 200 mg/day IV (continuous infusion or q6h)",
            "De-escalate antibiotics within 48–72h based on cultures",
            "Source control: drain abscess, remove infected catheter, surgical debridement as indicated",
        ],
        "monitoring": [
            "Lactate every 2h until normalizing",
            "Hourly urine output (target >0.5 mL/kg/h)",
            "Serial lactates, CBC, BMP, coagulation panel",
            "Procalcitonin (guide antibiotic duration — stop at <0.25 ng/mL)",
            "ICU monitoring: arterial line, central venous access if vasopressors",
        ],
        "follow_up": "ICU until hemodynamically stable; post-ICU syndrome follow-up at 3 months",
        "evidence_grade": "Class I, Level A — Surviving Sepsis Campaign 2021",
    },
    # ── ONCOLOGY ─────────────────────────────────────────────────────────────
    "breast_cancer_early": {
        "full_name": "Early-Stage Breast Cancer (Stage I–II)",
        "department": "Oncology",
        "emergency": False,
        "first_line": [
            "Surgery: Breast-conserving surgery (lumpectomy) + sentinel lymph node biopsy — preferred if feasible",
            "Mastectomy if large tumor-to-breast ratio, multicentric, or patient preference",
            "Adjuvant radiation: Whole-breast irradiation after BCS",
            "ER/PR+ (most breast cancers): Endocrine therapy x5–10 years",
            "  Pre-menopausal: Tamoxifen 20 mg daily",
            "  Post-menopausal: Aromatase inhibitor (Anastrozole 1 mg, Letrozole 2.5 mg, or Exemestane 25 mg daily)",
            "HER2+: Trastuzumab-based chemotherapy x1 year (pertuzumab if node-positive)",
        ],
        "second_line": [
            "CDK4/6 inhibitor (Palbociclib/Ribociclib) + AI for high-risk HR+ node-positive",
            "Neoadjuvant chemotherapy if HER2+ or triple-negative (to allow BCS)",
            "Olaparib (PARP inhibitor) for BRCA1/2 carriers with HER2-negative cancer",
        ],
        "monitoring": [
            "History/PE every 3–6 months x3 years, every 6–12 months x2 years, then annually",
            "Annual mammography",
            "DEXA scan if on aromatase inhibitor",
            "No routine blood tests or imaging unless symptoms (per ASCO guidelines)",
        ],
        "follow_up": "Oncology every 3–6 months; survivorship plan at 5 years",
        "evidence_grade": "Class I, Level A — ASCO/NCCN Breast Cancer Guidelines 2024",
    },
    # ── HEMATOLOGY ────────────────────────────────────────────────────────────
    "iron_deficiency_anemia": {
        "full_name": "Iron Deficiency Anemia",
        "department": "Hematology / General Medicine",
        "emergency": False,
        "first_line": [
            "Identify and treat underlying cause (bleeding, malabsorption, dietary insufficiency)",
            "Oral iron: Ferrous sulfate 325 mg TID between meals (take with Vitamin C to enhance absorption)",
            "Alternative if GI intolerance: Ferrous gluconate 240 mg TID or ferric carboxymaltose",
            "Duration: Continue 3–6 months AFTER Hgb normalizes to replete iron stores",
        ],
        "second_line": [
            "IV iron if: oral intolerance, malabsorption (IBD, post-bariatric), Hgb <7 g/dL with symptoms, or need for rapid repletion",
            "IV options: Ferric carboxymaltose 1000 mg over 15 min OR Ferumoxytol 510 mg IV",
            "Red cell transfusion if Hgb <7 g/dL with hemodynamic compromise or cardiac symptoms",
        ],
        "monitoring": [
            "CBC at 4 weeks (expect Hgb rise 1–2 g/dL/month with oral iron)",
            "Ferritin at 3 months (target >50 ng/mL to ensure stores replete)",
            "Reticulocyte count at 2 weeks (early response marker)",
            "GI workup (endoscopy) in men and post-menopausal women with iron deficiency",
        ],
        "follow_up": "Hematology/primary care at 4 weeks; source investigation GI if cause unclear",
        "evidence_grade": "Class I, Level A — BCSH Guidelines 2017; WHO IDA Guidelines",
    },
    "dvt_treatment": {
        "full_name": "Deep Vein Thrombosis (DVT)",
        "department": "Hematology / Vascular",
        "emergency": False,
        "first_line": [
            "DOAC (preferred): Rivaroxaban 15 mg BID x21 days, then 20 mg daily; OR Apixaban 10 mg BID x7 days then 5 mg BID",
            "Duration: Provoked (reversible trigger) — 3 months; Unprovoked — minimum 3 months, consider extended",
            "Below-knee DVT: 3 months if symptomatic; consider surveillance if asymptomatic",
        ],
        "second_line": [
            "LMWH bridge + Warfarin (target INR 2.0–3.0) if DOAC contraindicated",
            "LMWH alone for cancer-associated DVT (preferred) or use DOACs (Rivaroxaban, Apixaban — CARAVAGGIO trial)",
            "IVC filter only if anticoagulation absolutely contraindicated",
        ],
        "monitoring": [
            "Lower extremity compression ultrasound at 3 months to establish new baseline",
            "Renal function within 1 week (DOAC dose adjustment if eGFR changes)",
            "Thrombophilia workup at 3 months if unprovoked: Factor V Leiden, Prothrombin mutation, Antiphospholipid antibodies",
            "INR weekly then monthly if on Warfarin",
        ],
        "follow_up": "Hematology at 3 months; anticoagulation decision at that visit",
        "evidence_grade": "Class I, Level A — CHEST AT Guidelines 2021",
    },
    # ── PSYCHIATRY ────────────────────────────────────────────────────────────
    "major_depressive_disorder": {
        "full_name": "Major Depressive Disorder (MDD)",
        "department": "Psychology / Psychiatry",
        "emergency": False,
        "first_line": [
            "SSRI (first-line pharmacotherapy): Sertraline 50 mg daily (titrate to 200 mg) OR Escitalopram 10 mg daily (titrate to 20 mg)",
            "Psychotherapy: Cognitive Behavioral Therapy (CBT) — equally effective as medication for mild-moderate; combined therapy best for severe",
            "Response assessment at 4–6 weeks; adequate trial = 6–8 weeks at therapeutic dose",
            "Switch SSRI if no response at 6 weeks; augment if partial response",
        ],
        "second_line": [
            "SNRI: Venlafaxine XR 75 mg daily (titrate to 150–225 mg); effective for anxiety comorbidity",
            "Bupropion 150 mg daily (augmentation or 1st line if sexual dysfunction concern; avoid in seizure/eating disorder history)",
            "Augmentation: Lithium, Aripiprazole 2–15 mg, or Quetiapine XR 50–150 mg",
            "TMS (Transcranial Magnetic Stimulation) for treatment-resistant MDD",
            "ECT for severe, psychotic, or refractory MDD with imminent risk",
        ],
        "monitoring": [
            "PHQ-9 at baseline and every 4 weeks (target score <5)",
            "Suicide risk assessment at every visit (Columbia-Suicide Severity Rating Scale)",
            "Screen for bipolar disorder before initiating antidepressant (avoid inducing mania)",
            "SSRIs: monitor for activation/insomnia in first 2 weeks; QTc if high doses (escitalopram, citalopram)",
        ],
        "follow_up": "Psychiatry/psychology every 2–4 weeks until stable; then monthly for 6 months",
        "evidence_grade": "Class I, Level A — APA Practice Guidelines for MDD 2022",
    },
    # ── RHEUMATOLOGY ─────────────────────────────────────────────────────────
    "rheumatoid_arthritis": {
        "full_name": "Rheumatoid Arthritis",
        "department": "Rheumatology",
        "emergency": False,
        "first_line": [
            "Methotrexate 10 mg weekly PO/SC (titrate to 20–25 mg weekly) — anchor DMARD",
            "Folic acid 1 mg daily (reduce MTX toxicity)",
            "Bridge with low-dose prednisone 5–10 mg daily (taper as DMARD takes effect — 3–6 months)",
            "NSAIDs for symptom relief (short-term; GI protection with PPI if needed)",
            "DAS28 target remission (<2.6) or low disease activity (<3.2)",
        ],
        "second_line": [
            "Combination DMARDs: Add Hydroxychloroquine 200 mg BID and/or Sulfasalazine 1 g BID",
            "Biologic DMARD if inadequate response to MTX x3 months:",
            "  TNF inhibitor: Etanercept 50 mg SC weekly, Adalimumab 40 mg SC q2 weeks",
            "  JAK inhibitor: Baricitinib 4 mg daily or Upadacitinib 15 mg daily (if TNFi failed or contraindicated)",
            "  IL-6 inhibitor: Tocilizumab 8 mg/kg IV monthly",
        ],
        "monitoring": [
            "CBC, LFTs, creatinine every 4–8 weeks for first 6 months of MTX, then every 3 months",
            "CXR at baseline (MTX pulmonary toxicity)",
            "TB screening before biologic initiation (IGRA test)",
            "DAS28 at every visit; aim for treat-to-target strategy",
            "Annual: hepatitis B and C serology, lipid panel",
        ],
        "follow_up": "Rheumatology every 4–8 weeks until at target; then every 3–6 months",
        "evidence_grade": "Class I, Level A — ACR RA Guidelines 2021",
    },
    # ── GASTROENTEROLOGY ──────────────────────────────────────────────────────
    "gerd": {
        "full_name": "Gastroesophageal Reflux Disease (GERD)",
        "department": "Gastroenterology",
        "emergency": False,
        "first_line": [
            "Lifestyle: Elevate HOB, avoid meals 2–3h before bed, weight loss, avoid triggers (fatty foods, alcohol, caffeine, chocolate, mint)",
            "PPI (8-week healing course): Omeprazole 20 mg or Esomeprazole 40 mg 30–60 min before meal",
            "Step-down to lowest effective dose after 8 weeks",
            "H2 blocker (if PPI not tolerated): Famotidine 20 mg BID",
        ],
        "second_line": [
            "PPI twice daily for refractory symptoms (30 min before breakfast AND dinner)",
            "Baclofen 5–10 mg TID (reduces transient LES relaxations) for atypical GERD/laryngopharyngeal reflux",
            "Anti-reflux surgery (Nissen fundoplication) for medication-dependent young patients",
            "Upper endoscopy if: >5 years of symptoms, dysphagia, weight loss, anemia (screen for Barrett's)",
        ],
        "monitoring": [
            "Endoscopy for Barrett's esophagus (if alarm symptoms or prolonged GERD)",
            "Barrett's surveillance: endoscopy every 3–5 years (no dysplasia), 6 months (low-grade dysplasia)",
            "DXA scan if long-term PPI use (bone density — PPI increases fracture risk)",
        ],
        "follow_up": "Reassess at 8 weeks; GI referral if refractory or alarm features",
        "evidence_grade": "Class I, Level A — ACG GERD Guidelines 2022",
    },
    # ── ORTHOPEDICS ──────────────────────────────────────────────────────────
    "osteoarthritis_knee": {
        "full_name": "Osteoarthritis — Knee",
        "department": "Orthopedics / Rheumatology",
        "emergency": False,
        "first_line": [
            "Lifestyle: Weight loss (every 1 kg weight lost = 4 kg reduction in knee load), low-impact exercise (cycling, swimming)",
            "Physical therapy: quadriceps strengthening, proprioception training, patellar taping",
            "Topical NSAIDs (first-line for local pain, less GI risk): Diclofenac gel 1% QID",
            "Oral NSAIDs if topical insufficient (short-term): Naproxen 500 mg BID with PPI",
            "Acetaminophen 1 g TID for mild-moderate pain (limited evidence but low risk)",
        ],
        "second_line": [
            "Intra-articular corticosteroid injections (symptom relief 4–8 weeks): Methylprednisolone 40 mg + lidocaine",
            "Duloxetine 30–60 mg daily (central sensitization component)",
            "Knee replacement (TKA) if failed conservative therapy x6 months: 90–95% excellent outcomes at 10 years",
        ],
        "monitoring": [
            "Functional assessment (WOMAC, KOOS score) every 6 months",
            "Weight and BMI at every visit",
            "Annual X-ray to assess joint space progression",
            "Renal function if chronic NSAID use",
        ],
        "follow_up": "Orthopedics every 6 months; PT 6–8 weeks program",
        "evidence_grade": "Class I, Level A — OARSI Guidelines 2019; ACR OA Guidelines 2020",
    },
    # ── NEPHROLOGY (ACUTE) ────────────────────────────────────────────────────
    "hyperkalemia": {
        "full_name": "Hyperkalemia (K+ >5.5 mEq/L)",
        "department": "Nephrology",
        "emergency": True,
        "first_line": [
            "K+ >6.5 or ECG changes (peaked T, QRS widening, sine wave): IMMEDIATE treatment",
            "1. Membrane stabilization: Calcium gluconate 1–2 g IV over 10 min (onset 1–3 min, duration 30–60 min)",
            "2. Shift K+ intracellular: Insulin 10 units + Dextrose 50% 50 mL IV (onset 15 min, lowers K+ 0.5–1.5 mEq/L)",
            "3. Albuterol nebulized 10–20 mg (additive to insulin — lowers K+ 0.5–1.0 mEq/L)",
            "4. Sodium bicarbonate 50 mEq IV if metabolic acidosis (pH <7.2)",
            "5. Remove K+: Kayexalate (sodium polystyrene) 30 g PO/enema OR Patiromer 8.4 g daily PO (preferred)",
            "6. Dialysis if K+ life-threatening and above fail or renal failure",
        ],
        "second_line": [
            "Stop/reduce offending drugs: ACEi/ARB, NSAIDs, trimethoprim, spironolactone, beta-blockers",
            "Low-potassium diet counseling (<2 g/day)",
            "Patiromer 8.4 g daily for chronic hyperkalemia in CKD",
        ],
        "monitoring": [
            "Continuous cardiac monitoring (ECG changes guide urgency)",
            "Serum K+ every 1–2h during acute management",
            "BMP + ABG (acidosis worsens hyperkalemia)",
            "After stabilization: K+ every 6–12h x24h",
        ],
        "follow_up": "Nephrology urgent review; medication adjustment within 24–48h",
        "evidence_grade": "Class I, Level A — KDIGO and AHA Hyperkalemia Management 2020",
    },
    # ── UROLOGY ──────────────────────────────────────────────────────────────
    "kidney_stones": {
        "full_name": "Urolithiasis (Kidney Stones)",
        "department": "Urology",
        "emergency": False,
        "first_line": [
            "Analgesia: NSAIDs preferred (Ketorolac 30 mg IV or Ibuprofen 400–600 mg PO) — superior to opioids for stone pain",
            "Medical expulsive therapy (stones ≤10 mm): Tamsulosin 0.4 mg daily (alpha-blocker increases stone passage rates 29%)",
            "Hydration: increase fluid intake to maintain urine output >2.5 L/day",
            "Stones ≤5 mm: 80–90% pass spontaneously within 4 weeks — watchful waiting",
        ],
        "second_line": [
            "Stones 5–10 mm: ESWL (extracorporeal shock wave lithotripsy) — 80% stone-free rate for renal stones",
            "Stones >10 mm or failure of medical therapy: Ureteroscopy with laser lithotripsy",
            "Stones >20 mm in kidney: Percutaneous nephrolithotomy (PCNL)",
            "Stone prevention (type-specific): Calcium oxalate — increase fluid, restrict Na+/protein; Uric acid — allopurinol, alkalinize urine (potassium citrate); Cystine — D-penicillamine",
        ],
        "monitoring": [
            "KUB or CT renal stone at 4 weeks (assess stone passage)",
            "24h urine metabolic profile (calcium, oxalate, uric acid, citrate) for stone prevention",
            "Serum uric acid, calcium, PTH if recurrent stones",
        ],
        "follow_up": "Urology at 4 weeks; stone composition analysis if retrieved",
        "evidence_grade": "Class I, Level A — EAU Urolithiasis Guidelines 2023",
    },
}


def generate_treatment_plan(
    diagnosis: str,
    severity: str,
    patient_id: str,
    contraindications: Optional[list[str]] = None,
) -> dict:
    """Generates an evidence-based treatment protocol for a confirmed or working diagnosis.

    Returns structured first-line and second-line therapies, monitoring parameters,
    follow-up schedule, and evidence grading — all adapted to the patient's profile.

    Args:
        diagnosis: Diagnosis keyword (e.g., 'stemi', 'copd_exacerbation', 'type2_diabetes',
                   'atrial_fibrillation', 'ischemic_stroke', 'iron_deficiency_anemia',
                   'heart_failure_hfref', 'sepsis', 'epilepsy', 'ckd_management',
                   'hypothyroidism', 'rheumatoid_arthritis', 'gerd', 'hyperkalemia',
                   'pulmonary_embolism', 'dvt_treatment', 'breast_cancer_early',
                   'major_depressive_disorder', 'hypertension', 'osteoarthritis_knee',
                   'community_acquired_pneumonia', 'kidney_stones').
        severity: Clinical severity — 'mild', 'moderate', 'severe', or 'critical'.
        patient_id: Patient identifier for allergy and comorbidity cross-check.
        contraindications: Optional list of medications or procedures to avoid.

    Returns:
        dict: Complete treatment protocol with first-line, second-line, monitoring,
              follow-up, evidence grade, and patient-specific safety flags.
    """
    # Normalize diagnosis key
    diag_key = diagnosis.lower().strip().replace(" ", "_").replace("-", "_")

    # Try exact match first, then partial
    protocol = _TREATMENT_PROTOCOLS.get(diag_key)
    if not protocol:
        for key, val in _TREATMENT_PROTOCOLS.items():
            if diag_key in key or key in diag_key or diag_key in val.get("full_name", "").lower():
                protocol = val
                diag_key = key
                break

    if not protocol:
        available = ", ".join(_TREATMENT_PROTOCOLS.keys())
        return {
            "status": "not_found",
            "message": (
                f"No treatment protocol found for '{diagnosis}'. "
                f"Available diagnoses: {available}. "
                "For unlisted conditions, use web_search to retrieve current clinical guidelines."
            ),
        }

    # Load patient profile for safety cross-check
    patient = _PATIENT_DB.get(patient_id, {})
    patient_allergies = [a.lower() for a in patient.get("allergies", [])]
    patient_meds = [m.lower() for m in patient.get("current_medications", [])]
    patient_conditions = [c.lower() for c in patient.get("chronic_conditions", [])]
    patient_age = patient.get("age", 0)

    # Safety flags — check protocol steps against patient allergies + contraindications
    all_contraindications = list(contraindications or [])
    safety_flags = []

    combined_restrictions = [c.lower() for c in all_contraindications] + patient_allergies

    flagged_steps = []
    for step in protocol["first_line"]:
        for restriction in combined_restrictions:
            if restriction.split()[0] in step.lower():
                flagged_steps.append({
                    "step": step,
                    "flag": f"Patient allergy or contraindication: '{restriction}' — review before prescribing",
                    "severity": "WARNING",
                })

    # Age-specific flags
    if patient_age >= 65:
        safety_flags.append("Elderly patient (≥65): use lowest effective doses; monitor for drug accumulation")
    if patient_age < 18:
        safety_flags.append("Pediatric patient: verify all doses against weight-based pediatric references")

    # Severity-specific escalation note
    severity_note = {
        "mild":     "Mild severity: initiate outpatient management; reassess in 4–6 weeks",
        "moderate": "Moderate severity: close monitoring; consider short inpatient observation",
        "severe":   "Severe: inpatient admission warranted; expedite specialist review",
        "critical": "CRITICAL: ICU-level care; activate emergency protocols; immediate specialist involvement",
    }.get(severity.lower(), "Severity not specified: use clinical judgment")

    patient_name = patient.get("name", patient_id)

    return {
        "status": "generated",
        "diagnosis": protocol["full_name"],
        "matched_key": diag_key,
        "department": protocol["department"],
        "is_emergency": protocol.get("emergency", False),
        "severity": severity,
        "severity_note": severity_note,
        "patient_name": patient_name,
        "patient_id": patient_id,
        "treatment_protocol": {
            "first_line": protocol["first_line"],
            "second_line": protocol["second_line"],
        },
        "monitoring_parameters": protocol["monitoring"],
        "follow_up": protocol["follow_up"],
        "evidence_grade": protocol["evidence_grade"],
        "patient_safety": {
            "flagged_steps": flagged_steps,
            "general_safety_flags": safety_flags,
            "patient_allergies": patient.get("allergies", []),
            "current_medications": patient.get("current_medications", []),
        },
        "disclaimer": (
            "Protocol generated from evidence-based guidelines. "
            "Always individualize to patient comorbidities, renal/hepatic function, and preferences. "
            "Confirm with clinical pharmacist for drug-specific dosing."
        ),
    }


# =============================================================================
# DIAGNOSTIC ORDERING SYSTEM (Sprint 4)
# =============================================================================

# Investigation order states
_INVESTIGATION_ORDERS: dict[str, list[dict]] = {}  # patient_id → list of orders

# Investigation types and typical turnaround times
_INVESTIGATION_TYPES = {
    "blood_panel": {"name": "Blood Panel (CBC, BMP)", "turnaround_hours": 2},
    "lipid_panel": {"name": "Lipid Panel", "turnaround_hours": 4},
    "liver_function": {"name": "LFTs", "turnaround_hours": 4},
    "renal_function": {"name": "Renal Function", "turnaround_hours": 3},
    "cardiac_enzymes": {"name": "Cardiac Enzymes (Troponin, CK-MB)", "turnaround_hours": 1},
    "coagulation": {"name": "Coagulation Panel (PT/INR, APTT)", "turnaround_hours": 2},
    "inflammation": {"name": "Inflammatory Markers (CRP, ESR)", "turnaround_hours": 6},
    "thyroid": {"name": "Thyroid Function (TSH, Free T4)", "turnaround_hours": 24},
    "hba1c": {"name": "HbA1c", "turnaround_hours": 24},
    "blood_culture": {"name": "Blood Culture", "turnaround_hours": 48},
    "urineCulture": {"name": "Urine Culture", "turnaround_hours": 48},
    "chest_xray": {"name": "Chest X-Ray", "turnaround_hours": 2},
    "ct_chest": {"name": "CT Chest", "turnaround_hours": 6},
    "ct_abdomen": {"name": "CT Abdomen/Pelvis", "turnaround_hours": 8},
    "ct_head": {"name": "CT Head", "turnaround_hours": 2},
    "mri_brain": {"name": "MRI Brain", "turnaround_hours": 24},
    "mri_spine": {"name": "MRI Spine", "turnaround_hours": 24},
    "ecg": {"name": "12-Lead ECG", "turnaround_hours": 0.5},
    "echocardiogram": {"name": "Echocardiogram", "turnaround_hours": 24},
    "ultrasound_abdomen": {"name": "Abdominal Ultrasound", "turnaround_hours": 4},
    "doppler": {"name": "Doppler Ultrasound", "turnaround_hours": 6},
}

_INVESTIGATION_SEQ: dict[str, int] = {"n": 0}


def order_investigation(
    patient_id: str,
    investigation_type: str,
    clinical_indication: str,
    urgency: str = "routine",
    ordered_by: str = "",
) -> dict:
    """Places an investigation order with status tracking.

    Creates an investigation order with states: ordered → processing → resulted → reviewed.

    Args:
        patient_id: Patient identifier (e.g., "P001").
        investigation_type: Type of investigation. Available types:
            • blood_panel, lipid_panel, liver_function, renal_function
            • cardiac_enzymes, coagulation, inflammation, thyroid, hba1c
            • blood_culture, urine_culture
            • chest_xray, ct_chest, ct_abdomen, ct_head
            • mri_brain, mri_spine
            • ecg, echocardiogram, ultrasound_abdomen, doppler
        clinical_indication: Clinical reason for the investigation.
        urgency: "routine", "urgent", or "emergency".
        ordered_by: ID of the ordering clinician.

    Returns:
        dict: Order confirmation with order ID and status.
    """
    inv_type = _INVESTIGATION_TYPES.get(investigation_type.lower().replace(" ", "_"))
    if not inv_type:
        return {
            "status": "invalid_type",
            "message": f"Unknown investigation type: {investigation_type}. Available: {', '.join(_INVESTIGATION_TYPES.keys())}",
        }

    _INVESTIGATION_SEQ["n"] += 1
    now = datetime.datetime.now()
    order_id = f"INV-{now.strftime('%Y%m%d')}-{_INVESTIGATION_SEQ['n']:04d}"

    urgency_priority = {"emergency": 1, "urgent": 2, "routine": 3}

    order = {
        "order_id": order_id,
        "patient_id": patient_id,
        "investigation_type": investigation_type,
        "investigation_name": inv_type["name"],
        "clinical_indication": clinical_indication,
        "urgency": urgency,
        "priority": urgency_priority.get(urgency, 3),
        "ordered_by": ordered_by or "System",
        "ordered_at": now.strftime("%Y-%m-%d %H:%M"),
        "status": "ordered",
        "estimated_turnaround_hours": inv_type["turnaround_hours"],
    }

    _INVESTIGATION_ORDERS.setdefault(patient_id, []).append(order)

    return {
        "status": "ordered",
        "order_id": order_id,
        "patient_id": patient_id,
        "investigation": inv_type["name"],
        "urgency": urgency,
        "estimated_turnaround": f"{inv_type['turnaround_hours']} hours",
        "message": f"Order placed for {inv_type['name']} (ID: {order_id})",
    }


def get_pending_results(
    patient_id: str,
    status_filter: str = "all",
) -> dict:
    """Returns all ordered investigations with current status.

    Shows the full order lifecycle: ordered → processing → resulted → reviewed.

    Args:
        patient_id: Patient identifier.
        status_filter: Filter by status - "all", "pending", "resulted".

    Returns:
        dict: List of investigations with their current status.
    """
    if patient_id not in _INVESTIGATION_ORDERS:
        return {
            "status": "no_orders",
            "patient_id": patient_id,
            "message": "No investigation orders on record for this patient.",
            "orders": [],
        }

    orders = _INVESTIGATION_ORDERS[patient_id]

    if status_filter == "pending":
        orders = [o for o in orders if o["status"] in ("ordered", "processing")]
    elif status_filter == "resulted":
        orders = [o for o in orders if o["status"] == "resulted"]

    # Sort by priority (emergency first), then by time
    orders = sorted(orders, key=lambda x: (x["priority"], x["ordered_at"]))

    pending_count = sum(1 for o in orders if o["status"] in ("ordered", "processing"))
    resulted_count = sum(1 for o in orders if o["status"] == "resulted")
    reviewed_count = sum(1 for o in orders if o["status"] == "reviewed")

    return {
        "status": "success",
        "patient_id": patient_id,
        "total_orders": len(orders),
        "pending": pending_count,
        "resulted": resulted_count,
        "reviewed": reviewed_count,
        "orders": orders,
    }


def acknowledge_critical_result(
    patient_id: str,
    investigation_id: str,
    clinician_id: str,
    notes: str = "",
) -> dict:
    """Records that the ordering clinician has acknowledged a critical result.

    This closes the critical value notification loop required for patient safety.

    Args:
        patient_id: Patient identifier.
        investigation_id: The order ID to acknowledge.
        clinician_id: ID of the clinician acknowledging.
        notes: Optional clinical notes about the result.

    Returns:
        dict: Acknowledgment confirmation.
    """
    if patient_id not in _INVESTIGATION_ORDERS:
        return {
            "status": "not_found",
            "message": f"No investigation orders found for patient {patient_id}",
        }

    order = None
    for o in _INVESTIGATION_ORDERS[patient_id]:
        if o["order_id"] == investigation_id:
            order = o
            break

    if not order:
        return {
            "status": "not_found",
            "message": f"Order {investigation_id} not found for patient {patient_id}",
        }

    if order["status"] != "resulted":
        return {
            "status": "not_resulted",
            "message": f"Order {investigation_id} has not been resulted yet. Current status: {order['status']}",
        }

    order["status"] = "reviewed"
    order["acknowledged_by"] = clinician_id
    order["acknowledged_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    order["acknowledgment_notes"] = notes

    return {
        "status": "acknowledged",
        "order_id": investigation_id,
        "patient_id": patient_id,
        "investigation": order["investigation_name"],
        "acknowledged_by": clinician_id,
        "acknowledged_at": order["acknowledged_at"],
        "message": f"Critical result for {investigation_id} acknowledged by {clinician_id}",
    }


# Mock function to simulate results being available (for testing)
def mock_result_investigation(order_id: str, patient_id: str, result_data: dict = None) -> dict:
    """Simulates a lab/radiology result being available (for demo purposes)."""
    if patient_id not in _INVESTIGATION_ORDERS:
        return {"status": "not_found"}

    for order in _INVESTIGATION_ORDERS[patient_id]:
        if order["order_id"] == order_id:
            order["status"] = "resulted"
            order["resulted_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            order["result_data"] = result_data or {"result": "Normal", "notes": "No significant abnormalities"}
            return {"status": "resulted", "order": order}

    return {"status": "not_found"}

