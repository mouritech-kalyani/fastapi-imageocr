# Use the official Python image as a base image
FROM python:3.10
 
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 
# Set the working directory in the container
WORKDIR /app
 
# Copy the requirements file into the container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the entire application into the container
COPY main.py .
 
# Expose port 8000
EXPOSE 8080
 
# Command to run the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]