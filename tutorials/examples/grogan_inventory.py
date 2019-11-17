# Inventory System Discrete Event Simulation in Python (Process interaction)
# https://www.youtube.com/watch?v=Kmu9DNQamLw

import simpy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def warehouse_run(env, order_cutoff, order_target):
    global inventory, balance, num_ordered # alternative to using global variables are OOP

    inventory = order_target
    balance = 0.0
    num_ordered = 0

    while True:
        interarrival = generate_interarrival()
        yield env.timeout(interarrival)
        balance -= inventory * 2 * interarrival
        demand = generate_demand()
        if demand < inventory:
            balance += 100 * demand
            inventory -= demand
            print(f'{env.now:.2f}t: {demand} sold')
        else:
            balance += 100 * inventory
            inventory = 0
            print(f'{env.now:.2f}t: {inventory} sold (out of stock)')

        if inventory < order_cutoff and num_ordered == 0:
            env.process(handle_order(env, order_target))


def handle_order(env, order_target):
    global inventory, balance, num_ordered

    num_ordered = order_target - inventory
    print(f'{env.now:.2f}t: placed order for {inventory} ')
    balance -= 50 * num_ordered
    yield env.timeout(2.0)
    inventory += num_ordered
    num_ordered = 0
    print(f'{env.now:.2f}t: received order {inventory} in inventory')


def generate_interarrival():
    return np.random.exponential(1./5)


def generate_demand():
    return np.random.randint(1, 5)


obs_time = []
inventory_level = []


def observe(env):
    global inventory

    while True:
        obs_time.append(env.now)
        inventory_level.append(inventory)
        yield env.timeout(0.1) # logs this data 10 times a day


np.random.seed(0)
env = simpy.Environment()
env.process(warehouse_run(env, 10, 30))
env.process(observe(env))
env.run(until=5.0)


plt.figure()
plt.step(obs_time, inventory_level, where='post')
plt.xlabel('Simulation time (days)')
plt.ylabel('Inventory level')
plt.show()
