import re
from collections import Counter


STOP_WORDS = {
    "the",
    "and",
    "for",
    "are",
    "but",
    "not",
    "you",
    "your",
    "with",
    "that",
    "this",
    "from",
    "have",
    "has",
    "was",
    "were",
    "will",
    "would",
    "can",
    "could",
    "should",
    "into",
    "about",
    "their",
    "there",
    "they",
    "them",
    "his",
    "her",
    "its",
    "our",
    "out",
    "all",
    "any",
    "each",
    "more",
    "other",
    "than",
    "then",
    "when",
    "what",
    "which",
}


def generate_basic_summary(text: str, sentence_limit: int = 3) -> str:
    cleaned_text = " ".join(text.split())

    if not cleaned_text:
        return "No extractable text was found in this document."

    sentences = re.split(r"(?<=[.!?])\s+", cleaned_text)
    selected_sentences = sentences[:sentence_limit]

    return " ".join(selected_sentences)


def extract_keywords(text: str, keyword_limit: int = 10) -> list[str]:
    words = re.findall(r"\b[a-zA-Z][a-zA-Z]{3,}\b", text.lower())

    filtered_words = [
        word
        for word in words
        if word not in STOP_WORDS
    ]

    word_counts = Counter(filtered_words)

    return [
        word
        for word, _count in word_counts.most_common(keyword_limit)
    ]


def generate_document_insights(text: str) -> dict:
    return {
        "summary": generate_basic_summary(text),
        "keywords": extract_keywords(text),
    }
