FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY mock_api /app

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]