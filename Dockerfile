FROM python:3.10-slim

# ------------------------------------------------
# Install system dependencies
# ------------------------------------------------
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    && apt-get clean

# ------------------------------------------------
# Prevent Python from writing .pyc files
# ------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ------------------------------------------------
# Set working directory
# ------------------------------------------------
WORKDIR /app

# ------------------------------------------------
# Copy requirements and install them
# ------------------------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ------------------------------------------------
# Copy project files
# ------------------------------------------------
COPY . .

# ------------------------------------------------
# Ensure uploads folder exists
# ------------------------------------------------
RUN mkdir -p uploads

# ------------------------------------------------
# Expose FastAPI port
# ------------------------------------------------
EXPOSE 8000

# ------------------------------------------------
# Run application
# ------------------------------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
