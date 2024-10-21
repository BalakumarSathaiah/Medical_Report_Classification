#app.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from pydantic import BaseModel
from pdf_extractor import extract_text_from_pdf
from ocr_extractor import extract_text_from_image
from text_classifier import classify_document
import os
import spacy

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical Report Classification API!"}

@app.post("/load_pdf")
async def load_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    temp_pdf_path = f"temp_{file.filename}"
    
    # Save uploaded PDF temporarily
    with open(temp_pdf_path, "wb") as f:
        f.write(contents)
    
    # Extract text from PDF
    extracted_text = extract_text_from_pdf(temp_pdf_path)

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No text extracted from the PDF.")
    
    # Clean up temporary file
    os.remove(temp_pdf_path)
    
    return {"filename": file.filename, "extracted_text": extracted_text}

@app.post("/load_image")
async def load_image(file: UploadFile = File(...)):
    contents = await file.read()
    temp_image_path = f"temp_{file.filename}"
    
    # Save uploaded image temporarily
    with open(temp_image_path, "wb") as f:
        f.write(contents)
    
    # Extract text from image using OCR
    extracted_text = extract_text_from_image(temp_image_path)
    
    # Clean up temporary file
    os.remove(temp_image_path)
    
    return {"filename": file.filename, "extracted_text": extracted_text}

@app.post("/classify")
async def classify(input: TextInput):
    labels = ["medical report", "diagnosis", "prescription", "lab results", "invoice"]
    classification = classify_document(input.text, labels)
    return {"classification": classification}

@app.post("/extract_entities")
async def extract_entities(input: TextInput):
    # Load both models
    nlp_medical = spacy.load("en_ner_bc5cdr_md")  # Medical model
    nlp_general = spacy.load("en_core_web_md")  # General NER model

    # Apply medical model
    doc_medical = nlp_medical(input.text)

    # Apply general model
    doc_general = nlp_general(input.text)

    # Extract medical and general entities
    medical_entities = [(ent.text, ent.label_) for ent in doc_medical.ents]
    general_entities = [(ent.text, ent.label_) for ent in doc_general.ents]

    # Combine and remove redundant entities (filtered by unique text)
    combined_entities = list({ent[0]: ent for ent in medical_entities + general_entities}.values())

    return {"entities": combined_entities}