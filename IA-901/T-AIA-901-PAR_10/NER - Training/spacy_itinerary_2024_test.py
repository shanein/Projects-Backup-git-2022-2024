### Ficher de test pour verifier l'efficacité de la methode spacy (méthode utilisée dans le projet) ###

import spacy
import json

from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Chargement du modèle entraîné
nlp = spacy.load("../NER/disktosave/model1")

# Charger le fichier JSON contenant les données d'entraînement
with open('./test.json', 'r', encoding='utf-8') as f:
    print("test")
    TRAIN_DATA = json.load(f)

total_examples = len(TRAIN_DATA['annotations'])
correct_examples = 0
incorrect_results = []

for text, annotations in TRAIN_DATA['annotations']:
    print(text)

for text, annotations in TRAIN_DATA['annotations']:
    entities = annotations['entities']
    doc = nlp(text)
    found_entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]

    # Convertir les tuples des entités trouvées en un set pour faciliter la comparaison
    found_entities_set = set(found_entities)
    true_entities_set = set([(start, end, label) for start, end, label in entities])

    # Comparer les entités trouvées avec les vraies entités
    if found_entities_set == true_entities_set:
        correct_examples += 1
    else:
        incorrect_results.append({'text': text, 'true': list(true_entities_set), 'found': list(found_entities_set)})

# Calculer la précision
accuracy = (correct_examples / total_examples) * 100

# Afficher les résultats
print(f'Précision du modèle: {accuracy:.2f}%')
print(f'Nombre d’exemples corrects: {correct_examples} sur {total_examples}')
# if incorrect_results:
#     print("\nExemples incorrects:")
#     for result in incorrect_results:
#         print(f"Texte: {result['text']}")
#         print(f"Vraies entités: {result['true']}")
#         print(f"Entités trouvées: {result['found']}\n")


# Précision du modèle: 86.99%