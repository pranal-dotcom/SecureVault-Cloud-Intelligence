import re
from typing import Dict, List, Any, Tuple

# Precompiled PII regex patterns with high precision
PII_PATTERNS = {
    "AADHAAR": {
        # Indian Aadhaar: 12 digits (starts with 2-9, formatted as XXXX XXXX XXXX or contiguous)
        "regex": re.compile(r"\b[2-9]\d{3}[-\s]?\d{4}[-\s]?\d{4}\b"),
        "label": "[REDACTED_AADHAAR]",
        "name": "Indian Aadhaar Number"
    },
    "PAN": {
        # Indian PAN: 5 uppercase letters + 4 digits + 1 uppercase letter
        "regex": re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"),
        "label": "[REDACTED_PAN]",
        "name": "Permanent Account Number (PAN)"
    },
    "CREDIT_CARD": {
        # Major credit cards (Visa, MasterCard, Discover, Amex)
        "regex": re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12}|(?:[0-9]{4}[-\s]){3}[0-9]{4})\b"),
        "label": "[REDACTED_CREDIT_CARD]",
        "name": "Credit Card Number"
    },
    "EMAIL": {
        # Standard RFC email pattern
        "regex": re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b"),
        "label": "[REDACTED_EMAIL]",
        "name": "Email Address"
    },
    "PHONE": {
        # Indian (+91 / 10 digits starting 6-9) and international phone numbers
        "regex": re.compile(r"\b(?:\+?91[-\s]?)?[6-9]\d{9}\b|\b(?:\+?1[-.\s]?)?\(?[2-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
        "label": "[REDACTED_PHONE]",
        "name": "Phone / Mobile Number"
    }
}

def mask_preview(val: str, pii_type: str) -> str:
    """Creates a privacy-safe preview string for audit logs."""
    clean_val = val.strip()
    if pii_type in ("AADHAAR", "CREDIT_CARD", "PAN") and len(clean_val) >= 4:
        return f"{clean_val[:2]}****{clean_val[-2:]}"
    elif pii_type == "EMAIL" and "@" in clean_val:
        user, domain = clean_val.split("@", 1)
        return f"{user[:1]}***@{domain}"
    elif pii_type == "PHONE" and len(clean_val) >= 4:
        return f"{clean_val[:3]}****{clean_val[-2:]}"
    return "****"

def detect_and_redact_pii(text: str) -> Tuple[str, List[Dict[str, Any]], Dict[str, int]]:
    """
    Scans text for sensitive PII entities, generates sanitized text,
    and returns detected entity metadata.
    """
    if not text:
        return "", [], {}

    detected_entities: List[Dict[str, Any]] = []
    category_counts: Dict[str, int] = {}
    redacted_text = text

    # Order of processing: Credit Card & Aadhaar first, then PAN, Email, Phone
    ordered_keys = ["CREDIT_CARD", "AADHAAR", "PAN", "EMAIL", "PHONE"]

    for key in ordered_keys:
        info = PII_PATTERNS[key]
        pattern = info["regex"]
        label = info["label"]
        name = info["name"]

        matches = list(pattern.finditer(redacted_text))
        if matches:
            category_counts[key] = len(matches)
            for match in matches:
                matched_val = match.group(0)
                detected_entities.append({
                    "type": key,
                    "name": name,
                    "masked_preview": mask_preview(matched_val, key),
                    "start": match.start(),
                    "end": match.end()
                })

            # Replace with redaction label
            redacted_text = pattern.sub(label, redacted_text)

    return redacted_text, detected_entities, category_counts
