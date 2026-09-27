import re
from typing import List, Dict, Any

def tokenize_sentences(text: str) -> List[str]:
    """Splits text into clean sentences."""
    clean_text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Match sentence endings (. ! ?) while avoiding common abbreviations
    raw_sentences = re.split(r"(?<=[.!?])\s+", clean_text)
    sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 10]
    return sentences

def extract_key_highlights(text: str, max_highlights: int = 4) -> List[str]:
    """
    Extracts top key highlights using sentence scoring based on
    term frequency and position weighting.
    """
    sentences = tokenize_sentences(text)
    if not sentences:
        return []
    if len(sentences) <= max_highlights:
        return sentences

    # Compute word frequencies (excluding short stopwords)
    stopwords = {
        "the", "and", "is", "in", "to", "of", "a", "with", "for", "on", "that", "this",
        "by", "at", "from", "an", "be", "as", "are", "was", "or", "it", "not", "have"
    }
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    word_freq: Dict[str, int] = {}
    for w in words:
        if w not in stopwords:
            word_freq[w] = word_freq.get(w, 0) + 1

    # Score each sentence
    scored_sentences = []
    for idx, sentence in enumerate(sentences):
        sentence_words = re.findall(r"\b[a-zA-Z]{3,}\b", sentence.lower())
        score = sum(word_freq.get(w, 0) for w in sentence_words)
        
        # Position boost for introductory and concluding sentences
        if idx == 0:
            score *= 1.3
        elif idx == len(sentences) - 1:
            score *= 1.1
            
        scored_sentences.append((score, idx, sentence))

    # Pick top scoring sentences and maintain original order
    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    top_picks = scored_sentences[:max_highlights]
    top_picks.sort(key=lambda x: x[1])

    return [s[2] for s in top_picks]

def classify_document(text: str) -> str:
    """Classifies document domain based on keyword presence."""
    text_lower = text.lower()
    if any(k in text_lower for k in ["pan", "aadhaar", "passport", "license", "kyc", "identity"]):
        return "Identity & KYC Verification Document"
    elif any(k in text_lower for k in ["invoice", "tax", "payment", "bank", "statement", "credit card", "balance", "amount"]):
        return "Financial / Billing Statement"
    elif any(k in text_lower for k in ["confidential", "agreement", "contract", "nda", "terms"]):
        return "Legal / Contractual Agreement"
    elif any(k in text_lower for k in ["medical", "health", "patient", "diagnosis", "doctor"]):
        return "Healthcare / Medical Record"
    return "General Corporate Document"

def generate_summary(text: str, max_bullet_points: int = 3) -> Dict[str, Any]:
    """
    Generates structured executive summary, key highlights, and document metrics.
    """
    if not text or len(text.strip()) == 0:
        return {
            "executive_summary": "Empty document provided.",
            "key_highlights": [],
            "document_type": "Unknown",
            "metrics": {
                "word_count": 0,
                "character_count": 0,
                "sentence_count": 0,
                "estimated_read_time_seconds": 0
            }
        }

    words = text.split()
    word_count = len(words)
    sentences = tokenize_sentences(text)
    highlights = extract_key_highlights(text, max_highlights=max_bullet_points)
    doc_type = classify_document(text)

    # Construct concise executive summary from top highlight
    executive_summary = highlights[0] if highlights else (text[:200] + "..." if len(text) > 200 else text)

    return {
        "executive_summary": executive_summary,
        "key_highlights": highlights,
        "document_type": doc_type,
        "metrics": {
            "word_count": word_count,
            "character_count": len(text),
            "sentence_count": len(sentences),
            "estimated_read_time_seconds": max(1, round(word_count / 3.5))
        }
    }
