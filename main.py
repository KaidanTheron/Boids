"""
Run this file, make sure slider.py and boid.py are in the same folder as this one, otherwise it won't work.

On left of screen:
    There will be sliders for each of the properties of the boids
    There will be a run button to run the simulation with the given slider values
On right of screen:
    This is where the simulation is shown

This project is based on the information provided by wikipedia about boids
"""

from boid import Boid
import pygame
from pygame import *
import math
import random
import sys
from slider import Slider

from pygame import mouse
from pygame.time import Clock

pygame.init()

#######################################
# Setup
clock = Clock()
frameRate = 60

sliderDict = dict() # dict of sliders for easy iteration

# Screen size and settings, simulation panel size
screenHeight = 600
simulatonWidth = 600
settingsWidth = 200
screenWidth = settingsWidth + simulatonWidth

screen = pygame.display.set_mode(size=(screenWidth, screenHeight))

# screen colours
simulationBackCol = (125, 125, 125)
settingsBackCol = (125, 125, 255)

# fun draw mode, turn this to True if you want (epilepsy warning)
drawMode = False

# Boids setup
numBoids = 100
drawSteer = False

boidColR = 255
sliderDict["boidColR"] = Slider("R", [0, 0, settingsWidth, 35], [0, 255])

boidColG = 255
sliderDict["boidColG"] = Slider("G", [0, 35, settingsWidth, 35], [0, 255])

boidColB = 255
sliderDict["boidColB"] = Slider("B", [0, 70, settingsWidth, 35], [0, 255])

separationStrength = 1
sliderDict["separationStrength"] = Slider("Separation Strength", [0, 105, settingsWidth, 35], [0, 1])

alignmentStrength = 1
sliderDict["alignmentStrength"] = Slider("Alignment Strength", [0, 140, settingsWidth, 35], [0, 1])

cohesionStrength = 1
sliderDict["cohesionStrength"] = Slider("Cohesion Strength", [0, 175, settingsWidth, 35], [0, 1])

boidSpeed = 1
sliderDict["boidSpeed"] = Slider("Boid Speed", [0, 210, settingsWidth, 35], [1, 10])

wanderStrength = 1
sliderDict["wanderStrength"] = Slider("Wander Strength", [0, 245, settingsWidth, 35], [0, math.pi*2])

visionRadius = 30
sliderDict["visionRadius"] = Slider("Vision Radius", [0, 280, settingsWidth, 35], [0, 100])

runStrength = 1
sliderDict["runStrength"] = Slider("Run Strength", [0, 315, settingsWidth, 35], [-1, 1])

# default settings for sliders set
sliderDict["separationStrength"].setSlidePos([82, 0])
sliderDict["alignmentStrength"].setSlidePos([79, 0])
sliderDict["cohesionStrength"].setSlidePos([29, 0])
sliderDict["boidSpeed"].setSlidePos([96, 0])
sliderDict["wanderStrength"].setSlidePos([0, 0])
sliderDict["visionRadius"].setSlidePos([133, 0])
sliderDict["runStrength"].setSlidePos([100, 0])

boidCol = (sliderDict["boidColR"].mapToRange(), sliderDict["boidColG"].mapToRange(), sliderDict["boidColG"].mapToRange())
boids = []
for i in range(numBoids):
    randNum = random.randint(-15, 15)
    boids.append(Boid([random.randint(settingsWidth, screenWidth), 
    random.randint(0, screenHeight)], [randNum, (15**2 - randNum**2)**0.5]))

# get abs value
def abs(value):
    return (value**2)**0.5

# runtime loop
def main():
    run = True
    mouseDown = False
    numframes = 0
    quit = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit = True
            if quit:    
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False

        mousePos = mouse.get_pos()

        # if the mouse is pressed make sure the relevant slider is changed accordingly
        if mouseDown:
            for key in sliderDict.keys():
                if sliderDict[key].boundsCheck(mousePos):
                    sliderDict[key].setSlidePos(mousePos)
                    break

        if not drawMode:
            screen.fill(simulationBackCol)

        # update and render each boid
        for boid in boids:
            boid.visionRadius = sliderDict["visionRadius"].mapToRange()
            boid.steer(boids, sliderDict["separationStrength"].mapToRange(), sliderDict["alignmentStrength"].mapToRange(), 
            sliderDict["cohesionStrength"].mapToRange(), sliderDict["wanderStrength"].mapToRange(),
            sliderDict["runStrength"].mapToRange(), mousePos)
            boid.render(screen, (sliderDict["boidColR"].mapToRange(), sliderDict["boidColG"].mapToRange(), sliderDict["boidColB"].mapToRange()), drawSteer)
            boidAngle = boid.getAngle(boid.steerVector)
            boid.pos[0] += sliderDict["boidSpeed"].mapToRange()*math.cos(boidAngle)
            if boid.pos[0] > 800:
                boid.pos[0] -= 600
            if boid.pos[0] < 200:
                boid.pos[0] += 600
            boid.pos[1] += sliderDict["boidSpeed"].mapToRange()*math.sin(boidAngle)
            if boid.pos[1] > 600:
                boid.pos[1] -= 600
            elif boid.pos[1] < 0:
                boid.pos[1] += 600

        pygame.draw.rect(screen, settingsBackCol, [0, 0, settingsWidth, screenHeight])


        # render all sliders and change variables accordingly
        for key in sliderDict.keys():
            sliderDict[key].render(screen)

        # update frame
        pygame.display.flip()
        if drawMode:
            numframes += 0.02
            if numframes >= math.pi*2:
                numframes = 0
            sliderDict["boidColR"].setSlidePos([abs(math.sin(numframes)*settingsWidth), 0])
        clock.tick(frameRate)

main()