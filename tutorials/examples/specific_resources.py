import simpy

#class Pre_Assem:
#    def __init__(self, env, name, value):
#        self.nodes = simpy.Resource(env, capacity = 1)
#        self.name = name
#        self.value = value

class Job:
    def __init__(self, env, name, release, value):
        self.env = env
        self.name = name
        self.release = release
        self.value = value


def Process(env, job, pre_assem):
    print('initial slot values: ', pre_assem.items)
    yield env.timeout(job.release)

    print('available slots before: ', pre_assem.capacity)
    request = yield pre_assem.get(lambda request: request['value'] == job.value) | pre_assem.get()
    print('available slots after: ', pre_assem.capacity)
    print('slot requested: ' , request)

    print('slot is beeing used')
    yield env.timeout(10)
    print('slots after use: ', pre_assem.items)
    yield pre_assem.put({'value': job.value})
    print('new slots values: ', pre_assem.items)




env = simpy.Environment()
pre_assem = simpy.FilterStore(env, 2)

#preassem1 = Pre_Assem(env, 1, 1)
#preassem2 = Pre_Assem(env, 2, 1)
#pre_assem.items = [preassem1, preassem2]

pre_assem.put({'name':1, 'value':1})
pre_assem.put({'name':2, 'value':1})

jobs = [Job(env, 1, 0, 1),
        Job(env, 2, 0, 2),
        Job(env, 3, 60, 3)]

for job in jobs:
    env.process(Process(env, job, pre_assem))
env.run()