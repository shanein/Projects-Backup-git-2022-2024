import gymnasium as gym
import numpy as np
import pickle
import time
from IPython.display import clear_output
import matplotlib.pyplot as plt

# Charger les modèles
def load_model(filename):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    return model

# Fonction pour exécuter et visualiser le modèle
def run_model(env, model, episodes=1):
    for episode in range(episodes):
        state, _ = env.reset()
        terminated = False
        total_reward = 0
        steps = 0

        while not terminated:
            # Rendu de l'environnement
            img = env.render()
            plt.imshow(img)
            plt.axis('off')
            clear_output(wait=True)
            plt.show()
            time.sleep(0.5)  # Pour ralentir l'affichage

            # Choisir l'action selon le modèle
            action = np.argmax(model[state])
            state, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1

            print(total_reward)

        print(f"Episode terminé en {steps} étapes avec une récompense totale de {total_reward}.")

# Initialiser l'environnement
env = gym.make('Taxi-v3', render_mode="rgb_array")

# Charger les modèles
q_learning_model = load_model('../models/q_learning/q_learning_model.pkl')

# Exécuter et visualiser les modèles
print("Visualisation du modèle Q-Learning")
run_model(env, q_learning_model, episodes=1)

# Fermer l'environnement
env.close()
