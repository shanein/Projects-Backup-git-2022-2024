FROM python:3.10.0
COPY . /app
# COPY .env ./

WORKDIR /app
COPY requirements.txt .
# Installer les dépendances
RUN pip3 install -r requirements.txt


# Exposez le port d'écoute de l'application
ENV PORT 8080
EXPOSE 8080
ENV HOST "0.0.0.0"
# Démarrez l'application

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]