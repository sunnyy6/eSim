# Use an official Python runtime as the base image
FROM python:3.6

LABEL org.opencontainers.image.source https://github.com/FOSSEE/eSim

# Set the working directory in the container
WORKDIR /src/frontEnd

# Copy the requirements.txt file to the container  
COPY requirements.txt requirements.txt

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Define the command to run your application
CMD python3 Application.py
