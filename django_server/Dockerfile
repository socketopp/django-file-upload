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

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Clean up any existing socket file
RUN rm -f /tmp/daphne.sock

# Default command (can be overridden by docker-compose)
# CMD ["daphne", "-u", "/tmp/daphne.sock", "django_server.asgi:application"]
# CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && daphne -b 0.0.0.0 -p 8000 -u /tmp/daphne.sock django_server.asgi:application"]
CMD ["sh", "-c", "rm -f /tmp/daphne.sock && python manage.py makemigrations && python manage.py migrate && daphne -b 0.0.0.0 -p 8000 django_server.asgi:application"]


