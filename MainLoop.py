import pygame
import random
import Generator
import Robot
import Regions
import Flower
import math
import time

Screen_Size = 1024
block_size = 4
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((Screen_Size, Screen_Size))
pygame.display.set_caption("Sprite Generator")

block_scale = int(Screen_Size/block_size)

clock = pygame.time.Clock()

pygame.init()

running = True

# tic = time.perf_counter()
# toc = time.perf_counter()
# print(f"ran two diffuse in {toc - tic:0.4f} seconds")

scroll = 0.5


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


head = binary(random.randint(0, 255), 8)
body = binary(random.randint(0, 255), 8)
legs = binary(random.randint(0, 255), 8)

r = Robot.Robot(head, body, legs)


list_of_flowers = []

for i in range(0, 64):
    p1 = binary(2**102 -1, 102)
    p2 = binary(2**78 -1, 78)
    p3 = binary(2**94 -1, 94)

    c = Generator.Colour()
    f = Flower.Flower(p1, p2, p3, c)
    list_of_flowers.append(f)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                for flower in list_of_flowers:
                    flower.roll()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5: scroll = max(scroll - 0.1, 0)
            if event.button == 4: scroll = min(scroll + 0.1, 5)

    pygame.display.update()
    screen.fill((0, 0, 0))

    # Generator.draw_flower(screen, regions, 16, 100, 100, 16, 33)

    n = 0
    for x in range(0, 8):
        for y in range(0, 8):
            f = list_of_flowers[n]
            f_one = Regions.Region(f.p1_temp, f.p1)
            f_two = Regions.Region(f.p2_temp, f.p2)
            f_three = Regions.Region(f.p3_temp, f.p3)

            regions = [f_one, f_two, f_three]
            Generator.draw_flower(screen, regions, 2, 20 + x * 128, 20 + y * 128, 16, 33, f.c, f.size)
            n += 1

    clock.tick(30)
