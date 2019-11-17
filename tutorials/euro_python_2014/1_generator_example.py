def generator(x):
    y = yield x + 1
    return y + 1

g = generator(1)
print(next(g))
g.send(3)