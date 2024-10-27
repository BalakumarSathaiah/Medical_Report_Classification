from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pdf_extractor import extract_text_from_pdf
from ocr_extractor import extract_text_from_image
from text_classifier import classify_document
from ner_extractor import extract_entities  
import os
import spacy
import logging

# Initialize logging to suppress lower level logs
logging.basicConfig(level=logging.CRITICAL)

app = FastAPI()

# Load models once when the app starts
try:
    nlp_medical = spacy.load("model/en_ner_bc5cdr_md-0.5.4")  # Medical model
    nlp_general = spacy.load("model/en_core_web_md-3.1.0")    # General model
except Exception as e:
    logging.critical(f"Error loading models: {e}")
    raise RuntimeError("Failed to load NLP models. Check model paths and ensure Docker image has the required models.")

class TextInput(BaseModel):
    text: str

# In-memory storage for extracted text
extracted_text_storage = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical Report Classification API!"}

@app.post("/load_pdf")
async def load_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Unsupported file type. Please upload a PDF.")

    contents = await file.read()
    temp_pdf_path = f"temp_{file.filename}"

    with open(temp_pdf_path, "wb") as f:
        f.write(contents)

    try:
        extracted_text = extract_text_from_pdf(temp_pdf_path)
    except Exception as e:
        logging.critical(f"Error extracting text from PDF: {e}")
        raise HTTPException(status_code=500, detail="Error extracting text from PDF.")

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No text extracted from the PDF.")

    os.remove(temp_pdf_path)

    # Store the extracted text in memory
    extracted_text_storage['latest'] = extracted_text
    return {"filename": file.filename, "extracted_text": extracted_text}

@app.post("/load_image")
async def load_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Unsupported file type. Please upload an image.")

    contents = await file.read()
    temp_image_path = f"temp_{file.filename}"

    with open(temp_image_path, "wb") as f:
        f.write(contents)

    try:
        extracted_text = extract_text_from_image(temp_image_path)
    except Exception as e:
        logging.critical(f"Error extracting text from image: {e}")
        raise HTTPException(status_code=500, detail="Error extracting text from image.")

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No text extracted from the image.")

    os.remove(temp_image_path)

    # Store the extracted text in memory
    extracted_text_storage['latest'] = extracted_text
    return {"filename": file.filename, "extracted_text": extracted_text}

@app.post("/classify")
async def classify():
    # Retrieve the extracted text from memory
    extracted_text = extracted_text_storage.get('latest')
    if not extracted_text:
        raise HTTPException(status_code=400, detail="No text available. Please upload a file first.")

    labels = ["medical report", "diagnosis", "prescription", "lab results", "invoice"]
    try:
        classification = classify_document(extracted_text, labels)
    except Exception as e:
        logging.critical(f"Error during classification: {e}")
        raise HTTPException(status_code=500, detail="Error during document classification.")

    return {"classification": classification}

@app.post("/extract_entities")
async def extract_entities_endpoint():
    extracted_text = extracted_text_storage.get('latest')
    if not extracted_text:
        raise HTTPException(status_code=400, detail="No text available. Please upload a file first.")

    try:
        combined_entities = extract_entities(extracted_text)
    except Exception as e:
        logging.critical(f"Error during entity extraction: {e}")
        raise HTTPException(status_code=500, detail="Error during entity extraction.")

    # Format the response
    response = {"combined_entities": [{"entity": ent['entity'], "label": ent['label']} for ent in combined_entities]}
    return response