FROM python:3.12-slim

# Create application directory
WORKDIR /app

# Install Python dependencies first
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Create a non-root user
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

# Flask application port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
