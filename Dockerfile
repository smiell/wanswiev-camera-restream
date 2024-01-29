# Use the official Python 3.11 image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Install any dependencies
RUN pip install --no-cache-dir Flask requests opencv-python imutils

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port on which the application will run
EXPOSE 5000

# Run the application
CMD ["python", "stream.py"]
