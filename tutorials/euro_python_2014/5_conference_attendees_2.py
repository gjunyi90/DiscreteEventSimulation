from random import randint
import simpy

TALKS_PER_SESSION = 3
TALK_LENGTH = 30
BREAK_LENGTH = 15
DURATION_EAT = 3
BUFFET_SLOTS = 1

def attendee(env, name, buffet, knowledge=0, hunger=0):
    while True:
        # Visit talks
        for _ in range(TALKS_PER_SESSION):
            knowledge += randint(0, 3) / (1 + hunger)
            hunger += randint(1, 4)

            yield env.timeout(TALK_LENGTH)

        print(f'Attendee {name} finished talks with knowledge {knowledge:.2f} and hunger {hunger:.2f}')

        # Go to buffet
        start = env.now
        with buffet.request() as req:
            yield req | env.timeout(BREAK_LENGTH - DURATION_EAT)
            time_left = BREAK_LENGTH - (env.now - start)

            if req.triggered:
                food = min(randint(3, 12), time_left)
                yield env.timeout(DURATION_EAT)
                hunger -= min(food, hunger)
                time_left -= DURATION_EAT
                print(f'Attendee {name} finished eating with hunger {hunger:.2f}')
            else:
                hunger += 1
                print(f'Attendee {name} didn\'t make it to the buffet. Hunger is now at {hunger:.2f}')

        yield env.timeout(time_left)


env = simpy.Environment()
buffet = simpy.Resource(env, capacity=BUFFET_SLOTS)
for i in range(5):
    env.process(attendee(env, i, buffet))
env.run(until=220)
