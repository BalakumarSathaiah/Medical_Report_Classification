# Use a Python 3.8 base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the spaCy models to the correct locations
COPY ./model/en_ner_bc5cdr_md-0.5.4 /app/model/en_ner_bc5cdr_md-0.5.4
COPY ./model/en_core_web_md-3.1.0 /app/model/en_core_web_md-3.1.0

# Copy only the application files needed for the app to run
COPY app.py .          
COPY pdf_extractor.py . 
COPY ocr_extractor.py .
COPY text_classifier.py . 
COPY ner_extractor.py .  

# Run the application with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
