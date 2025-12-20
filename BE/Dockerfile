# Use official Python base image
FROM python:3.11

# Set working dir inside container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code into container
COPY . .

# (Optional) expose HTTP port
EXPOSE 8000

# Run Uvicorn to start the FastAPI / LangServe server
CMD ["langchain", "serve", "--host", "0.0.0.0", "--port", "8000"]