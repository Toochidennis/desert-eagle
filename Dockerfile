# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV DEBUG=False

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
