import numpy as np
import random # https://docs.scipy.org/doc/numpy-1.14.1/reference/routines.random.html
import pandas as pd

t_inter = 7

# def generate_interarrival():
#     return np.random.exponential(t_inter)


def generate_interarrival(t_inter, dist='exp'):
    dists = {
        'exp': np.random.exponential(t_inter),
        'norm': np.random.normal(t_inter)
    }
    return dists[dist]


# for i in range(100):
#     # print(random.randint(t_inter - 2, t_inter + 2))
#     print(generate_interarrival(t_inter, 'norm'))


df = pd.read_csv('tools.csv')
# print(df)

for i, rows in df.iterrows():
    print(rows['EquipID'])


print(len(df))