FROM python:3.9-slim
RUN apt-get update && apt-get install -y netcat

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Define entrypoint
ENTRYPOINT ["sh", "entrypoint.sh"]
