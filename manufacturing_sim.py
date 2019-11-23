import random
import numpy as np
import simpy


RANDOM_SEED = 42
NUM_TOOLS = 1  # Number of tools in the workstation
PROCESSTIME = 5      # Minutes it takes to process a lot
T_INTER = 7       # Create a lot every ~7 minutes
SIM_TIME = 100     # Simulation time in minutes


# TODO -  Replace fixed interarrival with probabilistic interarrival
def generate_interarrival():
    return np.random.exponential(1./5)

def generate_demand():
    return np.random.randint(1, 5)

class Workstation(object):
    """A carwash has a limited number of machines (``NUM_TOOLS``) to
    clean cars in parallel.

    Cars have to request one of the machines. When they got one, they
    can start the washing processes and wait for it to finish (which
    takes ``washtime`` minutes).

    """
    def __init__(self, env, num_machines, process_time):
        self.env = env
        # TODO -  Use a FilterStore
        self.machine = simpy.Resource(env, num_machines)
        self.process_time = process_time

    def lot_process(self, car):
        """The process. It takes a ``lot`` processes and process it."""
        yield self.env.timeout(PROCESSTIME)


def lot(env, lot_id, ws):
    """The car process (each car has a ``lot_id``) arrives at the carwash
    (``ws``) and requests a cleaning machine.

    It then starts the washing process, waits for it to finish and
    leaves to never come back ...

    """
    print('%s arrives at the workstation at %.2f.' % (lot_id, env.now))
    with ws.machine.request() as request:
        yield request

        print('%s enters the workstation at %.2f.' % (lot_id, env.now))
        yield env.process(ws.lot_process(lot_id))

        print('%s leaves the workstation at %.2f.' % (lot_id, env.now))


def setup(env, num_tools, process_time, t_inter):
    """Create a workstation, a number of initial lots and keep creating lots
    approx. every ``t_inter`` minutes. """
    # Create the workstation
    workstation = Workstation(env, num_tools, process_time)

    # Create 4 initial lots
    for i in range(4):
        print(f'Initial Lot {i}')
        env.process(lot(env, 'Lot %d' % i, workstation))

    # Create more lots while the simulation is running
    while True:
        # TODO -  Replace fixed interarrival with probabilistic interarrival
        timeout = random.randint(t_inter - 2, t_inter + 2)
        yield env.timeout(timeout)
        i += 1
        env.process(lot(env, 'Lot %d' % i, workstation))

# EVENT TRACKING

# obs_times = []
# obs_cost = []
# obs_spares = []
#
#
# def observe(env, spares):
#     while True:
#         obs_times.append(env.now)
#         obs_cost.append(cost)
#         obs_spares.append(spares.level)
#         yield env.timeout(1.0) # ensure that the logging interval is 1hour
#


# Setup and start the simulation
print('Workstation')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_TOOLS, PROCESSTIME, T_INTER))
# env.process(observe(env, spares))

# Execute!
env.run(until=SIM_TIME)