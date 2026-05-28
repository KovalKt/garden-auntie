FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies first (Docker layer caching optimization -
# if requirements.txt doesn't change, this layer is reused on rebuild)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Tell Streamlit not to open a browser 
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8080

# The port Railway will route traffic to
EXPOSE 8080

# Start the app
CMD ["streamlit", "run", "src/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
