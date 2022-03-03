import pygame
import random
import Regions
import Generator
import math


def binary(n, digit_count):
    s = bin(n)

    # removing "0b" prefix
    s1 = s[2:]

    length = len(s1)
    eight_long = 0

    # if we are using more than 8 blocks then we need to change this so that it is the number we ARE using

    if length < digit_count:
        eight_long = ("0" * (digit_count-length)) + s1
        return eight_long
    else:
        return s1


def get_polygon_vertices(sides, radius, ox, oy):
    vertices = []
    angle_div = (360/sides)/2
    for i in range(0, sides):
        x, y = radius * math.cos((math.radians(angle_div) + (i * 2 * math.pi) / sides)), radius * math.sin((math.radians(angle_div) + (i * 2 * math.pi) / sides))
        x1 = int(x)
        y1 = int(y)
        vertices.append((x1+ox, y1+oy))

    return vertices


class Flower:
    def __init__(self, num_of_petals, radius, col):
        self.c = col
        self.size = 1
        self.radius = radius
        self.vertices = get_polygon_vertices(num_of_petals, self.radius, 0, 0)
        self.template = self.generate_template()
        self.seed = 0
        self.shape_set()

    def generate_template(self):
        ox = 0
        oy = 0
        sublime = []

        for vertex in self.vertices:
            # d is distance
            d = 70

            if vertex[0] == ox:
                xpos = int((vertex[0] + ox) / 2) + int(d / 10)
                ypos = int((vertex[1] + oy) / 2)

                test = Regions.filled_region(vertex[0], vertex[1], ox, oy, int(xpos), int(ypos))
                sublime += test
            elif vertex[1] == oy:
                xpos = int((vertex[0] + ox) / 2)
                ypos = int((vertex[1] + oy) / 2) + int(d / 10)

                test = Regions.filled_region(vertex[0], vertex[1], ox, oy, int(xpos), int(ypos))
                sublime += test
            else:
                m = (ox - vertex[1]) / (oy - vertex[0])
                m_per = -1 * (m ** -1)

                mx = int((vertex[0] + ox) / 2)
                my = int((vertex[1] + oy) / 2)

                c = my - mx * m_per

                a = (1 + m_per ** 2)
                b = (2 * m_per * c - 2 * (mx + my * m_per))
                C = ((mx ** 2 + my ** 2 - d) - 2 * my * c) + c ** 2

                discrim = b * b - 4 * a * C

                xpos = (-1 * b + math.sqrt(discrim)) / (2 * a)
                ypos = m_per * xpos + c

                test = Regions.filled_region(vertex[0], vertex[1], ox, oy, int(xpos), int(ypos))
                sublime += test

        halved = []
        for tile in sublime:
            if tile[0] <= 0:
                moved_tile_x = tile[0] + self.radius
                moved_tile_y = tile[1] + self.radius
                moved_tile = (moved_tile_x, moved_tile_y)
                halved.append(moved_tile)

        return halved

    def shape_set(self):
        total = len(self.template)
        self.seed = binary(2**total - 1, total)

    def shape_unset(self):
        total = len(self.template)
        self.seed = binary(random.randint(0, 2 ** total - 1), total)

    def roll(self):
        new_num = random.randint(3, 20)
        self.vertices = get_polygon_vertices(new_num, self.radius, 0, 0)
        self.template = self.generate_template()
        total = len(self.template)
        self.seed = binary(random.randint(0, 2**total - 1), total)
        self.c = Generator.Colour()
        self.size = random.randint(1, 5)
