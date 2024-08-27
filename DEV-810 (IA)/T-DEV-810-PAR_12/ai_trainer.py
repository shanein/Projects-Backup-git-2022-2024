# import pickle
import pickle

import numpy as np
from keras import Sequential, Model
from keras.applications import VGG19
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from keras import utils as np_utils
from keras.models import save_model, load_model
from sklearn.neural_network import MLPClassifier
import tensorflow as tf

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

import dataset

img_length = 750

# vgg model
# img_length = 32
#

#use pickle but error with Adam
def get_ai(regenerate=True):
    # if regenerate == True:
    #     model = start_training()
    #     save_ai(model)
    #     return model
    try:
        with open("model.pkl", "rb") as f:
            print("Found an existing IA")
            model = pickle.load(f)
            start_with_data(model)
            return model

    except Exception as ex:
        print("Error IA not found : ", str(ex))
        model = start_training()
        save_ai(model)
        return model

def save_ai(ai):
    try:
        with open("model.pkl", "wb") as f:
            pickle.dump(ai, f, protocol=pickle.HIGHEST_PROTOCOL)
            print("IA model create")
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)

##

#save and load model without pickle
# def get_ai(regenerate=True):
#     # if regenerate == True:
#     #     model = start_training()
#     #     save_ai(model)
#     #     return model
#     try:
#         with open("model.keras", "rb") as f:
#             print("Found an existing IA")
#             model = load_model("model.keras")
#             start_with_data(model)
#             return model
#
#     except Exception as ex:
#         print("Error IA not found : ", str(ex))
#         model = start_training()
#         save_ai(model)
#         return model
#
# def save_ai(ai):
#     try:
#         ai.save("model.keras")
#         print("Modèle IA créé et sauvegardé.")
#     except Exception as ex:
#         print("Erreur lors de la sauvegarde du modèle IA :", str(ex))

##

def start_training():
    print("Regenerating IA")
    train_x, train_y = dataset.import_dataset(dataset.Dataset.TRAIN, img_length)
    train_x = dataset.format_dataset(train_x, img_length)
    train_y = np_utils.to_categorical(train_y, 2)

    test_x, test_y = dataset.import_dataset(dataset.Dataset.TEST, img_length)
    test_x = dataset.format_dataset(test_x, img_length)
    test_y = np_utils.to_categorical(test_y, 2)

    #choose your model
    model = cnn_model(train_x, train_y, test_x, test_y)

    return model

def start_with_data(model):

    test_x, test_y = dataset.import_dataset(dataset.Dataset.TEST, img_length)
    test_x = dataset.format_dataset(test_x, img_length)
    test_y = np_utils.to_categorical(test_y, 2)

    score(model, test_x, test_y)





def cnn_model(train_x, train_y, test_x, test_y):
    # building a linear stack of layers with the sequential model
    model = Sequential()
    # hidden layer
    model.add(Dense(100, input_shape=(img_length * img_length,), activation='relu'))
    # output layer
    model.add(Dense(2, activation='softmax'))

    # looking at the model summary
    model.summary()
    # compiling the sequential model
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=tf.keras.optimizers.legacy.Adam())
    # training the model for 10 epochs
    history = model.fit(train_x, train_y, batch_size=128, epochs=10, validation_data=(test_x, test_y))

    eval_model(history)

    score(model, test_x, test_y)

    # Calculer la précision du modèle sur l'ensemble de test
    test_acc = model.evaluate(test_x, test_y)[1]
    print('Précision sur l\'ensemble de test :', test_acc)

    return model

def mlp_model(train_x, train_y, test_x, test_y):
    # building a linear stack of layers with the sequential model
    model = MLPClassifier(hidden_layer_sizes=(300,), verbose=2)

    model.fit(train_x, train_y)

    score(model, test_x, test_y)

    # Calculer la précision du modèle sur l'ensemble de test
    test_acc = model.score(test_x, test_y)
    print('Précision sur l\'ensemble de test :', test_acc)

    return model

def vgg_model(list_x, list_y, test_x, test_Y):

    print('X (vecteur): vgg:  ' + str(list_x.shape))


    #Redimonsionner en 32\
    list_x = np.repeat(list_x[..., np.newaxis], 3, axis=-1)
    list_x = np.array(list_x).reshape(-1, img_length, img_length, 3)
    print('X (vecteur) vgg: ' + str(list_x.shape))

    test_x = np.repeat(test_x[..., np.newaxis], 3, axis=-1)
    test_x = np.array(test_x).reshape(-1, img_length, img_length, 3)


    print('X (vecteur) vgg: ' + str(test_x.shape))


    # Charger le modèle VGG19 pré-entraîné
    base_model = VGG19(weights='imagenet', include_top=False, input_shape=(img_length, img_length, 3))

    # Geler les poids des couches du modèle VGG19
    for layer in base_model.layers:
        layer.trainable = False

    # Ajouter les nouvelles couches de classification
    x = base_model.output
    x = Flatten()(x)
    x = Dense(300, activation='relu')(x)
    predictions = Dense(2, activation='softmax')(x)

    # Créer le modèle final en spécifiant les entrées et les sorties
    model = Model(inputs=base_model.input, outputs=predictions)

    # Compiler le modèle avec une fonction de perte de catégorie croisée, un optimiseur Adam et la métrique de précision
    model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=0.001), metrics=['accuracy'])

    # Entraîner le modèle en utilisant les images d'entraînement et les étiquettes correspondantes
    history = model.fit(list_x, list_y, batch_size=128, epochs=10, validation_data=(test_x, test_Y))

    eval_model(history)
    score(model, test_x, test_Y)

    # Évaluer le modèle sur l'ensemble de test
    test_loss, test_acc = model.evaluate(test_x, test_Y)
    print('Perte sur l\'ensemble de test :', test_loss)
    print('Précision sur l\'ensemble de test :', test_acc)


    return model

def eval_model(history):
    # Validation Accuracy
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

    # Validation Loss
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Test Loss')
    plt.title('Training and validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()


def score(model, test_x, test_y):
    test_y_pred = np.argmax(model.predict(test_x), axis=-1)
    test_y_inverse = np.argmax(test_y, axis=1)

    # Calculer la matrice de confusion
    cm = confusion_matrix(test_y_inverse, test_y_pred)

    # Calculer les pourcentages par classe
    cm_percent = cm / cm.sum(axis=1).reshape(-1, 1)

    unique_labels = np.unique(test_y_inverse)


    # Afficher le graphique de matrice de confusion
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, annot_kws={"fontsize": 12}, cmap="Blues", cbar=False, fmt='d')
    for i in range(len(unique_labels)):
        for j in range(len(unique_labels)):
            percentage = cm_percent[i, j]
            text_color = 'white' if percentage > 0.5 else 'black'
            plt.text(j + 0.5, i + 0.5, f"\n\n({percentage:.2%})", ha='center', va='center', fontsize=12, color=text_color)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()

    print('L\'ensemble de test :\n', test_y_inverse)
    print('Prédictions sur l\'ensemble de test :\n', test_y_pred)
    # print("\n")
    print('20 premieres données de test :\n', test_y_inverse[:20])
    print('20 premieres données de la prediction de test :\n', test_y_pred[:20])

    # # Calculer la précision du modèle sur l'ensemble de test
    # test_acc = model.evaluate(test_x, test_y)[1]
    # print('Précision sur l\'ensemble de test :', test_acc)
