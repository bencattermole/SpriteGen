'''

Documentation:
    Coming soon :)

Code snippets:

display sprites from a list in a grid:
    n = 0
    for x in range(0, 8):
        for y in range(0, 8):
            r = list_of_robots[n]
            Generator.draw_entity(screen, r.head_temp, r.body_temp, r.legs_temp, r.h, r.b, r.le, 8, 20+x*128, 20+y*128)
            n += 1


'''