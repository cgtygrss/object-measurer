import random


def generate_random_color():
    r = random.randint(0, 200)
    g = random.randint(0, 200)
    b = random.randint(0, 200)
    return [r, g, b]
