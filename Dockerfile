# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.13.0-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# Install required libraries for pygame.mixer
RUN apt-get update && apt-get install -y \
    libsdl2-mixer-2.0-0 \
    libasound2 \
    libasound2-data \  
    libasound2 libasound2-dev libasound2-plugins \
    && apt-get clean

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "Scripts/Main.py"]
