### Ficher de test pour verifier l'efficacité de la methode brut (méthode envisagée mais pas utilisée dans le projet car moins efficace) ###

import json

# Charger le fichier JSON
with open('./test.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Importer spaCy
import spacy

# Charger le modèle spaCy
nlp = spacy.load('fr_core_news_sm')

# Fonction pour trouver le départ et l'arrivée
def find_departure_arrival(text):
    # Traiter le texte avec spaCy
    doc = nlp(text)

    departure, arrival = None, None

    # Mots-clés pour identifier le départ et l'arrivée
    departure_keywords = ['de', 'depuis', 'à partir de', 'au départ de', 'd\'', 'du', 'de la', 'des', 'dans', 'en provenance de', 'sortant de', 'quittant', 'partant de', 'émanant de']
    arrival_keywords = ['a','à', 'vers', 'jusqu\'à', 'pour', 'en direction de', 'à destination de', 'au', 'à la', 'aux', 'dans', 'sur', 'chez']

    # Trouver les entités LOC
    locations = [ent for ent in doc.ents if ent.label_ == 'LOC']

    # Logique pour déterminer le départ et l'arrivée et si on ne trouve pas de préposition
    if len(locations) == 2:
        # Si une seule préposition est trouvée
        if any(token.text.lower() in departure_keywords + arrival_keywords for token in doc):
            for ent in locations:
                prev_token = doc[ent.start - 1].text.lower() if ent.start > 0 else ''
                if prev_token in departure_keywords:
                    departure = ent
                elif prev_token in arrival_keywords:
                    arrival = ent
            # Si une entité est identifiée comme arrivée, l'autre est le départ, et vice versa
            if departure is None and arrival is not None:
                departure = [loc for loc in locations if loc != arrival][0]
            elif arrival is None and departure is not None:
                arrival = [loc for loc in locations if loc != departure][0]
        else:
            # Assigner par défaut le premier LOC comme départ et le second comme arrivée
            departure, arrival = locations[0], locations[1]

    return departure, arrival

total_examples = len(data['annotations'])
correct_examples = 0
incorrect_results = []

# Parcourir les exemples d'annotations dans le fichier JSON
for annotation in data['annotations']:
    text = annotation[0]
    entities = annotation[1]['entities']

    # Trouver les entités annotées pour le départ et l'arrivée
    annotated_departure = next((e for e in entities if e[2] == "DEP"), None)
    annotated_arrival = next((e for e in entities if e[2] == "ARR"), None)

    # S'assurer que les deux entités sont trouvées
    if annotated_departure is None or annotated_arrival is None:
        print("Erreur : une entité est manquante dans les annotations.")
        continue

    if len(text.split()) == 2:
        text = ' et '.join(text.split())

    # Utiliser la fonction pour trouver le départ et l'arrivée
    departure, arrival = find_departure_arrival(text)

    # Comparer les résultats avec les annotations attendues
    is_departure_correct = departure is not None and departure.text == text[annotated_departure[0]:annotated_departure[1]]
    is_arrival_correct = arrival is not None and arrival.text == text[annotated_arrival[0]:annotated_arrival[1]]

    if is_departure_correct and is_arrival_correct:
        correct_examples += 1
        print("Résultat: CORRECT")
    else:
        print("Résultat: INCORRECT")
        incorrect_results.append((text, annotated_departure, annotated_arrival, departure, arrival))

    # Afficher les détails
    print(f"Phrase: {text}")
    print(f"Départ attendu: {text[annotated_departure[0]:annotated_departure[1]]}, Arrivée attendue: {text[annotated_arrival[0]:annotated_arrival[1]]}")
    print(f"Départ trouvé: {departure.text if departure else 'Aucun'}, Arrivée trouvée: {arrival.text if arrival else 'Aucun'}")
    print()

# Calculer le pourcentage de correct
percentage_correct = (correct_examples / total_examples) * 100
print(f"Pourcentage de correct : {percentage_correct}%")
print(f"liste des erreurs : {incorrect_results}")

# Pourcentage de correct : 76.42276422764228%
