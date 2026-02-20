"""Psychology-specific screening and assessment tools."""


def phq9_depression_screening(answers: list[int]) -> dict:
    """Scores the PHQ-9 depression screening questionnaire.

    Args:
        answers: List of 9 scores (0-3 each) for PHQ-9 questions.
            Q1: Little interest or pleasure in doing things
            Q2: Feeling down, depressed, or hopeless
            Q3: Trouble falling/staying asleep, or sleeping too much
            Q4: Feeling tired or having little energy
            Q5: Poor appetite or overeating
            Q6: Feeling bad about yourself or that you are a failure
            Q7: Trouble concentrating on things
            Q8: Moving or speaking slowly / being fidgety or restless
            Q9: Thoughts that you would be better off dead or of hurting yourself
            Scoring: 0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day

    Returns:
        dict: PHQ-9 score with severity classification and recommendations.
    """
    if len(answers) != 9:
        return {"status": "error", "message": f"PHQ-9 requires exactly 9 answers, got {len(answers)}"}

    for i, a in enumerate(answers):
        if not 0 <= a <= 3:
            return {"status": "error", "message": f"Answer {i+1} must be 0-3, got {a}"}

    total_score = sum(answers)

    # Severity classification
    if total_score <= 4:
        severity = "MINIMAL"
        action = "Monitor, re-screen if clinical concern persists"
    elif total_score <= 9:
        severity = "MILD"
        action = "Watchful waiting, repeat PHQ-9 at follow-up. Consider counseling."
    elif total_score <= 14:
        severity = "MODERATE"
        action = "Treatment plan recommended: psychotherapy (CBT) and/or medication"
    elif total_score <= 19:
        severity = "MODERATELY SEVERE"
        action = "Active treatment with medication and/or psychotherapy strongly recommended"
    else:
        severity = "SEVERE"
        action = "Immediate treatment initiation. Assess for safety. Consider psychiatric referral."

    # Safety check - Q9 (suicidal ideation)
    safety_concern = answers[8] > 0
    safety_note = None
    if answers[8] >= 2:
        safety_note = "CRITICAL: Patient endorses frequent suicidal thoughts. Immediate safety assessment required. Crisis line: 988."
    elif answers[8] == 1:
        safety_note = "CAUTION: Patient reports some suicidal ideation. Conduct thorough safety assessment."

    return {
        "status": "scored",
        "total_score": total_score,
        "severity": severity,
        "recommended_action": action,
        "safety_concern": safety_concern,
        "safety_note": safety_note,
        "question_breakdown": {
            "anhedonia": answers[0],
            "depressed_mood": answers[1],
            "sleep_disturbance": answers[2],
            "fatigue": answers[3],
            "appetite_changes": answers[4],
            "guilt_worthlessness": answers[5],
            "concentration_difficulty": answers[6],
            "psychomotor_changes": answers[7],
            "suicidal_ideation": answers[8],
        },
    }


def gad7_anxiety_screening(answers: list[int]) -> dict:
    """Scores the GAD-7 generalized anxiety disorder screening questionnaire.

    Args:
        answers: List of 7 scores (0-3 each) for GAD-7 questions.
            Q1: Feeling nervous, anxious, or on edge
            Q2: Not being able to stop or control worrying
            Q3: Worrying too much about different things
            Q4: Trouble relaxing
            Q5: Being so restless that it's hard to sit still
            Q6: Becoming easily annoyed or irritable
            Q7: Feeling afraid as if something awful might happen
            Scoring: 0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day

    Returns:
        dict: GAD-7 score with severity classification and recommendations.
    """
    if len(answers) != 7:
        return {"status": "error", "message": f"GAD-7 requires exactly 7 answers, got {len(answers)}"}

    for i, a in enumerate(answers):
        if not 0 <= a <= 3:
            return {"status": "error", "message": f"Answer {i+1} must be 0-3, got {a}"}

    total_score = sum(answers)

    if total_score <= 4:
        severity = "MINIMAL"
        action = "Monitor symptoms, no treatment needed at this time"
    elif total_score <= 9:
        severity = "MILD"
        action = "Watchful waiting, self-help strategies, consider counseling"
    elif total_score <= 14:
        severity = "MODERATE"
        action = "Consider psychotherapy (CBT) and/or pharmacotherapy"
    else:
        severity = "SEVERE"
        action = "Active treatment recommended: CBT + consider SSRI/SNRI medication. Psychiatric referral if needed."

    return {
        "status": "scored",
        "total_score": total_score,
        "severity": severity,
        "recommended_action": action,
        "question_breakdown": {
            "nervous_anxious": answers[0],
            "uncontrollable_worry": answers[1],
            "excessive_worry": answers[2],
            "trouble_relaxing": answers[3],
            "restlessness": answers[4],
            "irritability": answers[5],
            "feeling_afraid": answers[6],
        },
        "treatment_options": {
            "psychotherapy": "CBT is first-line treatment for anxiety disorders",
            "medication": "SSRIs (sertraline, escitalopram) or SNRIs (venlafaxine, duloxetine)" if total_score >= 10 else "Not indicated at current severity",
            "self_help": "Regular exercise, sleep hygiene, mindfulness/meditation, limiting caffeine",
        },
    }


def crisis_assessment(
    suicidal_ideation: bool,
    has_plan: bool,
    has_means: bool,
    previous_attempts: int,
    substance_use: bool,
    social_support: str,
    recent_loss: bool,
) -> dict:
    """Performs mental health crisis risk assessment.

    Args:
        suicidal_ideation: Whether patient is having thoughts of suicide.
        has_plan: Whether patient has a specific plan.
        has_means: Whether patient has access to means.
        previous_attempts: Number of previous suicide attempts.
        substance_use: Whether patient is currently using substances.
        social_support: Level of social support ('strong', 'moderate', 'weak', 'none').
        recent_loss: Whether patient has experienced a recent significant loss.

    Returns:
        dict: Crisis risk level with immediate actions and safety planning.
    """
    risk_score = 0
    risk_factors = []
    protective_factors = []

    if suicidal_ideation:
        risk_score += 3
        risk_factors.append("Active suicidal ideation")
    if has_plan:
        risk_score += 4
        risk_factors.append("Has a specific plan")
    if has_means:
        risk_score += 4
        risk_factors.append("Has access to means")
    if previous_attempts > 0:
        risk_score += 3
        risk_factors.append(f"History of {previous_attempts} previous attempt(s)")
    if substance_use:
        risk_score += 2
        risk_factors.append("Current substance use (impairs judgment)")
    if recent_loss:
        risk_score += 2
        risk_factors.append("Recent significant loss")

    if social_support.lower() == "strong":
        protective_factors.append("Strong social support network")
        risk_score -= 1
    elif social_support.lower() == "none":
        risk_factors.append("No social support")
        risk_score += 2

    # Risk determination
    if risk_score >= 10:
        risk_level = "IMMINENT"
        action = "EMERGENCY: Do not leave patient alone. Call 911 or go to nearest ER. Inpatient psychiatric admission recommended."
    elif risk_score >= 6:
        risk_level = "HIGH"
        action = "URGENT: Same-day psychiatric evaluation. Safety planning. Consider crisis stabilization unit."
    elif risk_score >= 3:
        risk_level = "MODERATE"
        action = "Develop safety plan. Schedule follow-up within 48 hours. Provide crisis resources."
    else:
        risk_level = "LOW"
        action = "Continue monitoring. Provide crisis resources. Schedule routine follow-up."

    safety_plan = [
        "Identify warning signs and triggers",
        "List internal coping strategies (breathing exercises, distraction)",
        "Identify people to contact for support",
        "Remove or restrict access to lethal means",
        "Crisis contacts: 988 Suicide & Crisis Lifeline, Crisis Text Line (text HOME to 741741)",
        "Emergency: 911 or nearest emergency room",
    ]

    return {
        "status": "assessed",
        "risk_level": risk_level,
        "risk_score": risk_score,
        "immediate_action": action,
        "risk_factors": risk_factors,
        "protective_factors": protective_factors,
        "safety_plan_components": safety_plan,
        "crisis_resources": {
            "988_lifeline": "Call or text 988",
            "crisis_text_line": "Text HOME to 741741",
            "emergency": "911",
            "veterans_crisis": "988 then press 1",
        },
    }
