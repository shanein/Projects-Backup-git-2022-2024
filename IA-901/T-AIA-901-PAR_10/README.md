## installation rapide

depuis le dossier TextToSpeech:

```conda env create -f environment.yml```

```conda activate nom_de_lenv```

# Installation de l'environnement Conda

Ce guide vous aidera à installer et à activer un environnement Conda spécifique en utilisant le fichier environment.yml fourni.

## Prérequis

Anaconda ou Miniconda doit être installé sur votre système. Si ce n'est pas le cas, veuillez suivre les instructions d'installation sur le site officiel d'Anaconda ou le site officiel de Miniconda.


## Étapes d'installation

Cloner le dépôt ou télécharger le fichier environment.yml

Si le fichier est dans un dépôt git, commencez par cloner le dépôt. Sinon, téléchargez simplement le fichier environment.yml.

Naviguer jusqu'au répertoire contenant environment.yml

Ouvrez un terminal ou une Anaconda Prompt et naviguez jusqu'au répertoire où se trouve le fichier environment.yml.

```cd /chemin/vers/le/répertoire```

Créer l'environnement Conda

Exécutez la commande suivante pour créer un environnement Conda basé sur le fichier environment.yml :


```conda env create -f environment.yml```

Conda va lire le fichier environment.yml et installer toutes les dépendances nécessaires.

Activer l'environnement

Une fois l'installation terminée, activez l'environnement avec :

```conda activate nom_de_lenv```

Remplacez nom_de_lenv par le nom de l'environnement tel qu'il apparaît en haut du fichier environment.yml.

## Utilisation

Après avoir activé l'environnement, vous pouvez commencer à utiliser les paquets installés. Pour vérifier que l'environnement est correctement activé, vous pouvez 

utiliser la commande :

```conda info --envs```

Cela vous montrera une liste des environnements disponibles et l'environnement actuellement actif sera marqué avec une étoile (*).


## Lancement de l'application

Après avoir activé l'environnement, vous pouvez lancer l'application en exécutant le fichier `main.py`. Assurez-vous d'être dans le bon répertoire où se trouve le fichier `main.py`, puis exécutez la commande :

```bash
python main.py