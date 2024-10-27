from transformers import pipeline

def classify_document(text, labels, threshold=0.1):
    """Classifies the given text into the provided labels."""
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    result = classifier(text, labels)

    # Filter results based on the threshold
    filtered_results = [
        (label, score) for label, score in zip(result["labels"], result["scores"]) if score >= threshold
    ]

    filtered_labels, filtered_scores = zip(*filtered_results) if filtered_results else ([], [])

    return {
        "sequence": text,
        "labels": filtered_labels,
        "scores": filtered_scores
    }
