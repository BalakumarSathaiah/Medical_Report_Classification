# Medical Report Classification and Query System

## Overview
This project is a Medical Report Classification and Query System that extracts text from medical reports in PDF or image format, classifies the type of document, and identifies medical entities using named entity recognition (NER).

### Features
- **PDF & Image Text Extraction**: Extracts text from PDF files and images using PyMuPDF and Tesseract OCR.
- **Document Classification**: Classifies medical documents into categories such as medical reports, prescriptions, lab results, and invoices using a zero-shot classifier.
- **Named Entity Recognition (NER)**: Identifies medical and general entities from the extracted text using pre-trained models like `en_ner_bc5cdr_md` for medical entities and `en_core_web_md` for general NER.

## Requirements
- Python 3.8+
- Libraries and models required:
  - `fastapi`
  - `uvicorn`
  - `spacy`
  - `transformers`
  - `pytesseract`
  - `Pillow`
  - `PyMuPDF`
  - Models: `en_ner_bc5cdr_md`, `en_core_web_md`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/BalakumarSathaiah/medical-report-classification.git
   ```
2. Navigate to the project directory:
   ```bash
   cd medical-report-classification
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Download and install the SpaCy models:
   ```bash
   python -m spacy download en_core_web_md
   python -m spacy download en_ner_bc5cdr_md
   ```

5. Install Tesseract OCR for image extraction:
   - Windows: Download and install Tesseract OCR from [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract).
   - Set the path to `tesseract.exe` in `ocr_extractor.py`.

## Running the Application Locally
1. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```

2. Test API Endpoints using tools like [curl](https://curl.se/) or by running the provided test script:
   ```bash
   python test_api.py
   ```

## API Endpoints
1. **GET /**
   - Returns a welcome message.
   
2. **POST /load_pdf**
   - Uploads and extracts text from a PDF file.
   - Request: `multipart/form-data` with a PDF file.
   
3. **POST /load_image**
   - Uploads and extracts text from an image file.
   - Request: `multipart/form-data` with an image file.
   
4. **POST /classify**
   - Classifies the document based on the extracted text.
   - Request body: `{ "text": "Extracted document text" }`
   
5. **POST /extract_entities**
   - Extracts named entities (both medical and general) from the text.
   - Request body: `{ "text": "Extracted document text" }`

## Acknowledgments
- [SpaCy](https://spacy.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
- [Transformers](https://huggingface.co/transformers/)
