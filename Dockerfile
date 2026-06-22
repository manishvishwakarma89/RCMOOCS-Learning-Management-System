FROM python:3.11-slim

WORKDIR /app
#install dependecies
# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy file
COPY . .
#EXPOSE PORT
EXPOSE 5000
#start the app
CMD ["python","app.py"]

