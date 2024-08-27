### Fonction d'extraction de villes de départ et d'arrivée
# Utilise le modele du dossier disktosave pour identifier les entités de départ (DEP) et d'arrivée (ARR) d'un texte'.

# import spacy

# nlp = spacy.load("./disktosave/model1")

def find_departure_arrival(text,nlp):
    # Chargement du modèle entraîné
    # Traiter le texte avec spaCy
    doc = nlp(text)

    return [ent.text for ent in doc.ents if ent.label_ == "DEP"], [ent.text for ent in doc.ents if ent.label_ == "ARR"]

# depart = find_departure_arrival("Mon trajet m'amène de paris à Bourg-en-bresse.",nlp)
# print(depart)
# depart = find_departure_arrival("je dois aller de lyon à nice.",nlp)
# print(depart)

