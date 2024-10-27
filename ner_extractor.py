import spacy
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load models
nlp_medical = spacy.load("model/en_ner_bc5cdr_md-0.5.4")  # Medical model
nlp_general = spacy.load("model/en_core_web_md-3.1.0")    # General model

# Known medical terms and keywords
known_tests = {"ECG", "CBC", "MRI", "X-Ray", "Blood Test", "Complete Blood Count", "WBC", "Platelets"}
known_drugs = {"Metformin", "Amlodipine", "Azithromycin", "Ibuprofen", "Amoxicillin"}  # Expanded drug list
known_diseases = {"diabetes", "hypertension", "asthma", "cancer", "splenomegaly"}  # Added diseases
known_organs = {"liver", "spleen", "kidneys", "heart", "lungs", "pancreas", "stomach"}  # Expanded organ list

# Regex patterns
doctor_pattern = re.compile(r"\bDr\.\s+\w+\b", re.IGNORECASE)
id_pattern = re.compile(r"(ID|PASSPORT|CNO REF)\s*:\s*[\w\-]+", re.IGNORECASE)
date_pattern = re.compile(r"\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}\b")  # Handles various date formats
dosage_pattern = re.compile(r"\b\d+\s*(mg|ml|g|units)\b", re.IGNORECASE)  # Added units

def extract_entities(text):
    """Extracts entities from the given text using both models and custom rules."""
    logging.info("Extracting entities from text: %s", text)
    try:
        # Apply both models
        doc_medical = nlp_medical(text)
        doc_general = nlp_general(text)

        # Collect entities from both models
        medical_entities = [(ent.text.strip(), ent.label_) for ent in doc_medical.ents]
        general_entities = [(ent.text.strip(), ent.label_) for ent in doc_general.ents]

        # Combine and prioritize entities
        combined_entities = prioritize_medical_entities(medical_entities, general_entities)

        # Apply rules and refine labels
        refined_entities = consolidate_and_refine(combined_entities)

        return refined_entities
    except Exception as e:
        logging.error("Error extracting entities: %s", e)
        return []

def prioritize_medical_entities(medical_entities, general_entities):
    """Prioritize entities from the medical model and resolve conflicts."""
    combined = {text.lower(): label for text, label in general_entities}  # General model

    for text, label in medical_entities:
        lower_text = text.lower()
        # Give precedence to medical entities (like DISEASE or MEDICAL_TEST)
        if label in {"DISEASE", "MEDICAL_TEST"} or lower_text not in combined:
            combined[lower_text] = label

    return list(combined.items())

def consolidate_and_refine(entities):
    """Refine and clean entity labels based on custom rules and patterns."""
    refined_entities = []
    unique_entities = {}

    # Deduplicate entities (case-insensitive) while preserving context
    for text, label in entities:
        lower_text = text.lower()
        if lower_text not in unique_entities:
            unique_entities[lower_text] = label

    for text, label in unique_entities.items():
        # Apply custom labeling rules
        if id_pattern.search(text):
            label = "ID"
        elif date_pattern.search(text):
            label = "DATE"
        elif dosage_pattern.search(text):
            label = "DOSAGE"
        elif text in known_tests:
            label = "MEDICAL_TEST"
        elif text in known_drugs:
            label = "DRUG"
        elif text in known_diseases:
            label = "DISEASE"
        elif text in {"daily", "5 days", "7 days", "2 weeks", "3 days", "10 years ago"}:
            label = "FREQUENCY"
        elif text.lower() in known_organs:
            label = "ORGAN"
        elif "splenomegaly" in text.lower():
            label = "DISEASE"
        elif text == "blood":
            label = "BODY_FLUID"
        elif label == "CARDINAL" and text.replace(".", "").isdigit():
            label = "NUMERIC_VALUE"

        refined_entities.append({"entity": text, "label": label})

    return refined_entities
