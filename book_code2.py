import numpy as np
import random

class Bandit:
    def __init__(self, arms=10): #arms = number of slotmachine
        self.rates = np.random.rand(arms) #각 슬롯머신의 승률 설정, 0과 1 사이의 무작위 값을 선택함,
                                          #10 random values between of 0 to 1 are given
    def play(self, arm):
        rate = self.rates[arm] #bring 'n' th rate of rates list
        if rate > np.random.rand(): #decide if the random number is bigger than the slot machines rates
            return 1
        else:
            return 0

bandit = Bandit()
for i in range(3):
    print(bandit.play(0))

#making agent
Q = 0

for n in range(1, 11): #play 10 times
    reward = bandit.play(0) #play 0th slot machine
    Q += (reward - Q) / n #renew value prediction Q is prediction of actions outcome.
    print(Q)

Qs = np.zeros(10) #value prediction of each slotmachine
ns = np.zeros(10) #play count of each slotmachine

for n in range(10):
    action = np.random.randint(0, 10) #random action
    reward = bandit.play(action) #play [action]th slot machine

    ns[action] += 1
    Qs[action] += (reward - Qs[action] / ns[action])
    print(Qs)

class Agent:
    def __init__(self, epsilon, action_size=10):
        self.epsilon = epsilon #random action probability
        self.Qs = np.zeros(action_size)
        self.ns = np.zeros(action_size)

    def update(self, action, reward): #slot machine value prediction
        self.ns[action] += 1 #increese play count of 'n' th slotmachine
        self.Qs[action] += (reward - self.Qs[action]) / self.ns[action]

    def get_action(self): #choosing action
        if np.random.rand() < self.epsilon: #epsilon is 0.1, which is 10 percent. so for 10 percent of the time it chooses random action.
            return np.random.randint(0, len(self.Qs)) #random action select
        return np.argmax(self.Qs) #greed action selection, returns the index location value of the biggest value

import matplotlib.pyplot as plt
'''
steps = 1000
epsilon = 0.1

bandit = Bandit()
agent = Agent(epsilon)
total_reward = 0
total_rewards = []
rates = []

for step in range(steps):
    action = agent.get_action() #select action
    reward = bandit.play(action) #play and get reward
    agent.update(action, reward) #learn
    total_reward += reward

    total_rewards.append(total_reward) #total of current rewards
    rates.append(total_reward / steps + 1) #save current win rates

plt.plot(total_reward)

plt.ylabel('Total_Reward')
plt.xlabel('Steps')
plt.plot(total_rewards)
plt.show()

plt.ylabel("Rates")
plt.xlabel("Steps")
plt.plot(rates)
plt.show()
'''
runs = 200
steps = 1000
epsilon = 0.1
all_rates = np.zeros((runs, steps)) #shape of 200 * 1000

for run in range(runs): # 200 times of total test
    bandit = Bandit()
    agent = Agent(epsilon)
    total_reward = 0
    rates = []
    for step in range(steps):
        action = agent.get_action()
        reward = bandit.play(action)
        agent.update(action, reward)
        total_reward += reward
        rates.append(total_reward / (steps + 1))

    all_rates[run] = rates # record

avg_rates1 = np.average(all_rates, axis=0) #record average of each experiment

print(avg_rates1)

runs = 200
steps = 1000
epsilon = 0.2
all_rates = np.zeros((runs, steps)) #shape of 200 * 1000

for run in range(runs): # 200 times of total test
    bandit = Bandit()
    agent = Agent(epsilon)
    total_reward = 0
    rates = []
    for step in range(steps):
        action = agent.get_action()
        reward = bandit.play(action)
        agent.update(action, reward)
        total_reward += reward
        rates.append(total_reward / (steps + 1))

    all_rates[run] = rates # record

avg_rates2 = np.average(all_rates, axis=0) #record average of each experiment

print(avg_rates2)

runs = 200
steps = 1000
epsilon = 0.8
all_rates = np.zeros((runs, steps)) #shape of 200 * 1000

for run in range(runs): # 200 times of total test
    bandit = Bandit()
    agent = Agent(epsilon)
    total_reward = 0
    rates = []
    for step in range(steps):
        action = agent.get_action()
        reward = bandit.play(action)
        agent.update(action, reward)
        total_reward += reward
        rates.append(total_reward / (steps + 1))

    all_rates[run] = rates # record

avg_rates3 = np.average(all_rates, axis=0) #record average of each experiment

print(avg_rates3)

plt.ylabel('Rates')
plt.xlabel('Steps')
plt.plot(avg_rates1, color='red', label='Average Reward1')
plt.plot(avg_rates2, color='blue', label='Average Reward2')
plt.plot(avg_rates3, color='green', label='Average Reward3')
plt.legend()
plt.show()

#non_stationary(비정상 문제)

class NonStatBandit:
    def __init__(self, arms=10): #arms = number of slotmachine
        self.arms = arms
        self.rates = np.random.rand(arms) #각 슬롯머신의 승률 설정, 0과 1 사이의 무작위 값을 선택함,
                                          #10 random values between of 0 to 1 are given
    def play(self, arm):
        rate = self.rates[arm] #bring 'n' th rate of rates list
        self.rates += 0.1 * np.random.randn(self.arms) #add noise to change the actual win rate
        if rate > np.random.rand(): #decide if the random number is bigger than the slot machines rates
            return 1
        else:
            return 0

class AlphaAgent:
    def __init__(self, epsilon, alpha, actions=10):
        self.epsilon = epsilon
        self.Qs = np.zeros(actions)
        self.alpha = alpha #fixed value A

    def update(self, action, reward):
            self.Qs[action] += (reward - self.Qs[action]) * self.alpha

    def get_action(self):
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, len(self.Qs))
        return np.argmax(self.Qs)

alpha = 0.8

for run in range(runs):
    bandit = NonStatBandit()
    agent = Agent(epsilon)
    total_reward = 0
    rates = []
    for step in range(steps):
        action = agent.get_action()
        reward = bandit.play(action)
        total_reward += reward
        rates.append(total_reward / (steps + 1))

    all_rates[run] = rates  # record

avg_rates1 = np.average(all_rates, axis=0)

for run in range(runs):
    bandit = NonStatBandit()
    agent = AlphaAgent(epsilon, alpha)
    total_reward = 0
    rates = []
    for step in range(steps):
        action = agent.get_action()
        reward = bandit.play(action)
        total_reward += reward
        rates.append(total_reward / (steps + 1))

    all_rates[run] = rates  # record

avg_rates2 = np.average(all_rates, axis=0)

plt.xlabel('Steps')
plt.ylabel('Rates')
plt.plot(avg_rates1, color='red', label='Agent')
plt.plot(avg_rates2, color='blue', label='Alpha Agent')
plt.legend()
plt.show()

class GridWorld:
    def __init__(self):
        self.action_space = [0, 1, 2, 3]
        self.acting_meaning = {
            0:'up', 1:'down', 2:'right', 3:'left'
        }
        self.reward_map = np.array(
            [[0, 0, 0, 1],
             [0, None, 0, -1],
             [0, 0, 0, 0]]
        )
        self.goal_state = (0, 3)
        self.wall_state = (1, 1)
        self.start_state = (2, 0)
        self.agent_state = self.start_state

        @property
        def height(self):
            return len(self.reward_map)
        @property
        def width(self):
            return len(self.reward_map[0])
        @property
        def shape(self):
            return self.reward_map.shape

        def actions(self):
            return self.action_space

        def states(self):
            for h in range(self.height):
                for w in range(self.width):
                    yield (h, w)

        def next_state(self, state, action):
            action_move_map = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            move = action_move_map[action]
            next_state = (state[0] + move[0], state[1] + move[1])
            ny, nx = next_state

            if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                next_state = state
            elif next_state == self.wall_state:
                next_state = state

            return next_state

        def reward(self, state, action, next_state):
            return self.reward_map[next_state]

