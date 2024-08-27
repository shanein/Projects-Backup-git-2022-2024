FROM python:3.11.2
WORKDIR /CryptoViz_Back
COPY ./ ./

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Exposez le port d'écoute de l'application
ENV PORT 8000
EXPOSE 8000
ENV HOST "127.0.0.1"
# Démarrez l'application

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]