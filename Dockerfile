FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port 7860 (Hugging Face default)
EXPOSE 7860

# Run the FastAPI app on port 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
