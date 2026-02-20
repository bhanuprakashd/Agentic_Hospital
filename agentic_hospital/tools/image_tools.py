"""Medical image analysis tool using AI vision capabilities.

Supports: skin lesions, X-rays, MRI, CT, ECG, wounds, retinal/fundus photos,
histopathology slides, ultrasound, PET/CT, and bone scans.
"""

import base64
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Type-specific analysis prompts
# ---------------------------------------------------------------------------

_IMAGE_TYPE_PROMPTS: dict[str, str] = {
    "skin_lesion": (
        "Analyze this dermatological image as an expert dermatologist.\n"
        "Evaluate:\n"
        "1. Lesion morphology: estimated size, shape, borders, color variation\n"
        "2. ABCDE criteria: Asymmetry, Border irregularity, Color variation, "
        "Diameter, Evolution clues\n"
        "3. Surface characteristics: texture, scale, crust, ulceration\n"
        "4. Surrounding skin changes and distribution pattern\n"
        "5. Differential diagnosis ranked by likelihood\n"
        "6. Urgency: routine / urgent / emergency referral\n"
        "7. Recommended next steps (dermoscopy, biopsy, patch test, topical treatment)"
    ),
    "xray": (
        "Analyze this radiograph as an expert radiologist.\n"
        "Evaluate:\n"
        "1. Image quality and technical adequacy\n"
        "2. Systematic review: bones, soft tissues, air-containing structures, "
        "foreign bodies\n"
        "3. All abnormal findings with anatomical location and description\n"
        "4. Significant normal findings\n"
        "5. Differential diagnosis for any abnormalities\n"
        "6. ACR communication urgency: routine / urgent / critical\n"
        "7. Recommended additional imaging if indicated"
    ),
    "mri": (
        "Analyze this MRI image as an expert radiologist/neuroradiologist.\n"
        "Evaluate:\n"
        "1. Sequence identification (T1, T2, FLAIR, DWI, GRE, etc.)\n"
        "2. Anatomical region and slice orientation\n"
        "3. Signal intensity abnormalities with precise location\n"
        "4. Mass effect, midline shift, herniation, or neural compression\n"
        "5. Enhancement patterns if contrast administration is evident\n"
        "6. Differential diagnosis ranked by likelihood\n"
        "7. Urgency and recommended follow-up"
    ),
    "ct": (
        "Analyze this CT image as an expert radiologist.\n"
        "Evaluate:\n"
        "1. Window/level settings apparent (soft tissue, bone, or lung window)\n"
        "2. Anatomical region and approximate slice level\n"
        "3. Abnormal densities, masses, fluid collections, calcifications\n"
        "4. Vascular structures if visible\n"
        "5. Bone and soft tissue assessment\n"
        "6. Differential diagnosis ranked by likelihood\n"
        "7. Communication urgency and follow-up recommendation"
    ),
    "ecg": (
        "Analyze this ECG/EKG as an expert cardiologist.\n"
        "Evaluate:\n"
        "1. Heart rate (from R-R interval) and rhythm (regular/irregular)\n"
        "2. P wave morphology, axis, and PR interval (ms)\n"
        "3. QRS complex: duration, morphology, electrical axis, bundle branch blocks\n"
        "4. ST segment: elevation or depression by lead, with localizing pattern\n"
        "5. T wave morphology and QT/QTc interval\n"
        "6. Notable patterns: delta waves, epsilon waves, Brugada, LQTS, STEMI equivalents\n"
        "7. Overall interpretation, clinical diagnosis, and urgency"
    ),
    "wound": (
        "Analyze this wound image as an expert wound care clinician.\n"
        "Evaluate:\n"
        "1. Wound classification: laceration, abrasion, ulcer (pressure/venous/"
        "arterial/diabetic), burn, surgical, traumatic\n"
        "2. Estimated size if scale reference is visible\n"
        "3. Wound bed: % granulation tissue, slough, eschar, necrosis\n"
        "4. Wound edges: regular/irregular, rolled, undermining signs\n"
        "5. Periwound tissue: erythema, induration, maceration, warmth\n"
        "6. Infection signs: purulence, biofilm sheen, cellulitis extension\n"
        "7. Wound healing stage (inflammatory / proliferative / remodeling)\n"
        "8. Recommended dressing type and management protocol"
    ),
    "retinal": (
        "Analyze this retinal/fundus photograph as an expert ophthalmologist.\n"
        "Evaluate:\n"
        "1. Optic disc: color, cup-to-disc ratio, margin sharpness, pallor\n"
        "2. Macula: foveal reflex, drusen, hard/soft exudates, hemorrhages\n"
        "3. Retinal vessels: caliber, A/V ratio, nicking, tortuosity\n"
        "4. Peripheral retina: hemorrhages, neovascularization, detachment signs\n"
        "5. Vitreous: hemorrhage or opacity\n"
        "6. Diabetic retinopathy grade (ETDRS scale) if applicable\n"
        "7. Hypertensive retinopathy grade if applicable\n"
        "8. Urgency and referral recommendation"
    ),
    "fundus": (
        "Analyze this fundus photograph as an expert ophthalmologist.\n"
        "Evaluate:\n"
        "1. Optic disc: color, cup-to-disc ratio, margin sharpness, pallor\n"
        "2. Macula: foveal reflex, drusen, exudates, hemorrhages\n"
        "3. Retinal vessels: caliber, A/V ratio, AV nicking, tortuosity\n"
        "4. Peripheral retina: hemorrhages, neovascularization, detachment signs\n"
        "5. Vitreous: hemorrhage or opacity\n"
        "6. Diabetic retinopathy grade (ETDRS) if applicable\n"
        "7. Hypertensive retinopathy grade if applicable\n"
        "8. Urgency and referral recommendation"
    ),
    "pathology_slide": (
        "Analyze this histopathology/cytology image as an expert pathologist.\n"
        "Evaluate:\n"
        "1. Stain type (H&E, IHC marker, PAS, Masson trichrome, etc.)\n"
        "2. Tissue architecture: normal vs disrupted, glandular/solid/other patterns\n"
        "3. Cellular features: size, shape, N:C ratio, nuclear pleomorphism, nucleoli\n"
        "4. Mitotic figures per high-power field (estimate)\n"
        "5. Inflammatory infiltrate type and distribution\n"
        "6. Malignant features: invasion, perineural/vascular invasion, necrosis\n"
        "7. Differential diagnosis using WHO classification\n"
        "8. Recommended additional IHC stains or molecular studies"
    ),
    "ultrasound": (
        "Analyze this ultrasound image as an expert sonographer/radiologist.\n"
        "Evaluate:\n"
        "1. Anatomical region and probe orientation\n"
        "2. Echo characteristics: hyperechoic, hypoechoic, anechoic, heterogeneous\n"
        "3. Organ morphology: size, shape, contour\n"
        "4. Abnormal findings: masses, cysts, calcifications, free fluid, thickening\n"
        "5. Vascularity if Doppler mode is visible\n"
        "6. Differential diagnosis for abnormalities\n"
        "7. Recommended follow-up or additional imaging"
    ),
    "pet_ct": (
        "Analyze this PET/CT image as an expert nuclear medicine physician.\n"
        "Evaluate:\n"
        "1. FDG-avid lesions: anatomical location, relative SUV, size\n"
        "2. CT correlation: corresponding structural abnormalities on the CT component\n"
        "3. Physiologic vs pathologic uptake distinction\n"
        "4. Disease distribution: primary, regional nodal, distant metastatic\n"
        "5. DEAUVILLE score (1–5) for lymphoma if applicable\n"
        "6. Treatment response assessment if prior imaging context is provided\n"
        "7. Clinical impression and management recommendation"
    ),
    "bone_scan": (
        "Analyze this nuclear medicine bone scintigraphy as an expert nuclear "
        "medicine physician.\n"
        "Evaluate:\n"
        "1. Radiotracer distribution across the skeleton\n"
        "2. Focal areas of increased uptake: location, intensity, pattern "
        "(solitary/multiple/superscan)\n"
        "3. Areas of photopenia (cold defects)\n"
        "4. Symmetry and physiologic uptake at expected sites\n"
        "5. Pattern: metastatic vs benign (Paget's, fracture, arthritis, "
        "fibrous dysplasia)\n"
        "6. Soft tissue uptake\n"
        "7. Correlation with X-ray/CT/MRI recommended"
    ),
    "general": (
        "Analyze this medical image as an expert clinician.\n"
        "Describe:\n"
        "1. Image modality and anatomical region\n"
        "2. Technical quality\n"
        "3. Key findings — normal structures and any abnormalities\n"
        "4. Clinical significance of findings\n"
        "5. Differential diagnosis if abnormalities are present\n"
        "6. Recommended next diagnostic steps"
    ),
}

# ---------------------------------------------------------------------------
# Image loading helper
# ---------------------------------------------------------------------------

def _load_image_as_data_uri(image_source: str) -> str:
    """Converts a file path, URL, raw base64, or existing data URI into the
    format expected by the vision API.

    Returns:
        str: A URL (for HTTPS sources) or a base64 data URI.
    """
    # Already an HTTPS/HTTP URL — pass through directly
    if image_source.startswith("http://") or image_source.startswith("https://"):
        return image_source

    # Already a well-formed data URI
    if image_source.startswith("data:"):
        return image_source

    # Raw base64 string (long, no path separators, no file extension)
    if (
        len(image_source) > 200
        and "/" not in image_source[:50]
        and not os.path.exists(image_source)
    ):
        return f"data:image/jpeg;base64,{image_source}"

    # Local file path
    path = Path(image_source)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_source}")

    _MIME_MAP = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
    }
    mime_type = _MIME_MAP.get(path.suffix.lower(), "image/jpeg")

    with open(path, "rb") as fh:
        encoded = base64.b64encode(fh.read()).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


# ---------------------------------------------------------------------------
# Public tool function
# ---------------------------------------------------------------------------

def analyze_medical_image(
    image_source: str,
    image_type: str = "general",
    clinical_context: str = "",
    patient_id: str = "",
) -> dict:
    """Analyzes a medical image using AI vision capabilities.

    Accepts skin photos, X-rays, MRI/CT scans, ECGs, wound images, fundus
    photographs, histopathology slides, ultrasound frames, PET/CT, and bone
    scans.  Pass the image as a local file path, an HTTPS URL, or a
    base64-encoded string.

    Args:
        image_source: File path, HTTPS URL, or base64-encoded image string.
        image_type: Medical image category.  One of:
            'skin_lesion', 'xray', 'mri', 'ct', 'ecg', 'wound',
            'retinal', 'fundus', 'pathology_slide', 'ultrasound',
            'pet_ct', 'bone_scan', 'general'.
        clinical_context: Patient symptoms, relevant history, or suspected
            diagnosis to guide the AI analysis (optional but recommended).
        patient_id: Optional patient ID for cross-referencing records.

    Returns:
        dict: Structured result with keys:
            status        – 'analyzed' or 'error'
            image_type    – the image_type used
            patient_id    – provided patient ID or 'not_provided'
            analysis      – full AI analysis text
            model_used    – model that performed the analysis
            disclaimer    – safety disclaimer
            message       – error description (only on error)
    """
    # --- Load image ---
    try:
        image_url = _load_image_as_data_uri(image_source)
    except FileNotFoundError as exc:
        return {"status": "error", "image_type": image_type, "message": str(exc)}
    except Exception as exc:
        return {
            "status": "error",
            "image_type": image_type,
            "message": f"Failed to load image: {exc}",
        }

    # --- Build analysis prompt ---
    type_key = image_type.lower() if image_type.lower() in _IMAGE_TYPE_PROMPTS else "general"
    analysis_prompt = _IMAGE_TYPE_PROMPTS[type_key]

    context_parts: list[str] = []
    if patient_id:
        context_parts.append(f"Patient ID: {patient_id}")
    if clinical_context:
        context_parts.append(f"Clinical context: {clinical_context}")
    if context_parts:
        analysis_prompt = (
            "Clinical context provided:\n"
            + "\n".join(context_parts)
            + "\n\n"
            + analysis_prompt
        )

    # --- Call vision model via LiteLLM ---
    try:
        import litellm  # noqa: PLC0415 – imported here to avoid startup overhead

        response = litellm.completion(
            model="openrouter/google/gemini-2.5-flash-lite",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": analysis_prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            max_tokens=1500,
        )
        analysis_text: str = response.choices[0].message.content or ""

        return {
            "status": "analyzed",
            "image_type": image_type,
            "patient_id": patient_id or "not_provided",
            "clinical_context": clinical_context or "none provided",
            "analysis": analysis_text,
            "model_used": "openrouter/google/gemini-2.5-flash-lite",
            "disclaimer": (
                "AI image analysis is for clinical decision-support only. "
                "All findings must be confirmed by a licensed radiologist or "
                "relevant specialist before clinical action is taken."
            ),
        }

    except Exception as exc:
        return {
            "status": "error",
            "image_type": image_type,
            "message": f"Image analysis failed: {exc}",
        }
