# Balancing-Pendulum-with-Q-Learning

## Q-Learning
Q-learning is an off policy reinforcement learning algorithm that seeks to find the best action to take given the current state. It’s considered off-policy because the q-learning function learns from actions that are outside the current policy, like taking random actions, and therefore a policy isn’t needed. More specifically, q-learning seeks to learn a policy that maximizes the total reward.

<img src="https://github.com/BhanuPrakashPebbeti/Balancing-Pendulum-with-Q-Learning/blob/main/assets/Q-learning.jfif" width="400" height="200">

## Important Terms in Q-Learning
- States: The State, S, represents the current position of an agent in an environment. 
- Action: The Action, A, is the step taken by the agent when it is in a particular state.
- Rewards: For every action, the agent will get a positive or negative reward.
- Episodes: When an agent ends up in a terminating state and can’t take a new action.
- Q-Values: Used to determine how good an Action, A, taken at a particular state, S, is. Q (A, S)
- 
## Bellman Equation
The Bellman Equation is used to determine the value of a particular state and deduce how good it is to be in/take that state. This equation is used to update the Q-Table. The optimal state will give us the highest optimal value. 

<img src="https://github.com/BhanuPrakashPebbeti/Balancing-Pendulum-with-Q-Learning/blob/main/assets/bellman-equation.jfif" width="600" height="200">

## Reward Stats while Training

<img src="https://github.com/BhanuPrakashPebbeti/Balancing-Pendulum-with-Q-Learning/blob/main/Q-Learning/Statistics.png" width="400" height="400">

## Pendulum Balancing 
![Pendulum_gif](https://github.com/BhanuPrakashPebbeti/Balancing-Pendulum-with-Q-Learning/blob/main/assets/Pendulum-Q.gif)
