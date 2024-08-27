### Méthode alternative pour identifier les villes de départ et d'arrivée
# Utilise spaCy pour identifier les localisations du texte et une logique personnalisée basée sur des mots-clés pour déterminer les entités de départ (DEP) et d'arrivée (ARR).

import spacy

# Charger le modèle spaCy
nlp = spacy.load('fr_core_news_sm')

# Fonction pour trouver le départ et l'arrivée
def find_departure_arrival(text,nlp):
    # Traiter le texte avec spaCy
    doc = nlp(text)

    departure, arrival = None, None
    departure_keywords = ['de', 'depuis', 'à partir de', 'au départ de', 'd\'', 'du', 'de la', 'des', 'dans', 'en provenance de', 'sortant de', 'quittant', 'partant de', 'émanant de']
    arrival_keywords = ['a','à', 'vers', 'jusqu\'à', 'pour', 'en direction de', 'à destination de', 'au', 'à la', 'aux', 'dans', 'sur', 'chez', 'pour aller à', 'pour aller en', 'pour aller vers', 'pour aller dans', 'pour aller sur', 'pour aller au', 'pour aller aux', 'pour aller jusqu\'à', 'pour aller jusqu\'au', 'pour aller jusqu\'aux', 'pour aller jusqu\'à la', 'pour aller jusqu\'à l\'']

    # Trouver les entités LOC
    locations = [ent for ent in doc.ents if ent.label_ == 'LOC']

    # Logique pour déterminer le départ et l'arrivée
    if len(locations) == 2:
        if any(token.text.lower() in departure_keywords + arrival_keywords for token in doc):
            for ent in locations:
                prev_token = doc[ent.start - 1].text.lower() if ent.start > 0 else ''
                if prev_token in departure_keywords:
                    departure = ent
                elif prev_token in arrival_keywords:
                    arrival = ent
            if departure is None and arrival is not None:
                departure = [loc for loc in locations if loc != arrival][0]
            elif arrival is None and departure is not None:
                arrival = [loc for loc in locations if loc != departure][0]
        else:
            departure, arrival = locations[0], locations[1]

    return departure, arrival

# Fonction pour utiliser la détection de départ et d'arrivée en temps réel
def get_departure_arrival_from_sentence(sentence,nlp):
    # Gérer les cas spéciaux
    if len(sentence.split()) == 2:
        sentence = ' et '.join(sentence.split())

    # Utiliser la fonction pour trouver le départ et l'arrivée
    departure, arrival = find_departure_arrival(sentence,nlp)

    # Formater le résultat
    departure_text = departure.text if departure else "Aucun"
    arrival_text = arrival.text if arrival else "Aucun"

    return departure_text, arrival_text

# Exemple d'utilisation
sentence = "je veux aller de Paris à Marseille"
departure, arrival = get_departure_arrival_from_sentence(sentence,nlp)
print(f"Départ: {departure}, Arrivée: {arrival}")
sentence = "je dois partir de Lyon pour aller à Nice"
departure, arrival = get_departure_arrival_from_sentence(sentence,nlp)
print(f"Départ: {departure}, Arrivée: {arrival}")
