# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Environment variables within image
ENV OpenAI_Key=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

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port on which the app will run
EXPOSE 8000

# Command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
