# FROM python:3.11-slim

# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# # Copy and install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy Streamlit application
# COPY streamlit_app.py .

# # Expose Streamlit port
# EXPOSE 8501

# # Disable CORS and XSRF for frontend (safe inside Docker)
# ENV STREAMLIT_SERVER_ENABLECORS=false
# ENV STREAMLIT_SERVER_ENABLEXsrfProtection=false

# CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]


# Frontend Dockerfile
FROM python:3.10-slim

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# Streamlit run command
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]