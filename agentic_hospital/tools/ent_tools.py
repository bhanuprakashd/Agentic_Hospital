"""ENT (Ear, Nose, Throat) specific diagnostic and assessment tools."""


def hearing_assessment(
    right_ear_db: list[int],
    left_ear_db: list[int],
    frequencies_hz: list[int],
    tympanometry: str,
    speech_recognition_pct: int,
) -> dict:
    """Interprets audiometry results and assesses hearing loss.

    Args:
        right_ear_db: Hearing thresholds for right ear in dB at each frequency.
        left_ear_db: Hearing thresholds for left ear in dB at each frequency.
        frequencies_hz: Frequencies tested in Hz (e.g., [250, 500, 1000, 2000, 4000, 8000]).
        tympanometry: Tympanometry result ('type_A', 'type_B', 'type_C', 'type_As', 'type_Ad').
        speech_recognition_pct: Speech recognition score percentage.

    Returns:
        dict: Hearing assessment with classification and recommendations.
    """
    def classify_hearing(avg_db):
        if avg_db <= 25: return "Normal"
        elif avg_db <= 40: return "Mild hearing loss"
        elif avg_db <= 55: return "Moderate hearing loss"
        elif avg_db <= 70: return "Moderately severe hearing loss"
        elif avg_db <= 90: return "Severe hearing loss"
        else: return "Profound hearing loss"

    right_avg = sum(right_ear_db) / len(right_ear_db) if right_ear_db else 0
    left_avg = sum(left_ear_db) / len(left_ear_db) if left_ear_db else 0

    right_class = classify_hearing(right_avg)
    left_class = classify_hearing(left_avg)

    # Tympanometry interpretation
    tympanometry_meaning = {
        "type_A": "Normal middle ear function",
        "type_B": "Flat - suggests middle ear effusion or TM perforation",
        "type_C": "Negative pressure - suggests Eustachian tube dysfunction",
        "type_As": "Shallow peak - suggests otosclerosis or tympanosclerosis",
        "type_Ad": "Deep peak - suggests ossicular discontinuity or flaccid TM",
    }

    # Pattern analysis
    pattern = "Unknown"
    if right_ear_db and left_ear_db:
        high_freq_r = right_ear_db[-2:] if len(right_ear_db) >= 2 else right_ear_db
        low_freq_r = right_ear_db[:2] if len(right_ear_db) >= 2 else right_ear_db
        if sum(high_freq_r) / len(high_freq_r) > sum(low_freq_r) / len(low_freq_r) + 15:
            pattern = "High-frequency hearing loss (noise-induced or presbycusis pattern)"
        elif abs(right_avg - left_avg) > 15:
            pattern = "Asymmetric hearing loss - further evaluation needed (consider MRI to rule out acoustic neuroma)"

    recommendations = []
    if right_avg > 40 or left_avg > 40:
        recommendations.append("Hearing aid evaluation recommended")
    if "type_B" in tympanometry:
        recommendations.append("ENT evaluation for middle ear pathology")
    if "Asymmetric" in pattern:
        recommendations.append("MRI internal auditory canals to rule out retrocochlear pathology")
    if speech_recognition_pct < 60:
        recommendations.append("Consider cochlear implant evaluation")
    if right_avg > 25 or left_avg > 25:
        recommendations.append("Annual audiometric monitoring")

    return {
        "status": "assessed",
        "right_ear": {
            "average_threshold_db": round(right_avg, 1),
            "classification": right_class,
        },
        "left_ear": {
            "average_threshold_db": round(left_avg, 1),
            "classification": left_class,
        },
        "tympanometry": tympanometry_meaning.get(tympanometry, "Unknown type"),
        "speech_recognition": f"{speech_recognition_pct}%",
        "pattern": pattern,
        "recommendations": recommendations,
    }


def sleep_apnea_screening(
    snoring: bool,
    witnessed_apneas: bool,
    daytime_sleepiness: int,
    bmi: float,
    neck_circumference_cm: float,
    hypertension: bool,
    age: int,
    gender: str,
) -> dict:
    """Screens for obstructive sleep apnea using STOP-BANG-like criteria.

    Args:
        snoring: Whether patient snores loudly.
        witnessed_apneas: Whether bed partner has witnessed breathing pauses.
        daytime_sleepiness: Epworth Sleepiness Scale score (0-24, >10 = excessive).
        bmi: Body Mass Index.
        neck_circumference_cm: Neck circumference in centimeters.
        hypertension: Whether patient has hypertension.
        age: Patient age in years.
        gender: Patient gender ('male' or 'female').

    Returns:
        dict: Sleep apnea risk screening with recommendations.
    """
    score = 0
    risk_factors = []

    if snoring:
        score += 1
        risk_factors.append("Loud snoring")
    if witnessed_apneas:
        score += 1
        risk_factors.append("Witnessed apneas")
    if daytime_sleepiness > 10:
        score += 1
        risk_factors.append(f"Excessive daytime sleepiness (ESS: {daytime_sleepiness})")
    if hypertension:
        score += 1
        risk_factors.append("Hypertension")
    if bmi > 35:
        score += 1
        risk_factors.append(f"Obesity (BMI: {bmi})")
    if age > 50:
        score += 1
        risk_factors.append(f"Age > 50 ({age})")
    if neck_circumference_cm > 40:
        score += 1
        risk_factors.append(f"Large neck circumference ({neck_circumference_cm} cm)")
    if gender.lower() == "male":
        score += 1
        risk_factors.append("Male gender")

    if score >= 5:
        risk = "HIGH"
        recommendation = "Polysomnography (sleep study) strongly recommended. High probability of moderate-to-severe OSA."
    elif score >= 3:
        risk = "INTERMEDIATE"
        recommendation = "Consider polysomnography or home sleep apnea test (HSAT)."
    else:
        risk = "LOW"
        recommendation = "Low risk for OSA. Monitor symptoms. Consider testing if symptoms worsen."

    return {
        "status": "screened",
        "stop_bang_score": score,
        "risk_level": risk,
        "risk_factors": risk_factors,
        "recommendation": recommendation,
        "next_steps": [
            "Polysomnography (gold standard)" if score >= 3 else "Monitor symptoms",
            "Weight management" if bmi > 25 else None,
            "Avoid alcohol and sedatives before sleep",
            "Sleep position therapy (avoid supine sleeping)",
        ],
    }
