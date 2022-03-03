import random
import math
import pygame


class Colour:
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0
        self.base_dark = (0, 0, 0)
        self.b_d1 = (0, 0, 0)
        self.base_light = (0, 0, 0)
        self.dom = 'null'
        self.random_colour()

    def random_colour(self):
        dom_col_test = random.randint(0, 10)

        if dom_col_test > 5:
            choice = random.uniform(0, 1)

            frst = random.randint(0, 255)
            scnd = random.randint(0, 255)
            thrd = random.randint(0, 255)

            list_of_cands = [frst, scnd, thrd]
            list_of_cands.sort(reverse=True)

            for_bd = random.randint(0, 63)
            for_bd1 = random.randint(0, 33)
            for_blbig = random.randint(0, 63)
            for_blsml = random.randint(0, 13)

            if choice < 0.4:
                # red dominant
                self.dom = 'RED'
                self.base_dark = (for_bd, 0, 0)
                self.b_d1 = (for_bd1, 0, 0)
                self.base_light = (for_blbig, for_blsml, for_blsml)

                self.r = list_of_cands[0]

                self.g = list_of_cands[1]
                self.b = list_of_cands[2]

            elif choice < 0.6:
                # green dominant
                self.dom = 'GREEN'
                self.base_dark = (0, for_bd, 0)
                self.b_d1 = (0, for_bd1, 0)
                self.base_light = (for_blsml, for_blbig, for_blsml)

                self.g = list_of_cands[0]

                self.r = list_of_cands[1]
                self.b = list_of_cands[2]

            elif choice <= 1:
                # blue dominant
                self.dom = 'BLUE'
                self.base_dark = (0, 0, for_bd)
                self.b_d1 = (0, 0, for_bd1)
                self.base_light = (for_blsml, for_blsml, for_blbig)

                self.b = list_of_cands[0]

                self.g = list_of_cands[1]
                self.r = list_of_cands[2]

            else:
                pass
        else:
            choice = random.randint(0, 2)

            frst = random.randint(0, 255)
            scnd = random.randint(0, 255)
            thrd = random.randint(0, 255)

            list_of_cands = [frst, scnd, thrd]
            list_of_cands.sort(reverse=True)

            six1 = random.randint(0, 63)
            six2 = random.randint(0, 63)
            six3 = random.randint(0, 63)

            list_of_sixs = [six1, six2, six3]
            list_of_sixs.sort(reverse=True)

            if choice == 0:
                # red dominant
                self.dom = 'RED'
                self.base_dark = (list_of_sixs[0], list_of_sixs[1], list_of_sixs[2])
                self.b_d1 = (list_of_sixs[0], list_of_sixs[1], list_of_sixs[2])
                self.base_light = (list_of_sixs[0], list_of_sixs[1], list_of_sixs[2])

                self.r = list_of_cands[0]

                self.g = list_of_cands[1]
                self.b = list_of_cands[2]

            elif choice == 1:
                # green dominant
                self.dom = 'GREEN'
                self.base_dark = (list_of_sixs[1], list_of_sixs[0], list_of_sixs[2])
                self.b_d1 = (list_of_sixs[1], list_of_sixs[0], list_of_sixs[2])
                self.base_light = (list_of_sixs[1], list_of_sixs[0], list_of_sixs[2])

                self.g = list_of_cands[0]

                self.r = list_of_cands[1]
                self.b = list_of_cands[2]

            elif choice == 2:
                # blue dominant
                self.dom = 'BLUE'
                self.base_dark = (list_of_sixs[2], list_of_sixs[1], list_of_sixs[0])
                self.b_d1 = (list_of_sixs[2], list_of_sixs[1], list_of_sixs[0])
                self.base_light = (list_of_sixs[2], list_of_sixs[1], list_of_sixs[0])

                self.b = list_of_cands[0]

                self.g = list_of_cands[1]
                self.r = list_of_cands[2]

            else:
                pass


def circle(radius):
    # init vars
    switch = 3 - (2 * radius)
    points = []
    x = 0
    y = radius
    # first quarter/octant starts clockwise at 12 o'clock
    while x <= y:
        # first quarter first octant
        points.append((x, -y))
        # first quarter 2nd octant
        points.append((y, -x))
        # second quarter 3rd octant
        points.append((y, x))
        # second quarter 4.octant
        points.append((x, y))
        # third quarter 5.octant
        points.append((-x, y))
        # third quarter 6.octant
        points.append((-y, x))
        # fourth quarter 7.octant
        points.append((-y, -x))
        # fourth quarter 8.octant
        points.append((-x, -y))
        if switch < 0:
            switch = switch + (4 * x) + 6
        else:
            switch = switch + (4 * (x - y)) + 10
            y = y - 1
        x = x + 1
    return points


def draw_entity(screen, regions, scale, start_x, start_y, x_range, y_range):
    drawn = []

    # change this if we change the size of the template
    # I think the general form of this would be scale * (2*symmetry axis - 1)
    sym_x = (scale*(30))

    # make the below use input sprite size parameters in place of 4 and 11

    for x in range(0, x_range):
        for y in range(0, y_range):
            if (x, y) in regions[0].map:
                position = regions[0].map.index((x, y))
                if regions[0].seed[position] == '1':
                    drawn.append((x, y))
                else:
                    pass

            is_outline = False
            draw = False
            alpha = 4

            if (x, y) in drawn:
                draw = True
                if (x + 1, y) in drawn:
                    alpha -= 1
                if (x - 1, y) in drawn:
                    alpha -= 1
                if (x, y + 1) in drawn:
                    alpha -= 1
                if (x, y - 1) in drawn:
                    alpha -= 1
            else:
                if (x + 1, y) in drawn:
                    is_outline = True
                    draw = True
                    alpha -= 1
                if (x - 1, y) in drawn:
                    is_outline = True
                    draw = True
                    alpha -= 1
                if (x, y + 1) in drawn:
                    is_outline = True
                    draw = True
                    alpha -= 1
                if (x, y - 1) in drawn:
                    is_outline = True
                    draw = True
                    alpha -= 1

            if draw:
                if is_outline:
                    if alpha == 0:
                        pygame.draw.rect(screen, (33, 33, 33), (start_x + (scale * x), start_y + (scale * y), scale, scale))
                        pygame.draw.rect(screen, (33, 33, 33), ((start_x+sym_x) - (scale * x), start_y + (scale * y), scale, scale))
                    else:
                        pygame.draw.rect(screen, (63*alpha, 63*alpha, 63*alpha), (start_x + (scale*x), start_y + (scale*y), scale, scale))
                        pygame.draw.rect(screen, (63*alpha, 63*alpha, 63*alpha), ((start_x+sym_x) - (scale*x), start_y + (scale*y), scale, scale))
                else:
                    if alpha == 4:
                        pygame.draw.rect(screen, (0, 232, 70), (start_x + (scale * x), start_y + (scale * y), scale, scale))
                        pygame.draw.rect(screen, (0, 232, 70), ((start_x+sym_x) - (scale * x), start_y + (scale * y), scale, scale))
                    elif alpha == 0:
                        pygame.draw.rect(screen, (0, 33, 0), (start_x + (scale * x), start_y + (scale * y), scale, scale))
                        pygame.draw.rect(screen, (0, 33, 0), ((start_x+sym_x) - (scale * x), start_y + (scale * y), scale, scale))
                    else:
                        pygame.draw.rect(screen, (0, 63 * alpha, 0), (start_x + (scale * x), start_y + (scale * y), scale, scale))
                        pygame.draw.rect(screen, (0, 63 * alpha, 0), ((start_x+sym_x) - (scale * x), start_y + (scale * y), scale, scale))


def draw_flower(screen, regions, scale, start_x, start_y, x_range, y_range, c, cen_size):
    drawn = []

    # change this if we change the size of the template
    # I think the general form of this would be scale * (2*symmetry axis - 1)
    sym_x = (scale*2*x_range-scale*2)

    # make the below use input sprite size parameters in place of 4 and 11

    for x in range(0, x_range):
        for y in range(0, y_range):

            # seems redundant we are checking every position to see if it appears in any of the regions

            for region in regions:
                if (x, y) in region.map:
                    position = region.map.index((x, y))
                    if region.seed[position] == '1':
                        drawn.append((x, y))
                    else:
                        pass

    for x in range(0, x_range):
        for y in range(0, y_range):
            is_outline = False
            draw = False
            alpha = 4

            if (x, y) in drawn:
                draw = True
                if (x + 1, y) in drawn:
                    alpha -= 1
                if (x - 1, y) in drawn:
                    alpha -= 1
                if (x, y + 1) in drawn:
                    alpha -= 1
                if (x, y - 1) in drawn:
                    alpha -= 1
            else:
                if (x + 1, y) in drawn:
                    is_outline = True
                    draw = True
                    alpha -= 1
                if (x - 1, y) in drawn:
                    is_outline = True
                    draw = True
                    alpha -= 1
                if (x, y + 1) in drawn:
                    is_outline = True
                    draw = True
                    alpha -= 1
                if (x, y - 1) in drawn:
                    is_outline = True
                    draw = True
                    alpha -= 1

            if draw:
                if is_outline:
                    if alpha == 0:
                        pygame.draw.rect(screen, (c.r, c.g, c.b), (start_x + (scale * x), start_y + (scale * y), scale, scale))
                        pygame.draw.rect(screen, (c.r, c.g, c.b), ((start_x+sym_x) - (scale * x), start_y + (scale * y), scale, scale))
                    else:
                        pygame.draw.rect(screen, (c.base_light[0]*alpha, c.base_light[1]*alpha, c.base_light[2]*alpha), (start_x + (scale*x), start_y + (scale*y), scale, scale))
                        pygame.draw.rect(screen, (c.base_light[0]*alpha, c.base_light[1]*alpha, c.base_light[2]*alpha), ((start_x+sym_x) - (scale*x), start_y + (scale*y), scale, scale))
                else:
                    if alpha == 4:
                        pygame.draw.rect(screen, (c.r, c.g, c.b), (start_x + (scale * x), start_y + (scale * y), scale, scale))
                        pygame.draw.rect(screen, (c.r, c.g, c.b), ((start_x+sym_x) - (scale * x), start_y + (scale * y), scale, scale))
                    elif alpha == 0:
                        pygame.draw.rect(screen, c.b_d1, (start_x + (scale * x), start_y + (scale * y), scale, scale))
                        pygame.draw.rect(screen, c.b_d1, ((start_x+sym_x) - (scale * x), start_y + (scale * y), scale, scale))
                    else:
                        pygame.draw.rect(screen, (c.base_dark[0] * alpha, c.base_dark[1] * alpha, c.base_dark[2] * alpha), (start_x + (scale * x), start_y + (scale * y), scale, scale))
                        pygame.draw.rect(screen, (c.base_dark[0] * alpha, c.base_dark[1] * alpha, c.base_dark[2] * alpha), ((start_x+sym_x) - (scale * x), start_y + (scale * y), scale, scale))

    center = []

    for i in range(0, cen_size):
        layer = circle(i)
        center += layer

    x = center[0][0]
    y = center[0][1]

    missing_four = [(x+1, y-1), (x+1, y+1), (x-1, y+1), (x-1, y-1)]

    center += missing_four
    for points in center:
        if (points[0] % 2) == (points[1] % 2):
            pygame.draw.rect(screen, (245, 212, 66), (start_x + (scale * (points[0] + x_range-1)), start_y + (scale * (points[1] + y_range/2 - 1)), scale, scale))
        else:
            pygame.draw.rect(screen, (255, 174, 0), (start_x + (scale * (points[0] + x_range-1)), start_y + (scale * (points[1] + y_range/2 - 1)), scale, scale))
