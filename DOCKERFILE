# Use an official Python runtime as the base image
FROM python:3.7-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Run the command to start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
