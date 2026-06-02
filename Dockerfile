# Base image — Python 3.12 slim for smaller image size
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (build-essential added and cleaned up to save space)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create specific nested subdirectories that might not exist on the host
RUN mkdir -p documents/eda_charts documents/shap_charts

# Copy project files into container
COPY data/ data/
COPY documents/ documents/
COPY sql/ sql/
COPY models/ models/
COPY notebooks/ notebooks/
COPY src/ src/
COPY ui/ ui/
COPY app.py .

# Expose Streamlit port
EXPOSE 8501

# Streamlit config environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_HEADLESS=true

# Run the app (Cleaned up flags since ENV variables handle them)
CMD ["streamlit", "run", "app.py"]
