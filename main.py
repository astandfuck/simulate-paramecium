import core.Environment as E

environment = E.Environment()

def setup(_environment: E.Environment):
    environment.generate_food()

def loop(_environment: E.Environment):
    environment.spread()

E.start(environment, setup, loop)
