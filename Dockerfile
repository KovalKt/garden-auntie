FROM python:3.12-slim

# Avoid Python cache files and pip noise
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PYTHONPATH=/app

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies first (Docker layer caching optimization -
# if requirements.txt doesn't change, this layer is reused on rebuild)
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the project and ChromaDB data
COPY src ./src
COPY chroma_db ./chroma_db

# Tell Streamlit not to open a browser 
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8080

# The port Railway will route traffic to
EXPOSE 8080

# Start the app
CMD ["streamlit", "run", "src/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
