from random import choice

from script.animals import animals
from script.emotions import emotions


def username():
    animal = choice(animals)
    emotion = choice(emotions)
    return f"{emotion}{animal}"
