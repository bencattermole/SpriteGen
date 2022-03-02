import pygame
import random
import Regions


def binary(n):
    s = bin(n)

    # removing "0b" prefix
    s1 = s[2:]

    length = len(s1)
    eight_long = 0

    # if we are using more than 8 blocks then we need to change this so that it is the number we ARE using

    if length < 8:
        eight_long = ("0" * (8-length)) + s1
        return eight_long
    else:
        return s1


class Robot:
    def __init__(self, head, body, leg):
        self.h = head
        self.b = body
        self.le = leg
        self.head_temp = [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (2, 3), (3, 3)]
        self.body_temp = [(3, 4), (1, 5), (2, 5), (3, 5), (1, 6), (2, 6), (3, 6), (3, 7)]
        self.legs_temp = [(3, 8), (1, 9), (2, 9), (3, 9), (0, 10), (1, 10), (2, 10), (3, 10)]

    def roll(self):
        self.h = binary(random.randint(0, 255))
        self.b = binary(random.randint(0, 255))
        self.le = binary(random.randint(0, 255))
