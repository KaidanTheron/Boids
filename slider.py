"""
Custom class for creating sliders for values
"""

import pygame

class Slider():
    label = ""
    renderedLabel = 0
    rect = [] # [x, y, width, height]
    Range = [] # [int, int] defining the range that the slider must map to
    slidePos = 0 # position of slider circle from left of slider

    def __init__(self, label, pos, Range, fontSize = 15, fontColour = (0, 0, 0)):
        self.label = label
        self.pos = pos
        self.Range = Range
        self.slidePos = pos[0]

        font = pygame.font.Font('freesansbold.ttf', fontSize)
        self.renderedLabel = font.render(self.label, True, fontColour)

    def setSlidePos(self, mousePos):
        if mousePos[0] > (self.pos[0]+self.pos[2]):
            mousePos[0] = self.pos[0]+self.pos[2]
        elif mousePos[0] < self.pos[0]:
            mousePos[0] = self.pos[0]
        
        self.slidePos = mousePos[0]

    def findSlideVal(self):
        return self.slidePos - self.pos[0] # value of slider would be distance of circle from left side of slider 

    # maps the current pos of the slider circle to the correspodning value in the given range
    def mapToRange(self):
        return ((self.Range[1]-self.Range[0]) / (self.pos[2])) * self.findSlideVal() + self.Range[0]

    # return true if number is in given range
    def between(self, val, numRange):
        return (val <= numRange[1]) & (val >= numRange[0])

    # check if mouse position is overlapping with the slider box
    def boundsCheck(self, mousePos):
        return self.between(mousePos[0], [self.pos[0], self.pos[0]+self.pos[2]]) & self.between(mousePos[1], [self.pos[1], self.pos[1]+self.pos[3]])

    def render(self, surface):
        pygame.draw.rect(surface, [200, 200, 200], self.pos)
        surface.blit(self.renderedLabel, [self.pos[0], self.pos[1]])

        labelRect = self.renderedLabel.get_rect()

        pygame.draw.rect(surface, [0, 120, 0], [self.pos[0], self.pos[1]+labelRect.height, self.pos[2], 20])
        pygame.draw.rect(surface, [0, 60, 0], [self.slidePos, self.pos[1]+labelRect.height, self.pos[2]-self.slidePos+self.pos[0], 20])

        pygame.draw.circle(surface, [255, 255, 255], [self.slidePos, self.pos[1]+labelRect.height+10], 10)
        surface.blit(self.renderedLabel, [self.pos[0], self.pos[1]])