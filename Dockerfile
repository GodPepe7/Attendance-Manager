# Use an official lightweight Python image
FROM python:3.14

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (Flask default)
EXPOSE 5000

# Start the Flask app
CMD ["gunicorn", "-w", "4", "src.adapters.flask.app:create_app"]
