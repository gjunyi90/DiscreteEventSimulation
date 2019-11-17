# Queuing System Discrete Event Simulation in Python (Process interaction)
# https://www.youtube.com/watch?v=eSNfC-HOl44

import simpy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

def generate_interarrival():
    # arrival rate 3 (3 customers per minute)
    return np.random.exponential(1./3.0)


def generate_service():
    # service rate 4 (4 customers per minute)
    return np.random.exponential(1./4.0)


def cafe_run(env, servers):
    i = 0
    while True:
        i += 1
        yield env.timeout(generate_interarrival())
        print(f'{env.now:.3f} customer {i} arrives')
        env.process(customer(env, i, servers))


wait_t = []


def customer(env, customer, servers):
    with servers.request() as request:
        t_arrival = env.now
        yield request
        print(f'{env.now:.3f} customer {customer} is being served')
        yield env.timeout(generate_service())
        print(f'{env.now:.3f} customer {customer} departs')
        t_depart = env.now
        wait_t.append(t_depart - t_arrival)


obs_times = []
q_length = []


def observe(env, servers):
    while True:
        obs_times.append(env.now)
        q_length.append(len(servers.queue))
        yield env.timeout(1.0)


np.random.seed(0)

env = simpy.Environment()

servers = simpy.Resource(env, capacity=1)

env.process(cafe_run(env, servers))
env.process(observe(env, servers))

env.run(until=10)

plt.figure()
plt.hist(wait_t)
plt.xlabel('Waiting time (min)')
plt.ylabel('Number of Customers')
plt.show()

# print(obs_times)
# print(q_length)
plt.figure()
plt.step(obs_times, q_length, where='post')
plt.xlabel('Time (min)')
plt.ylabel('Queue Length')

plt.show()