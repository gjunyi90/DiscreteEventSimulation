def speaker(env, start):
    until_start = start - env.now
    yield env.timeout(until_start)

    yield env.timeout(30)