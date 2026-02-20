"""Gastroenterology-specific diagnostic and assessment tools."""


def liver_function_assessment(
    alt: float,
    ast: float,
    alp: float,
    total_bilirubin: float,
    direct_bilirubin: float,
    albumin: float,
    inr: float,
    platelet_count: int,
) -> dict:
    """Interprets liver function tests and assesses liver disease severity.

    Args:
        alt: ALT (Alanine Aminotransferase) in U/L (normal: 7-56).
        ast: AST (Aspartate Aminotransferase) in U/L (normal: 10-40).
        alp: ALP (Alkaline Phosphatase) in U/L (normal: 44-147).
        total_bilirubin: Total bilirubin in mg/dL (normal: 0.1-1.2).
        direct_bilirubin: Direct bilirubin in mg/dL (normal: 0-0.3).
        albumin: Albumin in g/dL (normal: 3.5-5.5).
        inr: International Normalized Ratio (normal: 0.8-1.1).
        platelet_count: Platelet count (× 10³/μL).

    Returns:
        dict: Liver function interpretation with pattern and recommendations.
    """
    findings = []
    pattern = "NORMAL"

    # ALT/AST analysis
    if alt > 56 or ast > 40:
        if alt > ast:
            findings.append("Hepatocellular pattern (ALT > AST) - suggests viral hepatitis, NAFLD, or drug-induced")
            pattern = "HEPATOCELLULAR"
        else:
            findings.append("AST > ALT pattern - suggests alcoholic liver disease or cirrhosis")
            pattern = "HEPATOCELLULAR"
        if alt > 1000 or ast > 1000:
            findings.append("MARKEDLY ELEVATED transaminases - consider acute viral hepatitis, ischemic hepatitis, or drug toxicity")

    # ALP analysis
    if alp > 147:
        if pattern == "HEPATOCELLULAR":
            pattern = "MIXED"
        else:
            pattern = "CHOLESTATIC"
        findings.append("Elevated ALP - cholestatic pattern. Consider biliary obstruction, PBC, or bone disease.")

    # Bilirubin
    if total_bilirubin > 1.2:
        findings.append(f"Elevated total bilirubin ({total_bilirubin} mg/dL)")
        if direct_bilirubin > 0.3:
            findings.append("Direct hyperbilirubinemia - suggests biliary obstruction or hepatocellular dysfunction")
        else:
            findings.append("Indirect hyperbilirubinemia - consider hemolysis or Gilbert syndrome")

    # Synthetic function
    if albumin < 3.5:
        findings.append(f"Low albumin ({albumin} g/dL) - indicates impaired synthetic function (chronic liver disease)")
    if inr > 1.5:
        findings.append(f"Elevated INR ({inr}) - impaired coagulation factor synthesis")

    # FIB-4 score (fibrosis estimate)
    if ast > 0 and platelet_count > 0 and alt > 0:
        import math
        fib4 = (42 * ast) / (platelet_count * math.sqrt(alt))  # Using age=42 as placeholder
        if fib4 > 3.25:
            findings.append(f"FIB-4 score {fib4:.2f} - HIGH probability of advanced fibrosis")
        elif fib4 > 1.45:
            findings.append(f"FIB-4 score {fib4:.2f} - INTERMEDIATE fibrosis risk, further evaluation needed")
        else:
            findings.append(f"FIB-4 score {fib4:.2f} - LOW probability of advanced fibrosis")

    # MELD-like severity (simplified)
    if total_bilirubin > 1.2 and inr > 1.5 and albumin < 3.5:
        severity = "SEVERE liver dysfunction"
    elif total_bilirubin > 1.2 or inr > 1.2 or albumin < 3.5:
        severity = "MODERATE liver dysfunction"
    elif alt > 56 or ast > 40:
        severity = "MILD liver enzyme elevation"
    else:
        severity = "Normal liver function"

    recommendations = []
    if pattern != "NORMAL":
        recommendations.append("Hepatitis panel (Hep A IgM, Hep B sAg/sAb/cAb, Hep C Ab)")
        recommendations.append("Right upper quadrant ultrasound")
    if pattern == "CHOLESTATIC":
        recommendations.append("MRCP or ERCP for biliary evaluation")
    if alt > 56 or ast > 40:
        recommendations.append("Review medications for hepatotoxicity")
        recommendations.append("Limit alcohol intake")
    if albumin < 3.5 or inr > 1.5:
        recommendations.append("Gastroenterology/Hepatology referral for chronic liver disease evaluation")

    return {
        "status": "interpreted",
        "pattern": pattern,
        "severity": severity,
        "findings": findings,
        "lab_values": {
            "ALT": f"{alt} U/L (normal: 7-56)",
            "AST": f"{ast} U/L (normal: 10-40)",
            "ALP": f"{alp} U/L (normal: 44-147)",
            "Total_Bilirubin": f"{total_bilirubin} mg/dL (normal: 0.1-1.2)",
            "Direct_Bilirubin": f"{direct_bilirubin} mg/dL (normal: 0-0.3)",
            "Albumin": f"{albumin} g/dL (normal: 3.5-5.5)",
            "INR": f"{inr} (normal: 0.8-1.1)",
        },
        "recommendations": recommendations,
    }


def ibs_symptom_scoring(
    abdominal_pain_frequency: int,
    pain_related_to_defecation: bool,
    stool_frequency_change: bool,
    stool_form_change: bool,
    bloating_severity: int,
    symptom_duration_months: int,
    predominant_pattern: str,
) -> dict:
    """Evaluates IBS symptoms using Rome IV criteria.

    Args:
        abdominal_pain_frequency: Days per month with abdominal pain (Rome IV requires >= 1/week).
        pain_related_to_defecation: Whether pain is related to defecation.
        stool_frequency_change: Whether there is a change in stool frequency.
        stool_form_change: Whether there is a change in stool form/appearance.
        bloating_severity: Bloating severity (0-10).
        symptom_duration_months: How many months symptoms have been present.
        predominant_pattern: Predominant bowel pattern ('IBS-C', 'IBS-D', 'IBS-M', 'IBS-U').

    Returns:
        dict: IBS assessment with Rome IV criteria evaluation and management plan.
    """
    rome_criteria_met = 0

    if pain_related_to_defecation:
        rome_criteria_met += 1
    if stool_frequency_change:
        rome_criteria_met += 1
    if stool_form_change:
        rome_criteria_met += 1

    meets_rome_iv = (
        abdominal_pain_frequency >= 4 and  # At least 1 day/week
        rome_criteria_met >= 2 and  # At least 2 of 3 criteria
        symptom_duration_months >= 6  # Symptoms for at least 6 months
    )

    # Severity assessment
    if abdominal_pain_frequency >= 20 or bloating_severity >= 8:
        severity = "SEVERE"
    elif abdominal_pain_frequency >= 8 or bloating_severity >= 5:
        severity = "MODERATE"
    else:
        severity = "MILD"

    # Management plan based on subtype
    management = {
        "dietary": ["Low FODMAP diet trial (with dietitian guidance)", "Regular meals, adequate hydration"],
        "lifestyle": ["Regular exercise", "Stress management techniques", "Adequate sleep"],
    }

    medications = []
    pattern = predominant_pattern.upper()
    if pattern == "IBS-C":
        medications = ["Fiber supplementation (psyllium)", "Osmotic laxatives (PEG)", "Linaclotide or Lubiprostone if refractory"]
    elif pattern == "IBS-D":
        medications = ["Loperamide for diarrhea episodes", "Rifaximin course", "Eluxadoline if refractory"]
    elif pattern == "IBS-M":
        medications = ["Symptom-directed treatment", "Peppermint oil capsules for cramping"]
    medications.append("Antispasmodics (dicyclomine, hyoscyamine) for pain")

    if severity in ["MODERATE", "SEVERE"]:
        medications.append("Consider low-dose tricyclic antidepressant (amitriptyline) for pain modulation")

    alarm_features = [
        "Check for alarm features: rectal bleeding, unintentional weight loss, family history of CRC/IBD, anemia, nocturnal symptoms",
        "If alarm features present: colonoscopy and further workup before IBS diagnosis",
    ]

    return {
        "status": "evaluated",
        "meets_rome_iv_criteria": meets_rome_iv,
        "ibs_subtype": predominant_pattern,
        "severity": severity,
        "rome_criteria_details": {
            "pain_frequency": f"{abdominal_pain_frequency} days/month (need >= 4)",
            "related_to_defecation": pain_related_to_defecation,
            "frequency_change": stool_frequency_change,
            "form_change": stool_form_change,
            "criteria_met": f"{rome_criteria_met}/3 (need >= 2)",
            "duration": f"{symptom_duration_months} months (need >= 6)",
        },
        "management_plan": management,
        "medications": medications,
        "alarm_features_check": alarm_features,
    }
