# Use lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install dependencies without cache for smaller image
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files to container
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run the app and bind to all interfaces
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]