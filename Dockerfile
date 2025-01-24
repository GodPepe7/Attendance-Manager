FROM python:3.13

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "src.adapters.primary.app:create_app()"]
