from jarvis.envs.env import ArmEnv
from jarvis.agents.ddpg import DDPG

MAX_STEPS = 200
MAX_EPISODES = 500

# set env
env = ArmEnv()
s_dim = env.state_dim
a_dim = env.action_dim
a_bound = env.action_bound


# set RL method


# Sample rendering
while True:
    env.render()
    env.step(env.sample_action())
