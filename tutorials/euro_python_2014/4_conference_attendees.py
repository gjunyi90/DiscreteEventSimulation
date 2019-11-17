from random import randint
import simpy

TALKS_PER_SESSION = 3
TALK_LENGTH = 30
BREAK_LENGTH = 15

def attendee(env, name, knowledge=0, hunger=0):
    while True:
        # Visit talks
        for i in range(TALKS_PER_SESSION):
            print(f'Talk {i}:')
            knowledge += randint(0, 3) / (1 + hunger)
            hunger += randint(1, 4)

            yield env.timeout(TALK_LENGTH)

        print(f'Attendee {name} finished talks with knowledge {knowledge:.2f} and hunger {hunger:.2f}')

        # Go to buffet
        food = randint(3, 12)
        hunger -= min(food, hunger)

        yield env.timeout(BREAK_LENGTH)

        print(f'Attendee {name} finished eating with hunger {hunger:.2f}')


env = simpy.Environment()
for i in range(5):
    env.process(attendee(env, i))
print('Finished Initialization of process')
env.run(until=220)
