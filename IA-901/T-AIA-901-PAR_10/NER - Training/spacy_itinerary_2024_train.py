### Ficher d'entrainement pour entrainer notre modele basée sur spacy ###

import spacy
from spacy.training import Example
import random
import json
nlp = spacy.load("fr_core_news_sm")

# Step 2: Setup
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")
LABELS = ["DEP", "ARR"]
for label in LABELS:
    ner.add_label(label)

# use a json file to load the training data
# {"classes":["DEP","ARR"],"annotations":[["Mon trajet m'amène de Paris à Marseille.",{"entities":[[22,27,"DEP"],[30,39,"ARR"]]}],["Je dois aller de Lyon à Nice.",{"entities":[[17,21,"DEP"],[24,28,"ARR"]]}]]}
with open("./train.json") as f:
    TRAIN_DATA = json.load(f)["annotations"]

model=None

if model is None:
    optimizer = nlp.begin_training()
else:
    optimizer = nlp.entity.create_optimizer()

# Entraînement du modèle
# Séparation des données en ensembles d'entraînement et de test
random.shuffle(TRAIN_DATA)
split = int(len(TRAIN_DATA) * 0.8)  # 80% pour l'entraînement, 20% pour les tests
train_data = TRAIN_DATA[:split]
test_data = TRAIN_DATA[split:]

# Entraînement du modèle
optimizer = nlp.begin_training()
for iteration in range(35):
    random.shuffle(train_data)
    losses = {}
    for text, annotations in train_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], drop=0.5, losses=losses)

    # Évaluation du modèle
    correct_predictions, total_predictions = 0, 0
    for text, annotations in test_data:
        doc = nlp(text)
        for ent in doc.ents:
            total_predictions += 1
            if any([ent.text == e[0] and ent.label_ == e[2] for e in annotations['entities']]):
                correct_predictions += 1

    precision = correct_predictions / total_predictions if total_predictions > 0 else 0
    print(f"Iteration {iteration} - Loss: {losses} - Precision: {precision}")

# Enregistrement du modèle
nlp.to_disk("../NER/disktosave/model1")




