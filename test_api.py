import requests

# Function to load PDF and classify
def test_pdf_classification():
    pdf_file_paths = [
        r"C:\Users\BK\Documents\task1\Medical_Report.pdf"    # Add more paths as needed
    ]

    for pdf_file_path in pdf_file_paths:
        print(f"Testing with: {pdf_file_path}")
        with open(pdf_file_path, 'rb') as f:
            load_response = requests.post("http://127.0.0.1:8000/load_pdf", files={"file": f})
            print("Load PDF Response:")
            print(f"Filename: {load_response.json().get('filename')}")
            print(f"Extracted Text:\n{load_response.json().get('extracted_text')}\n")
            print(f"Labels: {load_response.json().get('labels')}")
            print(f"Scores: {load_response.json().get('scores')}\n")

        extracted_text = load_response.json().get("extracted_text")
        classification_response = requests.post(
            "http://127.0.0.1:8000/classify", 
            json={"text": extracted_text}
        )
        print("Classification Response:")
        print(classification_response.json(), "\n")

        entities_response = requests.post(
            "http://127.0.0.1:8000/extract_entities", 
            json={"text": extracted_text}
        )
        print("Extract Entities Response:")
        for entity in entities_response.json().get("entities"):
            print(f"Entity: {entity[0]}, Label: {entity[1]}")
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_pdf_classification()
