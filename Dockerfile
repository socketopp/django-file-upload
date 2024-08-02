# # Use an official Python runtime as a parent image
# FROM python:3.10-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements.txt file into the container at /app
# COPY django_server/requirements.txt /app/

# # Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt

# # Copy the current directory contents into the container at /app
# COPY django_server /app/

# # Make port 8000 available to the world outside this container
# EXPOSE 8000

# # Define environment variable
# ENV PYTHONUNBUFFERED=1

# # Run manage.py with runserver command when the container launches
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Use the official Python image

FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Debugging step to check if pip is present
RUN python --version
RUN python -m pip --version || echo "pip is not installed"

# Install dependencies
RUN python -m ensurepip --upgrade
RUN python -m pip install --no-cache-dir -r requirements.txt || echo "pip install failed"

# Another debugging step to list installed packages
RUN python -m pip list || echo "pip list failed"

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Clean up any existing socket file
RUN rm -f /tmp/daphne.sock

# Default command (can be overridden by docker-compose)
CMD ["sh", "-c", "rm -f /tmp/daphne.sock && python manage.py makemigrations && python manage.py migrate && daphne -b 0.0.0.0 -p 8000 django_server.asgi:application"]
