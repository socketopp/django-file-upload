# FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# ENV PYTHONUNBUFFERED 1

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY ../requirements.txt .

# Install the dependencies
RUN apt-get update && apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install dependencies
RUN python -m ensurepip --upgrade
RUN python -m pip install --no-cache-dir -r requirements.txt || echo "pip install failed"

# Copy the rest of the application code
COPY . .

RUN rm -f /tmp/daphne.sock

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

