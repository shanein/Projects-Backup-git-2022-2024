import numpy as np
import self as self
from keras import Sequential, Model
from keras.applications import VGG16, VGG19
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.datasets import mnist
from keras.layers import Dense, Flatten
from matplotlib import pyplot
import cv2

from sklearn.neural_network import MLPClassifier
from tqdm import tqdm

(train_X, train_y), (test_X, test_y) = mnist.load_data()
print('X_train: ' + str(train_X.shape))
print('Y_train: ' + str(train_y.shape))
print('X_test:  ' + str(test_X.shape))
print('Y_test:  ' + str(test_y.shape))


#
# print('X_train (vecteur): ' + str(train_X_reshaped.shape))
# print('X_test (vecteur):' + str(test_X_reshaped.shape))


pyplot.clf()

# Moyenne
# for i in range(9):
#     pyplot.subplot(330 + 1 + i)
#     pyplot.imshow(train_X[i], cmap=pyplot.get_cmap('gray'))

# Affichage de la fréquence de chaque chiffre
# pyplot.plot(range(10), np.bincount(train_y))
# pyplot.xlabel('Chiffre')
# pyplot.ylabel('Nombre d\'images')
# pyplot.title('Fréquence des chiffres')
# pyplot.show()



def compress_image(image):
    # Convertir l'image en niveaux de gris
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer un flou gaussien pour réduire le bruit de l'image
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Binariser l'image
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Trouver le contour de l'image
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(contours, key=cv2.contourArea)

    # Trouver le rectangle englobant le contour et recadrer l'image
    x, y, w, h = cv2.boundingRect(cnt)
    image = image[y:y + h, x:x + w]

    # Redimensionner l'image en 28x28 pixels
    # image = cv2.resize(image, (28, 28))

    image = cv2.resize(image, (32, 32))

    return image


def showImageWork(list_X, list_y):

    list_X_compressed = [compress_image(img) for img in list_X]

    print('X_list: ' + str(list_X.shape))
    print('X_list: ' + str(np.array(list_X_compressed).shape))

    list_X = np.array(list_X_compressed)
    list_X_reshaped = np.array(list_X_compressed).reshape(list_X.shape[0], -1)

    # list_X_reshaped = train_X.reshape(train_X.shape[0], -1)
    # test_X_reshaped = test_X.reshape(test_X.shape[0], -1)

    print('X (vecteur): ' + str(list_X_reshaped.shape))
    # print('X_test (vecteur):' + str(test_X_reshaped.shape))

    display_mean_graph(list_X, list_X_reshaped, list_y)

    # normalizing the data to help with the training
    # Transformer les images de test en vecteurs de caractéristiques
    test_X_compressed = [compress_image(img) for img in test_X]
    test_X_reshaped = np.array(test_X_compressed).reshape(test_X.shape[0], -1)

    list_X_reshaped = list_X_reshaped.astype('float32')
    test_X_reshaped = test_X_reshaped.astype('float32')
    list_X_reshaped /= 255
    test_X_reshaped /= 255

    # one-hot encoding using keras' numpy-related utilities
    n_classes = 10
    print("Shape before one-hot encoding: ", list_y.shape)
    print("Shape before one-hot encoding: ", list_y)
    list_y = np_utils.to_categorical(list_y, n_classes)
    test_Y = np_utils.to_categorical(test_y, n_classes)
    print("Shape after one-hot encoding: ", list_y.shape)
    print("Shape after one-hot encoding: ", list_y)

    vgg_model(list_X_reshaped, list_y, test_X_reshaped, test_Y)

def display_mean_graph(list_X, list_X_reshaped, list_y):
    for i in range(10):
        # Affichage d'une image pour chaque chiffre de 0 à 9
        index = np.where(list_y == i)[0][0] # Trouve l'index de la première image correspondant au chiffre i
        image = list_X[index] # Charge l'image
        pyplot.subplot(2, 2, 1) # Définit l'emplacement de l'image dans la figure

        pyplot.imshow(image, cmap='gray') # Affiche l'image en niveau de gris
        pyplot.title(format(i))
        pyplot.axis('off') # Désactive les axes X et Y
        ##

        # Affichage moyenne d'une image pour chaque chiffre de 0 à 9
        indexMean = np.where(list_y == i)[0] # Trouve l'index des image correspondant au chiffre i
        images = list_X[indexMean] # Charge les images

        ImageMean = np.mean(images, axis=0)
        pyplot.subplot(2, 2, 3) # Définit l'emplacement de l'image dans la figure

        pyplot.imshow(ImageMean, cmap='gray')  # Affiche l'image en niveau de gris
        pyplot.title(format(i))
        pyplot.axis('off') # Désactive les axes X et Y
        ##

        # Affichage graphique d'une image pour chaque chiffre de 0 à 9
        imageGraph = list_X_reshaped[index]  # Charge les images (vecteurs)


        pyplot.subplot(2, 2, 2)  # Définit l'emplacement de l'image dans la figure

        pyplot.title(format(i))
        pyplot.axis('off')  # Désactive les axes X et Y

        pyplot.plot(imageGraph)
        # pyplot.title('Valeurs des pixels de l\'image ' + str(i))
        # pyplot.xlabel('Position des pixels')
        # pyplot.ylabel('Valeur des pixels')
        ##

        # Affichage graphique de la moyenne d'une image pour chaque chiffre de 0 à 9
        imagesGraph = list_X_reshaped[indexMean] # Charge les images (vecteurs)
        ImageMeanGraph = np.mean(imagesGraph, axis=0)

        pyplot.subplot(2, 2, 4) # Définit l'emplacement de l'image dans la figure

        pyplot.title(format(i))
        pyplot.axis('off') # Désactive les axes X et Y

        pyplot.plot(ImageMeanGraph)
        # pyplot.title('Valeurs des pixels de l\'image ' + str(i))
        # pyplot.xlabel('Position des pixels')
        # pyplot.ylabel('Valeur des pixels')
        ##

        pyplot.show()

        # diff = np.sum(np.abs(imageGraph - ImageMeanGraph))
        # print(str(i) + " : " + str(diff))
        #
        # for i in range(10):
        #     # Affichage d'une image pour chaque chiffre de 0 à 9
        #     indexMean = np.where(list_y == i)[0]
        #     imagesGraph = list_X_reshaped[indexMean]  # Charge les images (vecteurs)
        #     ImageMeanGraph = np.mean(imagesGraph, axis=0)
        #     diff = np.sum(np.abs(imageGraph - ImageMeanGraph))
        #     print(str(i) + " : " + str(diff))

def mlp_model(list_X_reshaped, list_y, test_X_reshaped, test_Y):
    #MLP
    # Initialiser le modèle MLPClassifier avec des paramètres de configuration
    # model = MLPClassifier(hidden_layer_sizes=(50,), max_iter=100, alpha=1e-4,
    #                       solver='sgd', verbose=10, tol=1e-4, random_state=1,
    #                       learning_rate_init=.1)
    model = MLPClassifier(hidden_layer_sizes=(300,), verbose=2)

    # # Entraîner le modèle en utilisant les images d'entraînement et les étiquettes correspondantes
    model.fit(list_X_reshaped, list_y)


    # Entraîner le modèle en utilisant les images d'entraînement et les étiquettes correspondantes
    # with tqdm(total=len(list_X_reshaped)) as pbar:
    #     for X, y in zip(list_X_reshaped, list_y):
    #         model.partial_fit([X], [y], classes=np.unique(list_y))
    #         pbar.update(1)

    # # Transformer les images de test en vecteurs de caractéristiques
    # test_X_compressed = [compress_image(img) for img in test_X]
    # test_X_reshaped = np.array(test_X_compressed).reshape(test_X.shape[0], -1)

    score(model, test_X_reshaped, test_Y)

    # Calculer la précision du modèle sur l'ensemble de test
    test_acc = model.score(test_X_reshaped, test_Y)
    print('Précision sur l\'ensemble de test :', test_acc)

    return model

def cnn_model(list_X_reshaped, list_y, test_X_reshaped, test_Y):
    #Test avec sequential


    model = Sequential()
    model.add(Dense(300, input_shape=(784,), activation='relu'))
    model.add(Dense(10, activation='softmax'))

    model.summary()

    # Compiler le modèle avec une fonction de perte de catégorie croisée, un optimiseur Adam et la métrique de précision
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Entraîner le modèle en utilisant les images d'entraînement et les étiquettes correspondantes
    model.fit(list_X_reshaped, list_y, batch_size=128, epochs=10, validation_data=(test_X_reshaped, test_Y))

    score(model, test_X_reshaped, test_Y)

    # Calculer la précision du modèle sur l'ensemble de test
    test_acc = model.evaluate(test_X_reshaped, test_Y)[1]
    print('Précision sur l\'ensemble de test :', test_acc)

    return model

def vgg_model(list_X_reshaped, list_y, test_X_reshaped, test_Y):

    #Redimonsionner en 32\
    list_X_reshaped= np.repeat(list_X_reshaped[..., np.newaxis], 3, axis=-1)
    list_X_reshaped = np.array(list_X_reshaped).reshape(-1, 32, 32, 3)
    print('X (vecteur) vgg: ' + str(list_X_reshaped.shape))

    test_X_reshaped= np.repeat(test_X_reshaped[..., np.newaxis], 3, axis=-1)
    test_X_reshaped = np.array(test_X_reshaped).reshape(-1, 32, 32, 3)


    print('X (vecteur) vgg: ' + str(test_X_reshaped.shape))


    # Charger le modèle VGG19 pré-entraîné
    base_model = VGG19(weights='imagenet', include_top=False, input_shape=(32, 32, 3))

    # Geler les poids des couches du modèle VGG19
    for layer in base_model.layers:
        layer.trainable = False

    # Ajouter les nouvelles couches de classification
    x = base_model.output
    x = Flatten()(x)
    x = Dense(300, activation='relu')(x)
    predictions = Dense(10, activation='softmax')(x)

    # Créer le modèle final en spécifiant les entrées et les sorties
    model = Model(inputs=base_model.input, outputs=predictions)

    # Compiler le modèle avec une fonction de perte de catégorie croisée, un optimiseur Adam et la métrique de précision
    model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.001), metrics=['accuracy'])

    # Entraîner le modèle en utilisant les images d'entraînement et les étiquettes correspondantes
    model.fit(list_X_reshaped, list_y, batch_size=128, epochs=10, validation_data=(test_X_reshaped, test_Y))

    score(model, test_X_reshaped, test_Y)

    # Évaluer le modèle sur l'ensemble de test
    test_loss, test_acc = model.evaluate(test_X_reshaped, test_Y)
    print('Perte sur l\'ensemble de test :', test_loss)
    print('Précision sur l\'ensemble de test :', test_acc)


    return model

def score(model, test_X_reshaped, test_Y):
    # Utiliser le modèle pour prédire les étiquettes des images de test
    test_y_pred = np.argmax(model.predict(test_X_reshaped), axis=-1)
    test_Y_inverse = np.argmax(test_Y, axis=1)
    print('L\'ensemble de test :\n', test_Y_inverse)
    print('Prédictions sur l\'ensemble de test :\n', test_y_pred)
    print("\n")
    print('L\'ensemble de test :\n', test_Y_inverse[:20])
    print('Prédictions sur l\'ensemble de test :\n', test_y_pred[:20])




showImageWork(train_X, train_y)
