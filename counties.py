import random

countries = ["Россия", "СССР", "США", "Германия", "Швеция"]
upgrades = ["Ракета", "Щит", "Реформа"]

class Country:
    def __init__(self, country, friend=None, villain=None):
        self.name = country

        random_values = random.sample([0, 1, 2], 3)
        self.rockets = 1 if random_values[0] == 1 else 0
        self.shield = 1 if random_values[1] == 1 else 0
        self.reform = 1 if random_values[2] == 1 else 0

        self.friend = friend
        self.villain = villain