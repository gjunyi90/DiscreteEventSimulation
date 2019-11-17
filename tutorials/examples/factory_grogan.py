# Factory System Discrete Event Simulation in Python (Process interaction)
# https://www.youtube.com/watch?v=G2WftFiBRFg&t=167s

import simpy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


# repairers and spares as arguments so that the process can use them
def factory_run(env, repairers, spares):
    global cost # setting this as a global variable so that other processes can access and modify

    cost = 0.0

    # launching the 50 operating machine activities
    for i in range(50):
        env.process(operate_machine(env, repairers, spares))

    while True:
        cost += 3.75 * 8 * repairers.capacity + 30 * spares.capacity
        yield env.timeout(8.0)


def operate_machine(env, repairers, spares):
    global cost

    while True:
        yield env.timeout(generate_time_to_failure())
        t_broken = env.now
        print(f'{t_broken:.2f} machine broke')
        env.process(repair_machine(env, repairers, spares))
        # launch repair process
        yield spares.get(1) # allow us to wait until one spares is available
        t_replaced = env.now
        print(f'{t_broken:.2f} machine replaced')
        cost += 20 * (t_replaced - t_broken)


def repair_machine(env, repairers, spares):
    with repairers.request() as request:
        yield request
        yield env.timeout(generate_repair_time())
        yield spares.put(1) # put back the spares into the spares pool
    print(f'{env.now:.2f} repair complete')


def generate_time_to_failure():
    return np.random.uniform(132, 182)


def generate_repair_time():
    return np.random.uniform(4,10)


obs_times = []
obs_cost = []
obs_spares = []


def observe(env, spares):
    while True:
        obs_times.append(env.now)
        obs_cost.append(cost)
        obs_spares.append(spares.level)
        yield env.timeout(1.0) # ensure that the logging interval is 1hour


np.random.seed(0)

env = simpy.Environment()

repairers = simpy.Resource(env, capacity=3)

# By representing the spares as a Container rather than a Resource,
# it allows us some new methods to request and release individual components from it
spares = simpy.Container(env, init=15, capacity=15)

env.process(factory_run(env, repairers, spares))
env.process(observe(env, spares))

env.run(until=8*5*52)


plt.figure()
plt.step(obs_times, obs_spares, where='post')
plt.xlabel('Time (hours)')
plt.ylabel('Spares level')

plt.figure()
plt.step(obs_times, obs_cost, where='post')
plt.xlabel('Time (hours)')
plt.ylabel('Spares level')
plt.show()

print(f'Total cost was {obs_cost[-1]:.3f}')
