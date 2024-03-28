from collections import deque
from copy import deepcopy
from random import uniform, gauss, randint


from settings import settings


class Blob:
    def __init__(self):
        self.radius = settings["radius"]
        self.mass = settings["mass"]
        self.pos = [settings["range"] * uniform(-1, 1), settings["range"] * uniform(-1, 1)]
        self.velocity = [gauss(0, settings["sigma"]), gauss(0, settings["sigma"])]
        self.active = True
        if settings["col_set"]:
            self.colour = settings["colour"]
        else:
            self.colour = [randint(0, settings["shade"])  for x in range(3)]
        if settings["trail"]:
            self.history = deque(maxlen=settings["trail_len"])
            self.secondary = []
        

    def get_speed(self):
        return ((self.velocity[0]**2) + (self.velocity[1]**2)) ** 0.5

    def diff_to(self, other):
        return [other.pos[x] - self.pos[x]  for x in range(2)]

    def dist_to(self, other):
        diff = self.diff_to(other)
        return diff, ((diff[0]**2) + (diff[1]**2)) ** 0.5

    def merge(self, other):
        if self.active and other.active:
            diff, dist = self.dist_to(other)
            if dist < self.radius + other.radius:
                proportional_mass = other.mass / (self.mass + other.mass)
                momentum = [(self.mass * self.velocity[x]) + (other.mass * other.velocity[x])  for x in range(2)]
                
                self.pos = [self.pos[x] + (diff[x] * proportional_mass)  for x in range(2)]
                self.mass += other.mass
                self.velocity = [momentum[x] / self.mass  for x in range(2)]
                self.radius = ((self.radius**2) + (other.radius**2)) ** 0.5
                
                other.active = False
                if settings["trail"]:
                    self.secondary.append(other.history)
                    self.secondary += other.secondary

    def attract_to(self, other):
        diff, dist = self.dist_to(other)
        diff = [diff[x] / (abs(diff[0]) + abs(diff[1]))  for x in range(2)]
        force = (other.mass * settings["gravity"]) / (dist**2)
        acceleration = [diff[x] * force  for x in range(2)]
        self.velocity = [self.velocity[x] + acceleration[x]  for x in range(2)]

    def move(self):
        if settings["trail"]:
            self.history.append([self.pos, self.radius])
            self.secondary = [X for X in self.secondary if len(X)>0]
            for x in range(len(self.secondary)):
                self.secondary[x].popleft()
        self.pos = [self.pos[x] + self.velocity[x]  for x in range(2)]


def setup():
    blobs = [Blob() for x in range(settings["blobs"])]
    return blobs


def mainloop(blobs):
    for x in range(len(blobs)-1):
        for y in range(x+1, len(blobs)):
            blobs[x].merge(blobs[y])
    blobs = [B for B in blobs if B.active]
    for x in range(len(blobs)):
        for y in range(len(blobs)):
            if x != y:
                blobs[x].attract_to(blobs[y])
    for x in range(len(blobs)):
        blobs[x].move()
    return blobs
                        
if __name__ == "__main__":
    blobs = setup()
    for x in range(1000):
        blobs = mainloop(blobs)
