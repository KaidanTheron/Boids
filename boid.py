"""
This is the class that defines a boid object and how it behaves

The boids will have a steer direction as a vector, which dictates what direction they move.
The boids will also have a vision cone, dictating which boids they can see that will effect their steering direction.
"""
import math
from random import random
import pygame

class Boid():
    pos = [] # x, y of where boid is
    steerVector = [] # vector for steering that always has a magnitude of visionRadius
    visionAngle = 0 # angle in range from 0 to 2 pi of how much the boid can see
    visionRadius = 0
    def __init__(self, pos, steerVector = [15, 0], visionAngle = math.pi*2, visionRadius = 100):
        self.pos = pos
        self.steerVector = steerVector
        self.visionAngle = visionAngle
        self.visionRadius = visionRadius

    # # this will return true if the given boid is within the vision angle of the boid
    # def withinAngle(self, boid):
    #     boidAngle = boid.getAngle([boid.pos[0]-self.pos[0], boid.pos[1]-self.pos[1]])
    #     ownAngle = self.getAngle(self.steerVector)
    #     return (ownAngle+0.5*self.visionAngle >= boidAngle and ownAngle-0.5*self.visionAngle <= boidAngle)

    # this will return true if the given boid is within the vision radius of this boid
    def withinRadius(self, boid):
        distance = math.dist([boid.pos[0], boid.pos[1]], [self.pos[0], self.pos[1]])
        return (distance <= self.visionRadius and distance > 0)

    # this will use the vision cone to find a list of boids that it can see, those boids will the influence the
    # steering of this boid
    def getVisibleBoids(self, livingBoids):
        visibleBoids = []

        for boid in livingBoids:
            if self.withinRadius(boid):# and self.withinAngle(boid):
                visibleBoids.append(boid)

        return visibleBoids

    # gets all the important values from the visible boids to be used for steering
    def getValues(self, numBoids, visibleBoids):

        if numBoids > 0:
            averageAngle = 0
            averagePosX = 0
            averagePosY = 0
            closestBoid = []
            distancetoClosestBoid = 800

            for boid in visibleBoids:
                averageAngle += boid.getAngle(boid.steerVector)
                averagePosX += boid.pos[0]
                averagePosY += boid.pos[1]
                distanceToBoid = math.dist([self.pos[0], self.pos[1]], [boid.pos[0], boid.pos[1]])
                
                if distanceToBoid < distancetoClosestBoid:
                    closestBoid = [boid.pos[0], boid.pos[1]]
                    distancetoClosestBoid = distanceToBoid

            averagePosX /= numBoids
            averagePosY /= numBoids
            averageAngle /= numBoids

            return averageAngle, averagePosX, averagePosY, closestBoid
        return self.getAngle(self.steerVector), self.pos[0], self.pos[1], 0

    # takes in list of boids and uses those to change steering
    def steer(self, livingBoids, separationStength, alignmentStrength, cohesionStrength, wanderStrength, runStrength, mousePos):
        visibleBoids = self.getVisibleBoids(livingBoids)
        numBoids = len(visibleBoids)

        averageAngle, averagePosX, averagePosY, closestBoid = self.getValues(numBoids, visibleBoids)
  
        self.alignment(alignmentStrength, averageAngle)
        self.cohesion(cohesionStrength, averagePosX, averagePosY)
        self.wander(wanderStrength)
        self.separation(separationStength, closestBoid)
        self.run(runStrength, mousePos)

    # influence steering to steer away from visible boids boids
    def separation(self, separationStrength, closestBoid):
        if closestBoid == 0:
            return
        avoidanceVector = [closestBoid[0] - self.pos[0], closestBoid[1] - self.pos[1]]

        if avoidanceVector[0] != 0 and avoidanceVector[1] != 0:
            deltaVectorX = 200*separationStrength/(avoidanceVector[0])
            deltaVectorY = 200*separationStrength/(avoidanceVector[1])

            self.steerVector = [self.steerVector[0] - deltaVectorX, self.steerVector[1] - deltaVectorY]

    # influence steering to steer away from visible boids boids
    def run(self, runStrength, mousePos):
        if mousePos == 0:
            return
        avoidanceVector = [mousePos[0] - self.pos[0], mousePos[1] - self.pos[1]]
        targetAngle = self.getAngle(avoidanceVector)

        deltaVectorX = runStrength*(15*math.cos(targetAngle)-self.steerVector[0])
        deltaVectorY = runStrength*(15*math.sin(targetAngle)-self.steerVector[1])

        self.steerVector = [self.steerVector[0] - deltaVectorX, self.steerVector[1] - deltaVectorY]

    # influence steering to have similar steering to visible boids
    def alignment(self, alignmentStrength, averageAngle):
            deltaVectorX = alignmentStrength*(15*math.cos(averageAngle)-self.steerVector[0])
            deltaVectorY = alignmentStrength*(15*math.sin(averageAngle)-self.steerVector[1])

            self.steerVector = [self.steerVector[0] + deltaVectorX, self.steerVector[1] + deltaVectorY]

    # make it so that the boids also have some random wandering
    def wander(self, wanderStrength):
        randomAngle = random()*wanderStrength + self.getAngle(self.steerVector)
        self.steerVector = [self.steerVector[0] + 15*math.cos(randomAngle), self.steerVector[1] + 15*math.sin(randomAngle)]

    # influence steering so that boid steers toward average position of visible boids
    def cohesion(self, cohesionStrength, averagePosX, averagePosY):
        targetVector = [averagePosX - self.pos[0], averagePosY - self.pos[1]]
        if targetVector != [0,0]:
            targetAngle = self.getAngle(targetVector)
            deltaVectorX = cohesionStrength*(15*math.cos(targetAngle)-self.steerVector[0])
            deltaVectorY = cohesionStrength*(15*math.sin(targetAngle)-self.steerVector[1])

            self.steerVector = [self.steerVector[0] + deltaVectorX, self.steerVector[1] + deltaVectorY]

    # find the angle between the x axis and the steer vector
    # because of the way pygame works, clockwise is the positive direction for the angle
    def getAngle(self, vector):
        if vector[0] > 0:
            return math.atan(vector[1]/vector[0])
        elif vector[0] < 0:
            return math.pi + math.atan(vector[1]/vector[0])
        elif vector[1] > 0:
            return math.pi*0.5
        elif vector[1] < 0:
            return 3*math.pi*0.5

    # calculate points of triangle of boid
    def calculatePoints(self):
        triPoints = []
        angle = self.getAngle(self.steerVector)
        deg90 = math.pi/2

        triPoints.append([self.pos[0]-5*math.sin(angle), self.pos[1]+5*math.cos(angle)])
        triPoints.append([self.pos[0]+5*math.cos(deg90-angle), self.pos[1]-5*math.sin(deg90-angle)])
        triPoints.append([self.pos[0]+15*math.cos(angle), self.pos[1] + 15*math.sin(angle)])
        
        return triPoints

    # render boid on surface
    def render(self, screen, colour, drawSteer):
        triPoints = self.calculatePoints()
        pygame.draw.polygon(surface=screen, color=colour, points=[triPoints[0], triPoints[1], triPoints[2]])
        if drawSteer:
            pygame.draw.line(screen, colour, [self.pos[0], self.pos[1]], [self.pos[0]+20*math.cos(self.getAngle(self.steerVector)), 
            self.pos[1]+20*math.sin(self.getAngle(self.steerVector))])