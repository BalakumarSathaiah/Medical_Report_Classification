#ner_extractor.py
import spacy

# Load both models
nlp_medical = spacy.load("en_ner_bc5cdr_md")  # Medical model
nlp_general = spacy.load("en_core_web_md")  # General NER model

# Input text
text = input("Enter the document text: ")

# Apply medical model
doc_medical = nlp_medical(text)

# Apply general model
doc_general = nlp_general(text)

# Extract medical entities
medical_entities = [(ent.text, ent.label_) for ent in doc_medical.ents]

# Extract general entities
general_entities = [(ent.text, ent.label_) for ent in doc_general.ents]

# Combine results
combined_entities = medical_entities + general_entities

# Print combined results
print("Extracted Entities:")
for entity, label in combined_entities:
    print(f"{entity}: {label}")
