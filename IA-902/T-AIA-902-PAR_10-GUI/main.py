import os

import gymnasium as gym
import numpy as np
import tqdm
import matplotlib.pyplot as plt
import time
from statistics import stdev
import pickle
import tkinter as tk
from tkinter import messagebox

from tktooltip import ToolTip

render = None # human for display, None for quick process
env = gym.make('Taxi-v3',
                render_mode=render
                )

n_a = env.action_space.n
print(n_a)
# n_a est le nombre d'actions possibles ici 4 a savoir haut, bas, gauche, droite

n_o = env.observation_space.n
print(n_o)
# n_o est le nombre d'etats possibles ici 16 donc toutes les cases du jeu


df = 0.99
# df est le facteur de reduction de la recompense future, donc plus il est proche de 1, plus l'agent est oriente vers la recompense future
# On fait desirer la récompense

results = []
results_q_learning = []
results_sarsa = []
results_dqn = []

# Create directories if they don't exist
os.makedirs('models/q_learning', exist_ok=True)
os.makedirs('models/sarsa', exist_ok=True)

save_path_q_learning = 'models/q_learning/q_learning_model.pkl'
save_path_sarsa = 'models/sarsa/sarsa_model.pkl'


#in minutes
# max_duration = 1
# nb_episode_stable_to_stop = 100
# #Relatif avec un taux d'amélioration
# value_gap_to_stop = 20

#Defines if the algo is still progressing or if we stop now
def is_learning(rewards_history, start_time) :
    if time.time() - start_time >= 60*max_duration :
        return False
    if len(rewards_history) > nb_episode_stable_to_stop :
        last_episodes = rewards_history[len(rewards_history)-nb_episode_stable_to_stop:len(rewards_history)]
        min(last_episodes)
        #if max(last_episodes) - min(last_episodes) <= value_gap_to_stop :
        if min(last_episodes) >= 0 and max(last_episodes) - min(last_episodes) <= value_gap_to_stop :
            return False
    return True


def prepare_ia():
    Q = np.zeros((n_o, n_a))
    # Q est la matrice des valeurs d'actions, donc on initialise a 0

    rewards_history = []
    moves_history = []
    success_count = 0

    start_time = time.time()

    return Q, rewards_history, moves_history, success_count, start_time

def get_end_results(results) :
    end = results[len(results)-nb_episode_stable_to_stop:len(results)]
    return max(end), min(end), sum(end)/len(end), stdev(end)


def q_learning(env, initial_lr, lr_decay, lr_min, initial_eps, eps_decay, eps_min, df, save_path=None):
    Q, rewards_history, moves_history, success_count, start_time = prepare_ia()
    lr = initial_lr
    eps = initial_eps
    episode = 0

    while is_learning(rewards_history, start_time):
        episode += 1
        state, _ = env.reset()
        total_reward = 0
        moves = 0
        terminated = False
        while not terminated:
            action = get_greedy_action(Q, state, eps)
            new_state, reward, terminated, truncated, info = env.step(action)

            total_reward += reward
            moves += 1


            oldQValue = Q[state, action]
            maxFutureQValue = np.max(Q[new_state])
            newQValue = (1 - lr) * oldQValue + lr * (reward + df * maxFutureQValue)
            Q[state, action] = newQValue

            state = new_state
            if render :
                print(f"Q Learning : {episode}, Reward : {total_reward}")

        rewards_history.append(total_reward)
        moves_history.append(moves)
        success_count += 1 if total_reward > 0 else 0

        # Variation de espilon et taux d'apprentissage (decay du parametre) + minimum pour eviter de depasser
        eps = max(eps * eps_decay, eps_min) # Réduction progressive de epsilon (exploration)
        lr = max(lr * lr_decay, lr_min) # Réduction progressive du taux d'apprentissage

    end_time = time.time()
    total_time = end_time - start_time
    max_val, min_val, avg, std_dev = get_end_results(rewards_history)
    print(f"Q_LEARNING : Total episodes : {episode}, MAX : {max_val}, MIN : {min_val}, AVG : {avg}, STD_DEV : {std_dev}, TIME : {round(total_time,2)}s")
    performance_index = success_count / episode

    # Sauvegarder le modèle Q-learning
    if save_path:
        with open(save_path, 'wb') as f:
            pickle.dump(Q, f)
        print(f"Modèle sauvegardé sous {save_path}")

    return rewards_history, moves_history, total_time, performance_index

def sarsa(env, initial_lr, lr_decay, lr_min, initial_eps, eps_decay, eps_min, df, save_path=None):
    Q, rewards_history, moves_history, success_count, start_time = prepare_ia()
    lr = initial_lr
    eps = initial_eps

    episode = 0
    while is_learning(rewards_history, start_time):
        episode += 1
        state, _ = env.reset()
        total_reward = 0
        moves = 0
        terminated = False
        action = get_greedy_action(Q, state, eps)
        while not terminated:
            new_state, reward, terminated, truncated, info = env.step(action)
            new_action = get_greedy_action(Q, new_state, eps)

            total_reward += reward
            moves += 1

            oldQValue = Q[state, action]
            futureQValue = Q[new_state, new_action]
            newQValue = (1 - lr) * oldQValue + lr * (reward + df * futureQValue)
            Q[state, action] = newQValue

            state = new_state
            action = new_action
            if render :
                print(f"Sarsa : {episode}, Reward : {total_reward}")

        rewards_history.append(total_reward)
        moves_history.append(moves)
        success_count += 1 if total_reward > 0 else 0

        eps = max(eps * eps_decay, eps_min)
        lr = max(lr * lr_decay, lr_min)

    end_time = time.time()
    total_time = end_time - start_time
    max_val, min_val, avg, std_dev = get_end_results(rewards_history)
    print(f"SARSA : Total episodes : {episode}, MAX : {max_val}, MIN : {min_val}, AVG : {avg}, STD_DEV : {std_dev}, TIME : {round(total_time,2)}s")
    performance_index = success_count / episode


    # Sauvegarder le modèle Sarsa
    if save_path:
        with open(save_path, 'wb') as f:
            pickle.dump(Q, f)
        print(f"Modèle sauvegardé sous {save_path}")

    return rewards_history, moves_history, total_time, performance_index

# get_greedy_action permet de choisir l'action a prendre, donc si on est en phase d'exploration, on prend une action aleatoire sinon on prend l'action qui a la plus grande valeure
def get_greedy_action(model, state, epsilon):
    explore = np.random.uniform(0, 1) < epsilon
    # on genere un nombre aleatoire entre 0 et 1, si ce nombre est inferieur a epsilon, on explore
    if explore:
        return env.action_space.sample()
    else:
        return np.argmax(model[state])

def train_model(configurations):
    #Lancement de toutes les configurations vers l'environnement
    for config in tqdm.tqdm(configurations):
        rewards_history, moves_history, total_time, performance_index = q_learning(
            env, config["initial_lr"], config["lr_decay"], config["lr_min"],
            config["initial_eps"], config["eps_decay"], config["eps_min"], df,
            save_path=save_path_q_learning
        )
        results_q_learning.append({
            "config": config,
            "rewards_history": rewards_history,
            "moves_history": moves_history,
            "total_time": total_time,
            "performance_index": performance_index
        })

        rewards_history, moves_history, total_time, performance_index = sarsa(
            env, config["initial_lr"], config["lr_decay"], config["lr_min"],
            config["initial_eps"], config["eps_decay"], config["eps_min"], df,
            save_path=save_path_sarsa
        )
        results_sarsa.append({
            "config": config,
            "rewards_history": rewards_history,
            "moves_history": moves_history,
            "total_time": total_time,
            "performance_index": performance_index
        })

    # Affichage des résultats
    plt.figure(figsize=(20, 10))

    def get_graph_limit(results) :
        mean_results = results[round(len(results)/3):len(results)]
        return min(mean_results), max(mean_results)

    # Graphiques pour Q-learning
    for i, result in enumerate(results_q_learning):
        config = result["config"]
        plt.subplot(2, 4, i*2+1)
        plt.plot(result["rewards_history"]) #, label="Récompense par épisode"
        plt.xlabel('Épisodes')
        plt.ylabel('Récompense totale')
        #plt.ylim(get_graph_limit(result["rewards_history"]))
        plt.title(f"Q-Learning Config {i+1}\nLR: {config['initial_lr']}, LR Decay: {config['lr_decay']}\n"
                  f"EPS: {config['initial_eps']}, EPS Decay: {config['eps_decay']}")
        plt.legend(loc='upper left')
        plt.grid(True)

        rewards = result["rewards_history"][len(result["rewards_history"])-nb_episode_stable_to_stop:len(result["rewards_history"])]
        plt.subplot(2, 4, i*2+2)
        plt.plot(rewards) #, label="Récompense par épisode"
        plt.xlabel('Épisodes')
        plt.ylabel('Récompense totale')
        plt.title(f"Q-Learning Config {i+1} end\nLR: {config['initial_lr']}, LR Decay: {config['lr_decay']}\n"
                  f"EPS: {config['initial_eps']}, EPS Decay: {config['eps_decay']}")
        plt.legend(loc='upper left')
        plt.grid(True)

    # Graphiques pour SARSA
    for i, result in enumerate(results_sarsa):
        config = result["config"]
        plt.subplot(2, 4, i*2+5)
        plt.plot(result["rewards_history"], color="red")
        plt.xlabel('Épisodes')
        plt.ylabel('Récompense totale')
        #plt.ylim(get_graph_limit(result["rewards_history"]))
        plt.title(f"SARSA Config {i+1}\nLR: {config['initial_lr']}, LR Decay: {config['lr_decay']}\n"
                  f"EPS: {config['initial_eps']}, EPS Decay: {config['eps_decay']}")
        plt.legend(loc='upper left')
        plt.grid(True)

        rewards = result["rewards_history"][len(result["rewards_history"])-nb_episode_stable_to_stop:len(result["rewards_history"])]
        plt.subplot(2, 4, i*2+6)
        plt.plot(rewards, color="red") #, label="Récompense par épisode"
        plt.xlabel('Épisodes')
        plt.ylabel('Récompense totale')
        plt.title(f"SARSA Config {i+1} end\nLR: {config['initial_lr']}, LR Decay: {config['lr_decay']}\n"
                  f"EPS: {config['initial_eps']}, EPS Decay: {config['eps_decay']}")
        plt.legend(loc='upper left')
        plt.grid(True)

    # Affichage des métriques supplémentaires pour Q-learning
    for i, result in enumerate(results_q_learning):
        nb_episodes = len(result["rewards_history"])
        config = result["config"]
        last_fifth_start_index = int(nb_episodes-nb_episodes/5)
        last_fifth_reward = result['rewards_history'][last_fifth_start_index:nb_episodes]
        last_fifth_moves = result['moves_history'][last_fifth_start_index:nb_episodes]
        print(f"Q-Learning Config {i+1} - Performances:")
        print(f"  Learning Rate Initial: {config['initial_lr']}, Decay: {config['lr_decay']}, Min: {config['lr_min']}")
        print(f"  Epsilon Initial: {config['initial_eps']}, Decay: {config['eps_decay']}, Min: {config['eps_min']}")
        print(f"  Performance Index: {result['performance_index']:.4f}")
        print(f"  Total Time: {result['total_time']:.2f} seconds")
        print(f"  Average Reward: {np.mean(result['rewards_history']):.2f}")
        print(f"  Reward Standard Deviation: {np.std(result['rewards_history']):.2f}")
        print(f"  Average Moves: {np.mean(result['moves_history']):.2f}")
        print(f"  Last 20% Average Reward: {np.mean(last_fifth_reward):.2f}")
        print(f"  Last 20% Reward Standard Deviation: {np.std(last_fifth_reward):.2f}")
        print(f"  Last 20% Average Moves: {np.mean(last_fifth_moves):.2f}")
        print("")

    # Affichage des métriques supplémentaires pour SARSA
    for i, result in enumerate(results_sarsa):
        nb_episodes = len(result["rewards_history"])
        config = result["config"]
        last_fifth_start_index = int(nb_episodes-nb_episodes/5)
        last_fifth_reward = result['rewards_history'][last_fifth_start_index:nb_episodes]
        last_fifth_moves = result['moves_history'][last_fifth_start_index:nb_episodes]
        print(f"SARSA Config {i+1} - Performances:")
        print(f"  Learning Rate Initial: {config['initial_lr']}, Decay: {config['lr_decay']}, Min: {config['lr_min']}")
        print(f"  Epsilon Initial: {config['initial_eps']}, Decay: {config['eps_decay']}, Min: {config['eps_min']}")
        print(f"  Performance Index: {result['performance_index']:.4f}")
        print(f"  Total Time: {result['total_time']:.2f} seconds")
        print(f"  Average Reward: {np.mean(result['rewards_history']):.2f}")
        print(f"  Reward Standard Deviation: {np.std(result['rewards_history']):.2f}")
        print(f"  Average Moves: {np.mean(result['moves_history']):.2f}")
        print(f"  Last 20% Average Reward: {np.mean(last_fifth_reward):.2f}")
        print(f"  Last 20% Reward Standard Deviation: {np.std(last_fifth_reward):.2f}")
        print(f"  Last 20% Average Moves: {np.mean(last_fifth_moves):.2f}")
        print("")

    plt.tight_layout(pad=3.0)
    plt.show()
def start_function():
    global max_duration, nb_episode_stable_to_stop, value_gap_to_stop
    # Récupérer les valeurs des entrées
    try:
        initial_lr = float(entry_initial_lr.get())
        lr_decay = float(entry_lr_decay.get())
        lr_min = float(entry_lr_min.get())
        initial_eps = float(entry_initial_eps.get())
        eps_decay = float(entry_eps_decay.get())
        eps_min = float(entry_eps_min.get())

        max_duration = int(entry_max_duration.get())
        nb_episode_stable_to_stop = int(entry_nb_episode_stable_to_stop.get())
        value_gap_to_stop = float(entry_value_gap_to_stop.get())

        # Validation des valeurs
        if not (0 <= initial_lr <= 1 and 0 <= lr_decay <= 1 and 0 <= lr_min <= 1):
            raise ValueError("Les valeurs de initial_lr, lr_decay, et lr_min doivent être entre 0 et 1.")
        if not (0 <= initial_eps <= 1 and 0 <= eps_decay <= 1 and 0 <= eps_min <= 1):
            raise ValueError("Les valeurs de initial_eps, eps_decay, et eps_min doivent être entre 0 et 1.")

        configurations = [
            {"initial_lr": initial_lr, "lr_decay": lr_decay, "lr_min": lr_min, "initial_eps": initial_eps, "eps_decay": eps_decay, "eps_min": eps_min},
        ]

        # In minutes
        train_model(configurations)

    except ValueError as e:
        messagebox.showerror("Erreur de saisie", str(e))


# Création de la fenêtre principale
root = tk.Tk()
root.title("TaxiDriver")

# Titre
title_label = tk.Label(root, text="TaxiDriver", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Description
description_label = tk.Label(root, text="Description brève de TaxiDriver\n Ajustez les configurations et cliquez sur 'Lancer'")
description_label.pack(pady=10)

# Taille tkinter
window_width = 700
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Centre les boutons verticalement et horizontalement
frame = tk.Frame(root)

# Cadre pour le formulaire
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

config_labels = [
    "initial_lr (learning rate):",
    "lr_decay:",
    "lr_min:",
    "initial_eps (Epsilon):",
    "eps_decay:",
    "eps_min:"
]

config_tooltips = [
    "Taux d'apprentissage initial. Plus il est proche de 1, plus l'agent apprend vite.",
    "Décroissance du learning rate. Diminue progressivement.",
    "Valeur minimale du learning rate pour éviter de stagner à 0.",
    "Exploration initiale. Plus elle est proche de 1, plus l'agent explore.",
    "Décroissance de epsilon. Diminue l'exploration à mesure que l'agent apprend.",
    "Valeur minimale de epsilon pour éviter de stagner à 0 exploration."
]


config_defaults = [
    0.1,  # Default initial_lr
    0.999,  # Default lr_decay
    0.01,  # Default lr_min
    1.0,  # Default initial_eps
    0.999,  # Default eps_decay
    0.01  # Default eps_min
]

for i, (text, tooltip, default) in enumerate(zip(config_labels, config_tooltips, config_defaults)):
    label = tk.Label(form_frame, text=text, justify="left")
    if tooltip:
        ToolTip(label, msg=tooltip)
    label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
    entry = tk.Entry(form_frame)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entry.insert(0, default)

entry_initial_lr, entry_lr_decay, entry_lr_min, entry_initial_eps, entry_eps_decay, entry_eps_min = [
    form_frame.grid_slaves(row=i, column=1)[0] for i in range(6)]

separator = tk.Label(form_frame, text="", pady=10)
separator.grid(row=len(config_labels), column=0, columnspan=2)

# Valeurs par défaut pour les paramètres additionnels
max_duration_default = 1
nb_episode_stable_to_stop_default = 100
value_gap_to_stop_default = 20

# Champs pour les paramètres additionnels
additional_params_labels = [
    "Max Duration (minutes):",
    "Nombre d'épisodes stables avant arrêt:",
    "Valeur de gap pour arrêter:"
]

additional_params_defaults = [
    max_duration_default,
    nb_episode_stable_to_stop_default,
    value_gap_to_stop_default
]

additional_params_entries = []

for i, (text, default_value) in enumerate(zip(additional_params_labels, additional_params_defaults)):
    label = tk.Label(form_frame, text=text, justify="left")
    label.grid(row=len(config_labels) + i, column=0, sticky="w", padx=5, pady=5)
    entry = tk.Entry(form_frame)
    entry.grid(row=len(config_labels) + i, column=1, padx=5, pady=5)
    entry.insert(0, default_value)
    additional_params_entries.append(entry)

entry_max_duration, entry_nb_episode_stable_to_stop, entry_value_gap_to_stop = additional_params_entries

# Bouton pour lancer la fonction
start_button = tk.Button(root, text="Lancer", command=start_function)
start_button.pack(pady=10)

# Lancement de la boucle principale
root.mainloop()

# # Configurations de paramètres pour comparaison
# configurations = [
#
#     ###
#
#     # "initial_lr" (learning rate) taux d'apprentissage initial, plus il est proche de 1, plus l'agent apprend vite
#     # "lr_decay" Decroissance du learning rate, on essaie de garder en memoire progressivement et donc de moins en moins "apprendre"
#     # "lr_min": Valeur minimale du learning rate pour ne pas stagner à 0 changement (peut etre 0 si souhaité)
#     # "initial_eps": (Epsilon) Exploration, plus il est proche de 1, plus l'agent explore l'environnement
#     # "eps_decay": Decroissance de epsilon, au fur et a mesure que l'agent apprend, on diminue l'exploration
#     # "eps_min": Valeur minimale de epsilon pour ne pas stagner à 0 exploration (peut etre a 0 si souhaité)
#
#     ###
#
#     {"initial_lr": 0.1, "lr_decay": 0.999, "lr_min": 0.01, "initial_eps": 1.0, "eps_decay": 0.999, "eps_min": 0.01},
# ]
#
#

#
#
# train_model(configurations)