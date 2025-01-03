# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 8080

# Set the environment variable for Heroku
ENV PORT=8080

# Use Gunicorn to serve the app in production
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
