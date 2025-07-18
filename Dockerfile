# Start from a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports
EXPOSE 8000
EXPOSE 8501

# Run both backend (FastAPI) and frontend (Streamlit) in parallel
CMD ["bash", "-c", "uvicorn captain:app --host 0.0.0.0 --port 8000 & streamlit run frontend/chat_ui.py"]
