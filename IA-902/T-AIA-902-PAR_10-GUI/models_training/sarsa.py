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
