import pygame as pg


from settings import settings
from simulation import setup, mainloop


pg.init()
info = pg.display.Info()
screensize = settings["win_size"]
offset = [screensize[x] / 2  for x in range(2)]
screen = pg.display.set_mode(screensize)
clock = pg.time.Clock()

centre = [0, 0]
move = [False  for x in range(4)]
reset = False
blobs = setup()
done = False
while not done:
    for E in pg.event.get():
        if E.type == pg.QUIT:
            done = True
        if E.type == pg.KEYDOWN:
            for x in range(4):
                if E.key == settings["cam_typ"][x]:
                    settings["camera"] = ["fixed", "largest", "com", "adjust"][x]
            if settings["camera"] == "adjust":
                for x in range(4):
                    if E.key == settings["cam_move"][x]:
                        move[x] = True
                if E.key == settings["cam_reset"]:
                    reset = True
        if E.type == pg.KEYUP:
            if settings["camera"] == "adjust":
                for x in range(4):
                    if E.key == settings["cam_move"][x]:
                        move[x] = False
                    
            
    blobs = mainloop(blobs)
    screen.fill((255,255,255))

    if settings["camera"] == "fixed":
        centre = [0, 0]
    if settings["camera"] == "largest": 
        upper = blobs[0].mass
        centre = blobs[0].pos[:]
        for b in range(1, len(blobs)):
            if blobs[b].mass > upper:
                centre = blobs[b].pos[:]
    if settings["camera"] == "com":
        centre = [0, 0]
        total_mass = 0
        for B in blobs:
            for x in range(2):
                centre[x] += B.pos[x] * B.mass
                total_mass += B.mass
        for x in range(2):
            centre[x] /= total_mass
    if settings["camera"] == "adjust":
        if reset:
            centre = [0, 0]
            reset = False
        else:
            if move[0]:
                centre[1] -= settings["cam_step"]
            elif move[1]:
                centre[0] -= settings["cam_step"]
            elif move[2]:
                centre[1] += settings["cam_step"]
            elif move[3]:
                centre[0] += settings["cam_step"]

    for B in blobs:
        if settings["trail"]:
            for S in B.secondary:
                for h, H in enumerate(S):
                    pg.draw.circle(
                        screen,
                        [((255+B.colour[i])/2) + ((1-(h/settings["trail_len"])) * ((255-B.colour[i])/2)) for i in range(3)],
                        [round(H[0][x] + offset[x] - centre[x])  for x in range(2)],
                        round(H[1])
                        )
            for h, H in enumerate(B.history):
                pg.draw.circle(
                    screen,
                    [((255+B.colour[i])/2) + ((1-(h/settings["trail_len"])) * ((255-B.colour[i]) / 2)) for i in range(3)],
                    [round(H[0][x] + offset[x] - centre[x])  for x in range(2)],
                    round(H[1])
                    )
    for B in blobs:
        pg.draw.circle(
            screen,
            B.colour,
            [round(B.pos[x] + offset[x] - centre[x])  for x in range(2)],
            round(B.radius)
            )
    pg.display.update()

    clock.tick(50)

pg.quit()
