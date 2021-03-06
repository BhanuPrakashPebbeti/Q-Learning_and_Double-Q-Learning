import os
import gym
import pickle
import numpy as np
import matplotlib.pyplot as plt

env = gym.make("Pendulum-v1")

ROOT_DIR = os.path.dirname(__file__)
LOAD_PRETRAINED = True
VALIDATING = True
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 150000
SHOW_EVERY = 10000
STATS_EVERY = 100
epsilon = 1
EPSILON_THRESHOLD = 0.1
epsilon_decay_value = 0.99999

# Making discrete action space
DISCRETE_ACTION_SPACE_SIZE = 17
discrete_action_space_win_size = (env.action_space.high - env.action_space.low) / (DISCRETE_ACTION_SPACE_SIZE - 1)
action_space = {}
for i in range(DISCRETE_ACTION_SPACE_SIZE):
    action_space[i] = [env.action_space.low[0] + (i * discrete_action_space_win_size[0])]

# # Making discrete observation space
DISCRETE_OS_SIZE = [21, 21, 65]
discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / [i - 1 for i in DISCRETE_OS_SIZE]
if LOAD_PRETRAINED:
    q1_table = np.load(os.path.realpath(os.path.join(ROOT_DIR, 'q1table.npy')))
    q2_table = np.load(os.path.realpath(os.path.join(ROOT_DIR, 'q2table.npy')))
else:
    q1_table = np.random.uniform(low = -2, high = -0, size = (DISCRETE_OS_SIZE + [DISCRETE_ACTION_SPACE_SIZE]))
    q2_table = np.random.uniform(low = -2, high = -0, size = (DISCRETE_OS_SIZE + [DISCRETE_ACTION_SPACE_SIZE]))
ep_rewards = []
aggr_ep_rewards = {'ep': [], 'avg': [], 'max': [], 'min': []}


def get_discrete_state(state):
    ds = (state - env.observation_space.low) / discrete_os_win_size
    return tuple(ds.astype(np.int32))


if VALIDATING:
    epsilon = 0
    SHOW_EVERY = 1


def maxAction(state):
    values = np.add(q1_table[state], q2_table[state])
    action = np.argmax(values)
    return action


for episode in range(EPISODES):
    episode_reward = 0
    discrete_state = get_discrete_state(env.reset())
    done = False

    if episode % SHOW_EVERY == 0:
        render = True
    else:
        render = False
    while not done:
        if np.random.random() > epsilon:
            # Get action from Q tables
            action = maxAction(discrete_state)
        else:
            # Get random action
            action = np.random.randint(0, DISCRETE_ACTION_SPACE_SIZE)
        torque = action_space[action]
        new_state, reward, done, _ = env.step(torque)
        episode_reward += reward
        new_discrete_state = get_discrete_state(new_state)
        if episode % SHOW_EVERY == 0:
            env.render()
        if not VALIDATING:
            if not done:
                if np.random.random() <= 0.5:
                    action_ = np.argmax(q1_table[new_discrete_state])
                    # And here's our equation for a new Q value for current state and action
                    new_q = (1 - LEARNING_RATE) * q1_table[discrete_state + (action,)] + LEARNING_RATE * (
                                reward + DISCOUNT * q2_table[new_discrete_state + (action_,)])
                    # Update Q table with new Q value
                    q1_table[discrete_state + (action,)] = new_q

                else:
                    action_ = np.argmax(q2_table[new_discrete_state])
                    # And here's our equation for a new Q value for current state and action
                    new_q = (1 - LEARNING_RATE) * q2_table[discrete_state + (action,)] + LEARNING_RATE * (
                            reward + DISCOUNT * q1_table[new_discrete_state + (action_,)])
                    # Update Q table with new Q value
                    q2_table[discrete_state + (action,)] = new_q

            if new_state[0] == 0 and new_state[1] == 1:
                q1_table[discrete_state + (action,)] = 0
                q2_table[discrete_state + (action,)] = 0
                print(f"Acheived in {episode}")

        discrete_state = new_discrete_state
    if not VALIDATING:
        # Decaying is being done every episode if episode number is within decaying range
        if epsilon >= EPSILON_THRESHOLD:
            epsilon *= epsilon_decay_value
        ep_rewards.append(episode_reward)
        if not episode % STATS_EVERY:
            average_reward = sum(ep_rewards[-STATS_EVERY:]) / STATS_EVERY
            aggr_ep_rewards['ep'].append(episode)
            aggr_ep_rewards['avg'].append(average_reward)
            aggr_ep_rewards['max'].append(max(ep_rewards[-STATS_EVERY:]))
            aggr_ep_rewards['min'].append(min(ep_rewards[-STATS_EVERY:]))
            print(f'Episode: {episode:>5d}, average reward: {average_reward:>4.1f}, current epsilon: {epsilon:>1.2f}')
        if episode % 10 == 0:
            np.save(os.path.realpath(os.path.join(ROOT_DIR, 'q1table.npy')), q1_table)
            np.save(os.path.realpath(os.path.join(ROOT_DIR, 'q2table.npy')), q2_table)

env.close()

if not VALIDATING:
    filehandler = open("statistics", 'wb')
    pickle.dump(aggr_ep_rewards, filehandler)

    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label = "average rewards")
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label = "max rewards")
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label = "min rewards")
    plt.legend(loc = 4)
    plt.savefig(os.path.realpath(os.path.join(ROOT_DIR, "Statistics.png")))
    plt.show()
