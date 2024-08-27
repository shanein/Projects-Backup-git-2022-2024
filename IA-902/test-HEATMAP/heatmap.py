import gymnasium as gym
import numpy as np
import tqdm
import matplotlib.pyplot as plt
import time

render = None # 'human' for display, None for quick process
# env = gym.make('FrozenLake-v1',
#                 desc=None,
#                 map_name="4x4",
#                 is_slippery=False,
#                 # render_mode=render
#                 # on desactive le rendu pour accelerer l'apprentissage
#                 )
env = gym.make('CliffWalking-v0',
                 render_mode=render
                )
# env = gym.make('Taxi-v3',
#                 render_mode=render
#                 )

def prepare_ia() :
    n_a = env.action_space.n
    print(n_a)
    # n_a est le nombre d'actions possibles ici 4 a savoir haut, bas, gauche, droite

    n_o = env.observation_space.n
    print(n_o)
    # n_o est le nombre d'etats possibles ici 16 donc toutes les cases du jeu

    Q = np.zeros((n_o, n_a))
    print(Q)
    # Q est la matrice des valeurs d'actions, donc on initialise a 0

    rewards_history = []
    moves_history = []
    success_count = 0
    paths = []

    start_time = time.time()


    return Q, rewards_history, moves_history, success_count, start_time, paths

def q_learning(env, n_episodes, initial_lr, lr_decay, lr_min, initial_eps, eps_decay, eps_min, df):
    Q, rewards_history, moves_history, success_count, start_time, paths = prepare_ia()
    lr = initial_lr
    eps = initial_eps

    for episode in tqdm.tqdm(range(n_episodes)):
        state, _ = env.reset()
        total_reward = 0
        moves = 0
        terminated = False
        path = []
        while not terminated:
            action = get_greedy_action(Q, state, eps)
            new_state, reward, terminated, truncated, info = env.step(action)

            path.append(state)

            total_reward += reward
            moves += 1


            oldQValue = Q[state, action]
            maxFutureQValue = np.max(Q[new_state])
            newQValue = (1 - lr) * oldQValue + lr * (reward + df * maxFutureQValue)
            Q[state, action] = newQValue

            state = new_state
            if render :
                print(f"Q Learning : {episode}/{n_episodes}, Reward : {total_reward}")

        path.append(state)
        paths.append(path)
        rewards_history.append(total_reward)
        moves_history.append(moves)
        success_count += 1 if total_reward > 0 else 0

        # Variation de espilon et taux d'apprentissage (decay du parametre) + minimum pour eviter de depasser
        eps = max(eps * eps_decay, eps_min) # Réduction progressive de epsilon (exploration)
        lr = max(lr * lr_decay, lr_min) # Réduction progressive du taux d'apprentissage

    end_time = time.time()
    total_time = end_time - start_time

    performance_index = success_count / n_episodes

    return rewards_history, moves_history, total_time, performance_index, paths

def sarsa(env, n_episodes, initial_lr, lr_decay, lr_min, initial_eps, eps_decay, eps_min, df):
    Q, rewards_history, moves_history, success_count, start_time, paths = prepare_ia()
    lr = initial_lr
    eps = initial_eps

    for episode in tqdm.tqdm(range(n_episodes)):
        state, _ = env.reset()
        total_reward = 0
        moves = 0
        terminated = False
        path = []
        action = get_greedy_action(Q, state, eps)
        while not terminated:
            new_state, reward, terminated, truncated, info = env.step(action)
            new_action = get_greedy_action(Q, new_state, eps)

            path.append(state)

            total_reward += reward
            moves += 1

            oldQValue = Q[state, action]
            futureQValue = Q[new_state, new_action]
            newQValue = (1 - lr) * oldQValue + lr * (reward + df * futureQValue)
            Q[state, action] = newQValue

            state = new_state
            action = new_action
            if render :
                print(f"Sarsa : {episode}/{n_episodes}, Reward : {total_reward}")

        path.append(state)
        paths.append(path)
        rewards_history.append(total_reward)
        moves_history.append(moves)
        success_count += 1 if total_reward > 0 else 0

        eps = max(eps * eps_decay, eps_min)
        lr = max(lr * lr_decay, lr_min)

    end_time = time.time()
    total_time = end_time - start_time

    performance_index = success_count / n_episodes

    return rewards_history, moves_history, total_time, performance_index, paths

# get_greedy_action permet de choisir l'action a prendre, donc si on est en phase d'exploration, on prend une action aleatoire sinon on prend l'action qui a la plus grande valeure
def get_greedy_action(model, state, epsilon):
    explore = np.random.uniform(0, 1) < epsilon
    # on genere un nombre aleatoire entre 0 et 1, si ce nombre est inferieur a epsilon, on explore
    if explore:
        return env.action_space.sample()
    else:
        return np.argmax(model[state])

# Configurations de paramètres pour comparaison
configurations = [

    ###

    # "initial_lr" (learning rate) taux d'apprentissage initial, plus il est proche de 1, plus l'agent apprend vite
    # "lr_decay" Decroissance du learning rate, on essaie de garder en memoire progressivement et donc de moins en moins "apprendre"
    # "lr_min": Valeur minimale du learning rate pour ne pas stagner à 0 changement (peut etre 0 si souhaité)
    # "initial_eps": (Epsilon) Exploration, plus il est proche de 1, plus l'agent explore l'environnement
    # "eps_decay": Decroissance de epsilon, au fur et a mesure que l'agent apprend, on diminue l'exploration
    # "eps_min": Valeur minimale de epsilon pour ne pas stagner à 0 exploration (peut etre a 0 si souhaité)

    ###

    {"initial_lr": 0.1, "lr_decay": 0.995, "lr_min": 0.01, "initial_eps": 0.9, "eps_decay": 0.995, "eps_min": 0.1},
    # {"initial_lr": 0.1, "lr_decay": 0.999, "lr_min": 0.01, "initial_eps": 1.0, "eps_decay": 0.99, "eps_min": 0.1},
    # # {"initial_lr": 0.05, "lr_decay": 0.995, "lr_min": 0.01, "initial_eps": 0.8, "eps_decay": 0.99, "eps_min": 0.1},
    # {"initial_lr": 0.1, "lr_decay": 0.995, "lr_min": 0.01, "initial_eps": 0.8, "eps_decay": 0.995, "eps_min": 0.1},
    # {"initial_lr": 0.9, "lr_decay": 1, "lr_min": 0, "initial_eps": 0.9, "eps_decay": 1, "eps_min": 0}
]

# lr = 0.1
# # Mises à jour sont plus graduelles et moins d'aléatoire
# # lr = 0.9
# # lr est le taux d'apprentissage, donc plus il est proche de 1, plus l'agent apprend vite

# # df = 0.5
# # on le met a 0.5 pour que l'agent soit plus oriente vers la recompense immediate

# eps = 0.9
# # epsilon permet de controler l'exploration de l'agent, donc au fur et a mesure que l'agent apprend, on diminue l'exploration

# eps_min = 0.1  # Valeur minimum de epsilon
# eps_decay = 0.995  # Décroissance de epsilon

# lr_min = 0.01  # Valeur minimum du taux d'apprentissage
# lr_decay = 0.995  # Décroissance du taux d'apprentissage


n_episodes = 100
# n_episodes est le nombre d'episodes d'apprentissage

df = 0.99
# df est le facteur de reduction de la recompense future, donc plus il est proche de 1, plus l'agent est oriente vers la recompense future
# On fait desirer la récompense

results = []
results_q_learning = []
results_sarsa = []

#Lancement de toutes les configurations vers l'environnement
for config in configurations:
    rewards_history, moves_history, total_time, performance_index, paths = q_learning(
        env, n_episodes, config["initial_lr"], config["lr_decay"], config["lr_min"],
        config["initial_eps"], config["eps_decay"], config["eps_min"], df
    )
    results_q_learning.append({
        "config": config,
        "rewards_history": rewards_history,
        "moves_history": moves_history,
        "total_time": total_time,
        "performance_index": performance_index,
        "paths": paths
    })

    rewards_history, moves_history, total_time, performance_index, paths = sarsa(
        env, n_episodes, config["initial_lr"], config["lr_decay"], config["lr_min"],
        config["initial_eps"], config["eps_decay"], config["eps_min"], df
    )
    results_sarsa.append({
        "config": config,
        "rewards_history": rewards_history,
        "moves_history": moves_history,
        "total_time": total_time,
        "performance_index": performance_index,
        "paths": paths
    })

# Affichage des résultats
plt.figure(figsize=(20, 10))

# Graphiques pour Q-learning
for i, result in enumerate(results_q_learning):
    config = result["config"]
    plt.subplot(2, 4, i+1)
    plt.plot(result["rewards_history"]) #, label="Récompense par épisode"
    plt.xlabel('Épisodes')
    plt.ylabel('Récompense totale')
    plt.title(f"Q-Learning Config {i+1}\nLR: {config['initial_lr']}, LR Decay: {config['lr_decay']}\n"
              f"EPS: {config['initial_eps']}, EPS Decay: {config['eps_decay']}")
    plt.legend(loc='upper left')
    plt.grid(True)

# Graphiques pour SARSA
for i, result in enumerate(results_sarsa):
    config = result["config"]
    plt.subplot(2, 4, i+5)
    plt.plot(result["rewards_history"])
    plt.xlabel('Épisodes')
    plt.ylabel('Récompense totale')
    plt.title(f"SARSA Config {i+1}\nLR: {config['initial_lr']}, LR Decay: {config['lr_decay']}\n"
              f"EPS: {config['initial_eps']}, EPS Decay: {config['eps_decay']}")
    plt.legend(loc='upper left')
    plt.grid(True)



# Visualisation des chemins
grid_size = (4, 12)  # Taille de la grille pour CliffWalking-v0

heatmap_q_learning = np.zeros(grid_size)
heatmap_sarsa = np.zeros(grid_size)

for result in results_q_learning:
    for path in result['paths']:
        for state in path:
            row, col = divmod(state, grid_size[1])
            heatmap_q_learning[row, col] += 1

for result in results_sarsa:
    for path in result['paths']:
        for state in path:
            row, col = divmod(state, grid_size[1])
            heatmap_sarsa[row, col] += 1

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(heatmap_q_learning, cmap='hot', interpolation='nearest')
plt.title('Q-Learning Heatmap')
plt.colorbar()

plt.subplot(1, 2, 2)
plt.imshow(heatmap_sarsa, cmap='hot', interpolation='nearest')
plt.title('SARSA Heatmap')
plt.colorbar()
###

# Affichage des métriques supplémentaires pour Q-learning
for i, result in enumerate(results_q_learning):
    config = result["config"]
    last_fifth_start_index = int(n_episodes-n_episodes/5)
    last_fifth_reward = result['rewards_history'][last_fifth_start_index:n_episodes]
    last_fifth_moves = result['moves_history'][last_fifth_start_index:n_episodes]
    print(f"Q-Learning Config {i+1} - Performances:")
    print(f"  Learning Rate Initial: {config['initial_lr']}, Decay: {config['lr_decay']}, Min: {config['lr_min']}")
    print(f"  Epsilon Initial: {config['initial_eps']}, Decay: {config['eps_decay']}, Min: {config['eps_min']}")
    print(f"  Performance Index: {result['performance_index']:.4f}")
    print(f"  Total Time: {result['total_time']:.2f} seconds")
    print(f"  Average Reward: {np.mean(result['rewards_history']):.2f}")
    print(f"  Average Moves: {np.mean(result['moves_history']):.2f}")
    print(f"  Last 20% Average Reward: {np.mean(last_fifth_reward):.2f}")
    print(f"  Last 20% Average Moves: {np.mean(last_fifth_moves):.2f}")
    print("")

# Affichage des métriques supplémentaires pour SARSA
for i, result in enumerate(results_sarsa):
    config = result["config"]
    last_fifth_start_index = int(n_episodes-n_episodes/5)
    last_fifth_reward = result['rewards_history'][last_fifth_start_index:n_episodes]
    last_fifth_moves = result['moves_history'][last_fifth_start_index:n_episodes]
    print(f"SARSA Config {i+1} - Performances:")
    print(f"  Learning Rate Initial: {config['initial_lr']}, Decay: {config['lr_decay']}, Min: {config['lr_min']}")
    print(f"  Epsilon Initial: {config['initial_eps']}, Decay: {config['eps_decay']}, Min: {config['eps_min']}")
    print(f"  Performance Index: {result['performance_index']:.4f}")
    print(f"  Total Time: {result['total_time']:.2f} seconds")
    print(f"  Average Reward: {np.mean(result['rewards_history']):.2f}")
    print(f"  Average Moves: {np.mean(result['moves_history']):.2f}")
    print(f"  Last 20% Average Reward: {np.mean(last_fifth_reward):.2f}")
    print(f"  Last 20% Average Moves: {np.mean(last_fifth_moves):.2f}")
    print("")

plt.tight_layout(pad=3.0)
plt.show()



