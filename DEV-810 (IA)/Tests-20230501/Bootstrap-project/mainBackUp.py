import numpy as np
import self as self
from keras.datasets import mnist
from matplotlib import pyplot


(train_X, train_y), (test_X, test_y) = mnist.load_data()
print('X_train: ' + str(train_X.shape))
print('Y_train: ' + str(train_y.shape))
print('X_test:  ' + str(test_X.shape))
print('Y_test:  ' + str(test_y.shape))


train_X_reshaped = train_X.reshape(train_X.shape[0], -1)
test_X_reshaped = test_X.reshape(test_X.shape[0], -1)

print('X_train (vecteur): ' + str(train_X_reshaped.shape))
print('X_test (vecteur):' + str(test_X_reshaped.shape))


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

# Affichage d'une image pour chaque chiffre de 0 à 9
for i in range(10):
    index = np.where(train_y == i)[0][0] # Trouve l'index de la première image correspondant au chiffre i
    image = train_X[index] # Charge l'image
    pyplot.subplot(2, 5, i+1) # Définit l'emplacement de l'image dans la figure

    # pyplot.subplot(1, 10, i + 1)
    pyplot.imshow(image, cmap='gray') # Affiche l'image en niveau de gris
    pyplot.title(format(i))
    pyplot.axis('off') # Désactive les axes X et Y
pyplot.show()

# Affichage moyenne d'une image pour chaque chiffre de 0 à 9
for i in range(10):
    indexMean = np.where(train_y == i)[0] # Trouve l'index des image correspondant au chiffre i
    images = train_X[indexMean] # Charge les images

    ImageMean = np.mean(images, axis=0)
    pyplot.subplot(2, 5, i+1) # Définit l'emplacement de l'image dans la figure
    pyplot.imshow(ImageMean, cmap='gray')  # Affiche l'image en niveau de gris
    #
    # pyplot.subplot(1, 10, i + 1)
    # pyplot.imshow(image, cmap='gray') # Affiche l'image en niveau de gris
    pyplot.title(format(i))
    pyplot.axis('off') # Désactive les axes X et Y
pyplot.show()


# Affichage graphique de la moyenne d'une image pour chaque chiffre de 0 à 9
for i in range(10):
    indexMean = np.where(train_y == i)[0] # Trouve l'index des images correspondant au chiffre i
    imagesGraph = train_X_reshaped[indexMean] # Charge les images (vecteurs)

    ImageMeanGraph = np.mean(imagesGraph, axis=0)

    pyplot.subplot(2, 5, i+1) # Définit l'emplacement de l'image dans la figure
    pyplot.title(format(i))
    pyplot.axis('off') # Désactive les axes X et Y

    pyplot.plot(ImageMeanGraph)
    # pyplot.title('Valeurs des pixels de l\'image ' + str(i))
    # pyplot.xlabel('Position des pixels')
    # pyplot.ylabel('Valeur des pixels')

pyplot.show()



# print(train_y)