import random
import numpy as np
import simpy
import pandas as pd

RANDOM_SEED = 42
NUM_TOOLS = 1  # Number of tools in the workstation
PROCESSTIME = 1  # Minutes it takes to process a lot
T_INTER = 15  # Create a lot every ~7 minutes
SIM_TIME = 150  # Simulation time in minutes

# EVENT TRACKING

event_log = []


def generate_interarrival(t_inter, dist="exp"):
    dists = {"exp": np.random.exponential(t_inter), "norm": np.random.normal(t_inter)}
    return dists[dist]


def generate_process_time(t_inter, dist="exp"):
    dists = {"exp": np.random.exponential(t_inter), "norm": np.random.normal(t_inter)}
    return dists[dist]


class Workstation(object):
    """A Workstation has a limited number of machines (``NUM_TOOLS``) to
    clean cars in parallel.

    Products have to request one of the machines. When they got one, they
    can start the washing processes and wait for it to finish (which
    takes ``washtime`` minutes).

    """

    def __init__(self, env, equip_df, process_time):
        self.env = env
        # self.machine = simpy.Resource(env, num_machines)
        self.machine = simpy.FilterStore(env, len(equip_df))
        self.process_time = process_time

        for i, rows in equip_df.iterrows():
            self.machine.put({"EquipID": rows["EquipID"], "Chambers": rows["Chambers"]})

    def lot_process(self, tool_details):
        """The process. It takes a ``lot`` processes and process it."""
        yield self.env.timeout(
            generate_process_time(PROCESSTIME) / tool_details["Chambers"]
        )


def lot(env, lot_id, ws):
    """The car process (each car has a ``lot_id``) arrives at the carwash
    (``ws``) and requests a cleaning machine.

    It then starts the washing process, waits for it to finish and
    leaves to never come back ...

    """
    print(f"{lot_id} arrives at the workstation at {env.now:.2f}.")
    event_log.append([lot_id, env.now, "", "Arrival"])

    with ws.machine.get() as request:
        yield request

        processing_tool = request.value
        print(f"{lot_id} enters the workstation at {env.now:.2f}. -- {processing_tool}")
        event_log.append([lot_id, env.now, processing_tool["EquipID"], "TrackIn"])
        yield env.process(ws.lot_process(processing_tool))

        print(f"{lot_id} leaves the workstation at {env.now:.2f}. -- {processing_tool}")
        event_log.append([lot_id, env.now, processing_tool["EquipID"], "TrackOut"])

        yield ws.machine.put(processing_tool)


def setup(env, num_tools, process_time, t_inter):
    """Create a workstation, a number of initial lots and keep creating lots
    approx. every ``t_inter`` minutes. """
    # Create the workstation
    workstation = Workstation(env, num_tools, process_time)
    env.process(observe(env, workstation))

    # Create 4 initial lots
    for i in range(4):
        print(f"Initial Lot {i}")
        env.process(lot(env, "Lot %d" % i, workstation))

    # Create more lots while the simulation is running
    while True:
        # t_arr = random.randint(t_inter - 2, t_inter + 2)
        t_arr = generate_interarrival(t_inter, "exp")
        yield env.timeout(t_arr)
        i += 1
        env.process(lot(env, "Lot %d" % i, workstation))


obs_times = []
obs_tools = []


def observe(env, workstation):
    while True:
        obs_times.append(env.now)
        obs_tools.append(workstation.machine.items)
        yield env.timeout(1.0)  # logs every one minute (timestep)


equip_df = pd.read_csv("data/tools.csv")

# Setup and start the simulation
print("Workstation")
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment
env = simpy.Environment()
# Start the processes
env.process(setup(env, equip_df, PROCESSTIME, T_INTER))


# Execute!
env.run(until=SIM_TIME)

event_log_df = pd.DataFrame(event_log, columns=["LotID", "TimeStep", "EquipID", "Desc"])
event_log_df.to_csv("output/event_log.csv", index=False)

obs_times_df = pd.DataFrame(obs_times)
obs_times_df.to_csv("output/obs_times.csv", index=False)

obs_tools = pd.DataFrame(obs_tools)
obs_tools.to_csv("output/obs_tools.csv", index=False)

