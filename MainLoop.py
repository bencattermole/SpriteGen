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


c = Generator.Colour()
f = Flower.Flower(12, 27, c)

list_of_flowers = []

for i in range(0, 64):
    co = Generator.Colour()
    fl = Flower.Flower(12, 27, co)
    list_of_flowers.append(fl)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                for flower in list_of_flowers:
                    flower.roll()
            if event.key == pygame.K_j:
                for flower in list_of_flowers:
                    flower.shape_set()
            if event.key == pygame.K_k:
                for flower in list_of_flowers:
                    flower.shape_unset()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5: scroll = max(scroll - 0.1, 0)
            if event.button == 4: scroll = min(scroll + 0.1, 5)

    pygame.display.update()
    screen.fill((0, 0, 0))

    # Generator.draw_flower(screen, regions, 16, 100, 100, 16, 33)

    f_three = Regions.Region(f.template, f.seed)

    regions = [f_three]

    # 16 ,33 and change flower size back to 17

    # r_x_value = f.radius + 1
    # r_y_value = r_x_value*2
    # Generator.draw_flower(screen, regions, 1, 250, 250, r_x_value, r_y_value, f.c, f.size)

    n = 0
    for x in range(0, 8):
        for y in range(0, 8):
            f = list_of_flowers[n]
            r_x_value = f.radius + 1
            r_y_value = r_x_value * 2
            f_three = Regions.Region(f.template, f.seed)

            regions = [f_three]
            Generator.draw_flower(screen, regions, 2, 20 + 128*x, 20 + 128 *y, r_x_value, r_y_value, f.c, f.size)
            n += 1

    clock.tick(30)
