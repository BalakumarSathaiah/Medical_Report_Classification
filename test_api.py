import requests

def test_pdf_classification():
    pdf_file_path = "Report.pdf"

    # Test /load_pdf endpoint
    with open(pdf_file_path, 'rb') as f:
        response = requests.post("http://127.0.0.1:8000/load_pdf", files={"file": f})
    if response.status_code != 200:
        print(f"Failed to load PDF: {response.json()}")
        return
    print("Load PDF Response:")
    print(response.json())

    extracted_text = response.json().get("extracted_text", "")

    # Test /classify endpoint
    classify_response = requests.post("http://127.0.0.1:8000/classify", json={"text": extracted_text})
    if classify_response.status_code != 200:
        print(f"Classification failed: {classify_response.json()}")
        return
    print("\nClassification Response:")
    print(classify_response.json())

    # Test /extract_entities endpoint
    entities_response = requests.post("http://127.0.0.1:8000/extract_entities", json={"text": extracted_text})
    if entities_response.status_code != 200:
        print(f"Entity extraction failed: {entities_response.json()}")
        return

    print("\nExtract Entities Response:")
    entities = entities_response.json().get("combined_entities", [])
    if entities:
        print("Extracted Entities:\n" + "-"*30)
        for entity in entities:
            print(f"Entity: {entity['entity']:<20} | Label: {entity['label']}")
    else:
        print("No entities found.")

if __name__ == "__main__":
    test_pdf_classification()
