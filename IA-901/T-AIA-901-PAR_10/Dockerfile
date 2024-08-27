# Utilisez une image basée sur ARM64
FROM python:3.9-slim

# Installation des dépendances système
RUN apt-get update && \
    apt-get install -y python3-pyaudio portaudio19-dev && \
    apt-get install -y tk && \
    apt-get install -y libportaudio2 && \
    rm -rf /var/lib/apt/lists/*

# Copiez votre script Python dans le conteneur
COPY main.py /app/main.py

# Définissez le répertoire de travail
WORKDIR /app

# Installez PyAudio avec pip
RUN pip install pyaudio
RUN pip install pydub

# Exécutez le script Python
CMD ["python", "main.py"]
