FROM python:3.9-slim
CMD ["gunicorn", "credit_approval_system.wsgi:application", "--bind", "0.0.0.0:8000"]


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
