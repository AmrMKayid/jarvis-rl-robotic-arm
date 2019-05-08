import click
from jarvis.envs.env import ArmEnv
from jarvis.agents.ddpg import DDPG

MAX_STEPS = 200
MAX_EPISODES = 500

# set env
env = ArmEnv()
state_dim = env.state_dim
action_dim = env.action_dim
action_bound = env.action_bound


# set RL method
rl = DDPG(state_dim, action_dim, action_bound)


def train():
    # start training
    for episode in range(MAX_EPISODES):
        s = env.reset()
        ep_r = 0.
        for step in range(MAX_STEPS):
            env.render()

            a = rl.choose_action(s)

            s_, r, done = env.step(a)

            rl.store_transition(s, a, r, s_)

            ep_r += r
            if rl.memory_full:
                # start to learn once has fulfilled the memory
                rl.learn()

            s = s_
            if done or step == MAX_STEPS-1:
                print('Ep: %i | %s | ep_r: %.1f | steps: %i' %
                      (episode, '---' if not done else 'done', ep_r, step))
                break
    rl.save()


def eval():
    rl.restore()
    env.render()
    env.viewer.set_vsync(True)
    while True:
        s = env.reset()
        for _ in range(200):
            env.render()
            a = rl.choose_action(s)
            s, r, done = env.step(a)
            if done:
                print("You reach the goal! Here is your reward, ", r)
                break


@click.command()
@click.option('--on_train', default="True", help='Train the agent from scratch', type=bool)
def main(on_train):
    if on_train:
        train()
    else:
        eval()


if __name__ == "__main__":
    main()
