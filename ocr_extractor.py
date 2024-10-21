# ocr_extractor.py
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\BK\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """Extracts text from image using Tesseract OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

if __name__ == "__main__":
    image_path = input("Enter the image file path: ")
    extracted_text = extract_text_from_image(image_path)
    print("Extracted Text from Image:\n", extracted_text)
