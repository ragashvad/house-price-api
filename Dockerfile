# ============================================================
# Base image: Python 3.10 slim variant
# ============================================================
FROM python:3.10-slim

# ============================================================
# Set the working directory inside the container
# ============================================================
WORKDIR /app

# ============================================================
# Copy requirements first (for Docker's layer caching)
# ============================================================
COPY requirements.txt .

# ============================================================
# Install Python dependencies
# Use CPU-only PyTorch to keep image size manageable
# ============================================================
RUN pip install --no-cache-dir torch==2.5.0 --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

# ============================================================
# Copy the rest of the application
# ============================================================
COPY app/ ./app/
COPY models/ ./models/
COPY static/ ./static/ 
# ============================================================
# Expose the port the API will run on
# ============================================================
EXPOSE 7860

# ============================================================
# Command to run when the container starts
# ============================================================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]