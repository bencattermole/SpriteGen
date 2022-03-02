import pygame


class Region:
    def __init__(self, coord_map, seed):
        self.map = coord_map
        self.seed = seed


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_line(start, end):
    # Setup initial conditions
    x1 = start[0]
    y1 = start[1]
    x2 = end[0]
    y2 = end[1]
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


def lerp(v0, v1, t):
    return v0 + t * (v1 - v0)


def flood_fill(area, x, y):
    if (x, y) not in area:
        area.append((x, y))
        if (x - 1, y) not in area:
            flood_fill(area, x - 1, y)
        if (x + 1, y) not in area:
            flood_fill(area, x + 1, y)
        if (x, y - 1) not in area:
            flood_fill(area, x, y - 1)
        if (x, y + 1) not in area:
            flood_fill(area, x, y + 1)


def filled_region(x1, y1, x2, y2, x3, y3):
    outline = enc_region_cmap_gen(x1, y1, x2, y2, x3, y3)

    mx = int((x1+x2)/2)
    my = int((y1+y2)/2)

    flood_fill(outline, mx, my)

    region_to_return = []
    n = 0
    for tile in outline:
        if n == 0:
            region_to_return.append(tile)
            n += 1
        else:
            if tile in region_to_return:
                pass
            else:
                region_to_return.append(tile)

    return region_to_return


def enc_region_cmap_gen(x1, y1, x2, y2, x3, y3):
    rflct_anchr = get_mirror_anchor_point(x1, y1, x2, y2, x3, y3)

    true_side = region_coord_map_generator(x1, y1, x2, y2, x3, y3)

    t_start = get_line(true_side[0], (x1, y1))
    t_end = get_line(true_side[-1], (x2, y2))
    true_side_connected = []

    true_side_connected += t_start
    true_side_connected += t_end

    nt = 1
    for tile in true_side:
        if nt == len(true_side):
            pass
        else:
            con = get_line(tile, true_side[nt])
            true_side_connected += con

        nt += 1

    true_side += true_side_connected

    mirror_side = region_coord_map_generator(x1, y1, x2, y2, rflct_anchr[0], rflct_anchr[1])

    m_start = get_line(mirror_side[0], (x1, y1))
    m_end = get_line(mirror_side[-1], (x2, y2))
    mirror_side_connected = []

    mirror_side_connected += m_start
    mirror_side_connected += m_end

    nt = 1
    for tile in mirror_side:
        if nt == len(mirror_side):
            pass
        else:
            con = get_line(tile, mirror_side[nt])
            mirror_side_connected += con

        nt += 1

    mirror_side += mirror_side_connected

    all_together = []

    all_together += true_side
    all_together += mirror_side

    return all_together


def region_coord_map_generator(x1, y1, x2, y2, x3, y3):
    p0 = Point(x1, y1)
    p1 = Point(x2, y2)

    achr = Point(x3, y3)
    positions = []

    tens_to_test = []

    for i in range(1, 10):
        t = i/10
        tens_to_test.append(t)

    for t_val in tens_to_test:
        ax = int(lerp(p0.x, achr.x, t_val))
        ay = int(lerp(p0.y, achr.y, t_val))

        bx = int(lerp(achr.x, p1.x, t_val))
        by = int(lerp(achr.y, p1.y, t_val))

        x = int(lerp(ax, bx, t_val))
        y = int(lerp(ay, by, t_val))

        positions.append((x, y))

    return positions


def get_mirror_anchor_point(x1, y1, x2, y2, x3, y3):
    # initial line
    if y2 == y1:
        x_rlf = x3
        y_rlf = y2 - (y3 - y2)
        mirror_anchor = (x_rlf, y_rlf)
    elif x2 == x1:
        y_rlf = y3
        x_rlf = x2 - (x3 - x2)
        mirror_anchor = (x_rlf, y_rlf)
    else:

        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1

    # perpendicular line
        m_per = -1 * (m ** -1)
        c_per = y3 - m_per * x3

    # intercept point
        x_inc = (c_per - c) / (m - m_per)
        y_inc = m * x_inc + c

    # reflected point
        x_rlf = (2*x_inc) - x3
        y_rlf = (2*y_inc) - y3

        mirror_anchor = (x_rlf, y_rlf)

    return mirror_anchor
