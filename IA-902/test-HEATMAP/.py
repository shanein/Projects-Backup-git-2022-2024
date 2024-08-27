import gymnasium as gym
import numpy as np
import tqdm
import matplotlib.pyplot as plt
import time

render = None  # 'human' for display, None for quick process

env = gym.make('CliffWalking-v0', render_mode=render)


def prepare_ia():
    n_a = env.action_space.n
    print(n_a)

    n_o = env.observation_space.n
    print(n_o)

    Q = np.zeros((n_o, n_a))
    print(Q)

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
            if render:
                print(f"Q Learning : {episode}/{n_episodes}, Reward : {total_reward}")

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
            if render:
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


def get_greedy_action(model, state, epsilon):
    explore = np.random.uniform(0, 1) < epsilon
    if explore:
        return env.action_space.sample()
    else:
        return np.argmax(model[state])


configurations = [
    {"initial_lr": 0.1, "lr_decay": 0.995, "lr_min": 0.01, "initial_eps": 0.9, "eps_decay": 0.995, "eps_min": 0.1},
    # {"initial_lr": 0.1, "lr_decay": 0.999, "lr_min": 0.01, "initial_eps": 1.0, "eps_decay": 0.99, "eps_min": 0.1},
    # {"initial_lr": 0.1, "lr_decay": 0.995, "lr_min": 0.01, "initial_eps": 0.8, "eps_decay": 0.995, "eps_min": 0.1},
    # {"initial_lr": 0.9, "lr_decay": 1, "lr_min": 0, "initial_eps": 0.9, "eps_decay": 1, "eps_min": 0}
]

n_episodes = 100
df = 0.99

results_q_learning = []
results_sarsa = []

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

plt.figure(figsize=(20, 10))

for i, result in enumerate(results_q_learning):
    config = result["config"]
    plt.subplot(2, 4, i + 1)
    plt.plot(result["rewards_history"])
    plt.xlabel('Épisodes')
    plt.ylabel('Récompense totale')
    plt.title(f"Q-Learning Config {i + 1}\nLR: {config['initial_lr']}, LR Decay: {config['lr_decay']}\n"
              f"EPS: {config['initial_eps']}, EPS Decay: {config['eps_decay']}")
    plt.grid(True)

for i, result in enumerate(results_sarsa):
    config = result["config"]
    plt.subplot(2, 4, i + 5)
    plt.plot(result["rewards_history"])
    plt.xlabel('Épisodes')
    plt.ylabel('Récompense totale')
    plt.title(f"SARSA Config {i + 1}\nLR: {config['initial_lr']}, LR Decay: {config['lr_decay']}\n"
              f"EPS: {config['initial_eps']}, EPS Decay: {config['eps_decay']}")
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

plt.show()
