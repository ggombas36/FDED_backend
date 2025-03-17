# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Másold be a függőségeket
COPY requirements.txt .

# Telepítsd a függőségeket
RUN pip install --no-cache-dir -r requirements.txt

# Másold be a projektfájlokat
COPY . .

# Expose port
EXPOSE 8000

# Indítsd a FastAPI alkalmazást
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]