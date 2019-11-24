import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set()

event_df = pd.read_csv('event_log.csv')
print(event_df)

# plt.figure()
# plt.step(obs_times, obs_spares, where='post')
# plt.xlabel('Time (hours)')
# plt.ylabel('Spares level')
#
# plt.figure()
# plt.step(obs_times, obs_cost, where='post')
# plt.xlabel('Time (hours)')
# plt.ylabel('Spares level')
# plt.show()
#
# print(f'Total cost was {obs_cost[-1]:.3f}')