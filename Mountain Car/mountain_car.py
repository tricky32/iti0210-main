import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

# ------------------------
# Hyperparameters (Adjust as needed)
# ------------------------
alpha = 0.1
gamma = 0.95
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.995
episodes = 50000
max_steps = 200

# ------------------------
# State Discretization
# ------------------------
num_pos_bins = 20
num_vel_bins = 20
pos_space = np.linspace(-1.2, 0.6, num_pos_bins)
vel_space = np.linspace(-0.07, 0.07, num_vel_bins)

def discretize_state(obs):
    pos, vel = obs
    pos_bin = np.digitize(pos, pos_space) - 1
    vel_bin = np.digitize(vel, vel_space) - 1
    # clip values to ensure indices are within range
    pos_bin = min(num_pos_bins - 1, max(0, pos_bin))
    vel_bin = min(num_vel_bins - 1, max(0, vel_bin))
    return (pos_bin, vel_bin)

# ------------------------
# Q-table Initialization
# ------------------------
q_table = np.zeros((num_pos_bins, num_vel_bins, 3)) # 3 actions: left (0), no acc (1), right (2)

def choose_action(state, epsilon):
    if np.random.random() < epsilon:
        return np.random.randint(0, 3) # random action
    else:
        return np.argmax(q_table[state[0], state[1], :])

env = gym.make("MountainCar-v0") 
rewards_all_episodes = []
max_positions_all_episodes = []
steps_all_episodes = []

# ------------------------
# Training Loop
# ------------------------
for ep in range(episodes):
    obs, info = env.reset()
    state = discretize_state(obs)
    total_reward = 0
    max_position = -1.2
    steps = 0

    for step in range(max_steps):
        action = choose_action(state, epsilon)
        next_obs, reward, terminated, truncated, info = env.step(action)

        # Optional reward shaping: encourage reaching new max positions
        if next_obs[0] > max_position:
            max_position = next_obs[0]
            reward += 0.02

        next_state = discretize_state(next_obs)

        # Q-learning update
        max_future_q = np.max(q_table[next_state[0], next_state[1], :])
        current_q = q_table[state[0], state[1], action]
        new_q = current_q + alpha * (reward + gamma * max_future_q - current_q)
        q_table[state[0], state[1], action] = new_q

        state = next_state
        total_reward += reward
        steps += 1

        if terminated or truncated:
            break

    rewards_all_episodes.append(total_reward)
    max_positions_all_episodes.append(max_position)
    steps_all_episodes.append(steps)

    # Decay epsilon
    if epsilon > epsilon_min:
        epsilon *= epsilon_decay

    # Print occasional progress updates
    if (ep+1) % 1000 == 0:
        avg_reward = np.mean(rewards_all_episodes[-1000:])
        print(f"Episode {ep+1}, Average Reward (last 1000): {avg_reward:.2f}")

env.close()

# ------------------------
# Plotting the Results on One Page
# ------------------------
def moving_average(data, window_size=100):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

smoothed_rewards = moving_average(rewards_all_episodes)

plt.figure(figsize=(12, 9))

# Subplot 1: Average Rewards Over Time
plt.subplot(3, 1, 1)
plt.plot(smoothed_rewards, label="Average Rewards (Smoothed)")
plt.title("Training Progress")
plt.xlabel("Episode")
plt.ylabel("Average Reward (per 100 episodes)")
plt.legend()

# Subplot 2: Max X Position Each Episode
plt.subplot(3, 1, 2)
plt.plot(max_positions_all_episodes, label="Max X Position")
plt.xlabel("Episode")
plt.ylabel("Max X Position")
plt.legend()

# Subplot 3: Episode Length (Steps) Over Time
plt.subplot(3, 1, 3)
plt.plot(steps_all_episodes, label="Steps per Episode")
plt.xlabel("Episode")
plt.ylabel("Steps")
plt.legend()

plt.tight_layout()
plt.show()

# ------------------------
# Watching the Trained Agent in a Loop
# ------------------------
env = gym.make("MountainCar-v0", render_mode="human")

while True:
    obs, info = env.reset()
    done = False
    while not done:
        state = discretize_state(obs)
        action = np.argmax(q_table[state[0], state[1], :])
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

env.close()
