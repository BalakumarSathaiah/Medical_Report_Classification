# pdf_extractor.py
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extracts text from each page of the PDF file."""
    text = ""
    with fitz.open(pdf_path) as pdf_file:
        for page in pdf_file:
            text += page.get_text()
    return text

if __name__ == "__main__":
    pdf_path = input("Enter the PDF file path: ")
    extracted_text = extract_text_from_pdf(pdf_path)
    print("Extracted Text:\n", extracted_text)
